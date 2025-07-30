import asyncio
import json
import re
from functools import cache
from os import environ
from typing import Annotated, Any, Dict, List, Literal, Tuple, TypedDict, Union

import aiohttp
from bs4 import BeautifulSoup
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool, tool
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode
from loguru import logger
from pydantic import BaseModel, Field
from rongda_mcp_server.api import ReportType, comprehensive_search, download_report_html
from rongda_mcp_server.login import login
from rongda_mcp_server.models import FinancialReport

from xxy.client import get_llm, get_slm
from xxy.config import load_config
from xxy.stream import send_reasoning

MAX_DOC_RESULT = 8


class TextChunker:
    """
    A class for chunking long text into manageable segments and providing search/retrieval functionality.
    """

    def __init__(self, text: str, chunk_size: int = 1000, overlap: int = 10000):
        """
        Initialize the TextChunker with a long string.

        Args:
            text (str): The long text to be chunked
            chunk_size (int): Size of each chunk in characters (default: 1000)
            overlap (int): Number of overlapping characters between chunks (default: 100)
        """
        self.text = text
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunks = []
        self._create_chunks()

    def _create_chunks(self):
        """
        Create chunks from the input text with specified size and overlap.
        """
        if not self.text:
            return

        start = 0
        while start < len(self.text):
            end = start + self.chunk_size

            # If this is not the last chunk and we're not at the end of text
            if end < len(self.text):
                # Try to find a good breaking point (sentence end, paragraph, etc.)
                break_point = self._find_break_point(self.text[start:end])
                if break_point != -1:
                    end = start + break_point

            chunk = self.text[start:end].strip()
            if chunk:  # Only add non-empty chunks
                self.chunks.append(chunk)

            # Move start position with overlap consideration
            if end >= len(self.text):
                break
            start = max(start + self.chunk_size - self.overlap, start + 1)

    def _find_break_point(self, text: str) -> int:
        """
        Find a good breaking point in the text (sentence end, paragraph break, etc.).

        Args:
            text (str): Text to find break point in

        Returns:
            int: Position of break point, or -1 if no good break point found
        """
        # Look for sentence endings in the last 200 characters
        search_start = max(0, len(text) - 200)
        search_text = text[search_start:]

        # Look for paragraph breaks first
        paragraph_break = search_text.rfind("\n\n")
        if paragraph_break != -1:
            return search_start + paragraph_break

        # Look for sentence endings
        sentence_endings = [". ", "! ", "? ", ".\n", "!\n", "?\n"]
        best_break = -1

        for ending in sentence_endings:
            pos = search_text.rfind(ending)
            if pos != -1:
                best_break = max(best_break, search_start + pos + len(ending))

        return best_break if best_break != -1 else -1

    def search(
        self, keywords: Union[str, List[str]], case_sensitive: bool = False
    ) -> List[int]:
        """
        Search for chunks containing specified keywords.

        Args:
            keywords (Union[str, List[str]]): Keywords to search for
            case_sensitive (bool): Whether search should be case sensitive

        Returns:
            List[int]: Ordered list of chunk indices containing the keywords
        """
        if isinstance(keywords, str):
            keywords = [keywords]

        matching_indices = []

        for i, chunk in enumerate(self.chunks):
            search_text = chunk if case_sensitive else chunk.lower()
            search_keywords = (
                keywords if case_sensitive else [kw.lower() for kw in keywords]
            )

            # Check if any keyword is found in the chunk
            if any(keyword in search_text for keyword in search_keywords):
                matching_indices.append(i)

        return matching_indices

    def retrieval(self, index: int) -> str:
        """
        Retrieve a chunk by its index.

        Args:
            index (int): Index of the chunk to retrieve

        Returns:
            str: The chunk at the specified index

        Raises:
            IndexError: If index is out of range
        """
        if not 0 <= index < len(self.chunks):
            raise IndexError(
                f"Index {index} is out of range. Valid range: 0-{len(self.chunks)-1}"
            )

        return self.chunks[index]

    def get_chunk_count(self) -> int:
        """
        Get the total number of chunks.

        Returns:
            int: Total number of chunks
        """
        return len(self.chunks)

    def get_chunk_info(self, index: int) -> Dict[str, Any]:
        """
        Get information about a specific chunk.

        Args:
            index (int): Index of the chunk

        Returns:
            Dict[str, Any]: Information about the chunk including index, length, and preview
        """
        if not 0 <= index < len(self.chunks):
            raise IndexError(
                f"Index {index} is out of range. Valid range: 0-{len(self.chunks)-1}"
            )

        chunk = self.chunks[index]
        return {
            "index": index,
            "length": len(chunk),
            "preview": chunk[:100] + "..." if len(chunk) > 100 else chunk,
            "has_previous": index > 0,
            "has_next": index < len(self.chunks) - 1,
        }


# Global chunker instance for tool usage
_document_chunker: TextChunker = None


@tool
def load_document(text: str, chunk_size: int = 1000, overlap: int = 100) -> str:
    """
    Load a document into the text chunker for searching and reading.

    Args:
        text: The document text to load and chunk
        chunk_size: Size of each chunk in characters (default: 1000)
        overlap: Number of overlapping characters between chunks (default: 100)

    Returns:
        Status message with chunk count
    """
    global _document_chunker
    _document_chunker = TextChunker(text, chunk_size, overlap)
    chunk_count = _document_chunker.get_chunk_count()
    return f"Document loaded successfully. Created {chunk_count} chunks."


@tool
def search_document(keywords: str, case_sensitive: bool = False) -> str:
    """
    Search for chunks in the loaded document containing specified keywords.

    Args:
        keywords: Keywords to search for (can be multiple words separated by spaces)
        case_sensitive: Whether search should be case sensitive (default: False)

    Returns:
        Search results with chunk indices and previews
    """
    if _document_chunker is None:
        return "No document loaded. Please load a document first using load_document."
    
    send_reasoning(f"Searching {keywords}")
    # Split keywords by spaces if multiple keywords provided
    keyword_list = keywords.split() if " " in keywords else [keywords]

    matching_indices = _document_chunker.search(keyword_list, case_sensitive)

    if not matching_indices:
        return f"No chunks found containing keywords: {keywords}"

    results = [f"Found {len(matching_indices)} chunks containing '{keywords}':"]

    logger.info(f"🔍 Found {len(matching_indices)} chunks containing '{keywords}'")

    for idx in matching_indices:
        chunk_info = _document_chunker.get_chunk_info(idx)
        results.append(f"- Chunk {idx}: {chunk_info['preview']}")

    return "\n".join(results)


@tool
def get_chunk(index: int) -> str:
    """
    Retrieve the full content of a specific chunk by its index.

    Args:
        index: The index of the chunk to retrieve

    Returns:
        The full content of the chunk at the specified index
    """
    if _document_chunker is None:
        return "No document loaded. Please load a document first using load_document."

    logger.info(f"🔍 Getting chunk {index}")
    try:
        chunk = _document_chunker.retrieval(index)
        chunk_info = _document_chunker.get_chunk_info(index)

        nav_info = []
        if chunk_info["has_previous"]:
            nav_info.append(f"Previous chunk: {index - 1}")
        if chunk_info["has_next"]:
            nav_info.append(f"Next chunk: {index + 1}")

        nav_text = f" ({', '.join(nav_info)})" if nav_info else ""

        return f"Chunk {index}{nav_text}:\n\n{chunk}"

    except IndexError as e:
        return str(e)


@tool
def get_next_chunk(current_index: int) -> str:
    """
    Get the next chunk after the specified index.

    Args:
        current_index: The current chunk index

    Returns:
        The content of the next chunk, or error message if not available
    """
    if _document_chunker is None:
        return "No document loaded. Please load a document first using load_document."

    next_index = current_index + 1

    logger.info(f"🔍 Getting next chunk {current_index}")

    try:
        chunk = _document_chunker.retrieval(next_index)
        chunk_info = _document_chunker.get_chunk_info(next_index)

        nav_info = []
        if chunk_info["has_previous"]:
            nav_info.append(f"Previous chunk: {next_index - 1}")
        if chunk_info["has_next"]:
            nav_info.append(f"Next chunk: {next_index + 1}")

        nav_text = f" ({', '.join(nav_info)})" if nav_info else ""

        return f"Chunk {next_index}{nav_text}:\n\n{chunk}"

    except IndexError:
        return (
            f"No next chunk available. Current chunk {current_index} is the last chunk."
        )


@tool
def get_previous_chunk(current_index: int) -> str:
    """
    Get the previous chunk before the specified index.

    Args:
        current_index: The current chunk index

    Returns:
        The content of the previous chunk, or error message if not available
    """
    if _document_chunker is None:
        return "No document loaded. Please load a document first using load_document."

    prev_index = current_index - 1
    logger.info(f"🔍 Getting previous chunk {current_index}")

    if prev_index < 0:
        return f"No previous chunk available. Current chunk {current_index} is the first chunk."

    try:
        chunk = _document_chunker.retrieval(prev_index)
        chunk_info = _document_chunker.get_chunk_info(prev_index)

        nav_info = []
        if chunk_info["has_previous"]:
            nav_info.append(f"Previous chunk: {prev_index - 1}")
        if chunk_info["has_next"]:
            nav_info.append(f"Next chunk: {prev_index + 1}")

        nav_text = f" ({', '.join(nav_info)})" if nav_info else ""

        return f"Chunk {prev_index}{nav_text}:\n\n{chunk}"

    except IndexError as e:
        return str(e)


@tool
def get_document_info() -> str:
    """
    Get information about the currently loaded document.

    Returns:
        Document statistics and overview
    """
    if _document_chunker is None:
        return "No document loaded. Please load a document first using load_document."
    logger.info(f"🔍 Getting document info")
    chunk_count = _document_chunker.get_chunk_count()
    total_length = len(_document_chunker.text)
    avg_chunk_size = total_length // chunk_count if chunk_count > 0 else 0

    return f"""Document Information:
- Total chunks: {chunk_count}
- Total text length: {total_length:,} characters
- Average chunk size: {avg_chunk_size} characters
- Chunk size setting: {_document_chunker.chunk_size}
- Overlap setting: {_document_chunker.overlap}
- Index range: 0 to {chunk_count - 1}"""


# Tool list for easy access
document_tools = [
    load_document,
    search_document,
    get_chunk,
    get_next_chunk,
    get_previous_chunk,
    get_document_info,
]


async def get_rongda_seesion() -> aiohttp.ClientSession:
    config = load_config()
    if get_rongda_seesion.session is None:
        logger.info(f"🔒 Logging in to Rongda... with user {config.rongda.username}")
        get_rongda_seesion.session = await login(
            config.rongda.username, config.rongda.password
        )
    return get_rongda_seesion.session


get_rongda_seesion.session = None


async def get_rongda_doc(doc_id: str) -> str:
    session = await get_rongda_seesion()
    report = await download_report_html(
        session,
        FinancialReport(
            title=None,
            content=None,
            dateStr=None,
            security_code=None,
            downpath=None,
            htmlpath=doc_id,
        ),
    )

    if report is not None:
        return report.content
    else:
        raise Exception(f"Failed to download report: {doc_id}")


class RongdaDoc(TypedDict):
    doc_id: str
    title: str
    content_clip: str


async def search_rongda_doc(
    title_keywords: List[str], content_keywords: List[str], company_code: List[str]
) -> List[RongdaDoc]:
    session = await get_rongda_seesion()
    results = await comprehensive_search(
        session,
        company_code,
        content_keywords,
        title_keywords,
        report_types=[ReportType.ANNUAL_REPORT],
    )
    result = [
        RongdaDoc(
            doc_id=result.htmlpath, title=result.title, content_clip=result.content
        )
        for result in results
    ]

    if len(result) > MAX_DOC_RESULT:
        return result[:MAX_DOC_RESULT]
    else:
        return result


class AgentState(TypedDict):
    """Unified state for both document search and analysis"""

    user_question: str
    company_code: List[str]
    doc_id: str
    messages: List[Union[HumanMessage, AIMessage, ToolMessage]]

    # Search phase state
    found_documents: List[RongdaDoc]
    selected_doc_id: str
    search_completed: bool

    # Analysis phase state
    document_loaded: bool
    final_answer: str


class SearchAgentState(TypedDict):
    """State for the document search agent"""

    user_question: str
    company_code: List[str]
    messages: List[Union[HumanMessage, AIMessage, ToolMessage]]
    found_documents: List[RongdaDoc]
    selected_doc_id: str


@tool
async def search_documents(
    title_keywords: List[str], content_keywords: List[str], company_code: List[str]
) -> str:
    """
    Search for financial documents using title and content keywords.

    Args:
        title_keywords: Keywords for document title (e.g., "年度报告")
        content_keywords: Keywords for document content (e.g., "营业收入", "分行业", "成本")
        company_code: List of company codes to search in

    Returns:
        Search results with document IDs and content clips
    """

    logger.debug(
        f"🔍 Searching documents with title: '{title_keywords}', content: '{content_keywords}', companies: {company_code}"
    )

    try:
        results = await search_rongda_doc(
            title_keywords, content_keywords, company_code
        )

        if not results:
            return "No documents found matching the criteria."

        result_text = f"Found {len(results)} documents:\n"
        for i, doc in enumerate(results, 1):
            result_text += f"{i}. Document ID: {doc['doc_id']}\n"
            result_text += f"   Title: {doc['title']}\n"
            result_text += f"   Content clip: {doc['content_clip']}\n\n"

        logger.info(
            f"🔍 Found {len(results)} documents: {[doc['title'] for doc in results]}"
        )
        return result_text

    except Exception as e:
        logger.exception(f"❌ Error searching documents: {str(e)}")
        return f"Error searching documents: {str(e)}"


@tool
def select_document(doc_id: str, title: str) -> str:
    """
    Select a specific document for detailed analysis.

    Args:
        doc_id: The document ID to select for analysis

    Returns:
        Confirmation of document selection
    """
    # logger.success(f"📋 Document selected: {doc_id}")
    return f"Document selected: {doc_id}. Ready for detailed analysis."


def should_continue_search(state: SearchAgentState) -> str:
    """
    Determine whether to continue the search loop or proceed to document analysis
    """
    logger.trace("🔄 Evaluating search workflow...")

    # If a document is selected, proceed to analysis
    if state.get("selected_doc_id"):
        logger.trace("✅ Document selected - proceeding to analysis")
        return "analyze"

    # Continue searching
    logger.trace("🔄 Continuing document search...")
    return "continue"


def create_search_agent():
    """
    Create the document search agent
    """
    # Get the LLM
    llm = get_llm()

    # Search tools
    search_tools = [search_documents, select_document]
    logger.debug(
        f"🔍 Search tools: {[(tool.name, tool.func) for tool in search_tools]}"
    )

    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(search_tools)

    # Create system prompt for search
    search_system_prompt = f"""You are a financial document search agent. Your job is to find the most relevant financial documents for the user's question.

Available tools:
- search_documents: Search for documents using title and content keywords
- select_document: Select a specific document for detailed analysis

Guidelines for title_keywords:
- Start with 1 short keywords, if returned too many results (search returns max {MAX_DOC_RESULT} results), refine by adding more keywords
- If search gives no results, refine by reducing keywords
- Keep it simple and focused on document types
- Common financial document titles: "年度报告"
- Do NOT put complex phrases or content-specific terms in title_keywords

Guidelines for content_keywords:

- Start with 1 short keywords, if returned too many results (search returns max {MAX_DOC_RESULT} results), refine by adding more keywords
- If search gives no results, refine by reducing keywords
- Use specific terms related to the user's question
- Examples: "营业收入", "分行业", "成本", "利润", "资产", "负债"
- Can be more detailed and specific than title keywords

Strategy:
1. Analyze the user's question to understand what type of financial information they need
2. Use search_documents with appropriate title and content keywords
3. Review the search results and content clips
4. If no relevant documents found, try different keyword combinations
5. Once you find relevant documents, select the most appropriate one using select_document

Be strategic about your search - start broad, then narrow down based on results."""

    async def search_agent_node(state: SearchAgentState) -> SearchAgentState:
        """
        Search agent node that finds relevant documents
        """
        logger.trace("🔍 Search agent called - finding relevant documents")

        messages = [SystemMessage(content=search_system_prompt)]
        messages.extend(state["messages"])

        # Add the user question and company info if not already present
        if not any(
            isinstance(msg, HumanMessage) and state["user_question"] in msg.content
            for msg in messages
        ):
            question_msg = f"Find financial documents relevant to this question: {state['user_question']}\nCompany codes: {state['company_code']}"
            messages.append(HumanMessage(content=question_msg))

        # Get LLM response
        logger.debug("🧠 Calling LLM for document search reasoning...")
        response = await llm_with_tools.ainvoke(messages)
        logger.info(
            f"🧠 Search LLM response received with {len(response.tool_calls) if response.tool_calls else 0} tool calls"
        )

        # Update state with the response
        state["messages"].append(response)
        # If there are tool calls, execute them
        if response.tool_calls:
            logger.trace(f"🔧 Executing {len(response.tool_calls)} search tool calls")
            for i, tool_call in enumerate(response.tool_calls, 1):
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                logger.trace(
                    f"🔧 Search Tool {i}/{len(response.tool_calls)}: {tool_name} with args: {tool_args}"
                )

                # Find and execute the tool
                tool_func = None
                for tool in search_tools:
                    if tool.name == tool_name:
                        # For async tools, the function might be in 'coroutine' attribute instead of 'func'
                        tool_func = tool.func or tool.coroutine
                        break

                if tool_func:
                    try:
                        logger.trace(f"⚡ Executing search tool: {tool_name}")
                        if (
                            "company_code" in tool_args
                            and tool_args["company_code"] != state["company_code"]
                        ):
                            logger.warning(f"🔧 LLM tried to modify company codes!")
                            logger.warning(
                                f"   LLM provided: {tool_args['company_code']}"
                            )
                            logger.warning(
                                f"   Using original: {state['company_code']}"
                            )
                            tool_args["company_code"] = state["company_code"]

                        # Check if tool is async
                        if asyncio.iscoroutinefunction(tool_func):
                            tool_result = await tool_func(**tool_args)
                        else:
                            tool_result = tool_func(**tool_args)

                        # Special handling for select_document tool
                        if tool_name == "select_document":
                            state["selected_doc_id"] = tool_args.get("doc_id", "")
                            title = tool_args.get("title", "")
                            send_reasoning(f"Reading {title}")
                            logger.success(
                                f"📋 Document selected: {title}: {state['selected_doc_id']}"
                            )

                        logger.trace(
                            f"✅ Search tool {tool_name} executed successfully"
                        )

                        # Add tool result to messages
                        state["messages"].append(
                            ToolMessage(
                                content=tool_result, tool_call_id=tool_call["id"]
                            )
                        )
                    except Exception as e:
                        logger.exception(f"❌ Error executing search tool {tool_name}")
                        state["messages"].append(
                            ToolMessage(
                                content=f"Error executing {tool_name}: {str(e)}",
                                tool_call_id=tool_call["id"],
                            )
                        )
                else:
                    logger.error(f"❌ Search tool not found: {tool_name}")
        else:
            logger.info("💭 No tool calls in search LLM response")

        logger.trace("🔍 Search agent node completed")
        return state

    # Create the search graph
    search_workflow = StateGraph(SearchAgentState)

    # Add search node
    search_workflow.add_node("search_agent", search_agent_node)

    # Add edges
    search_workflow.set_entry_point("search_agent")
    search_workflow.add_conditional_edges(
        "search_agent",
        should_continue_search,
        {"continue": "search_agent", "analyze": END},
    )

    return search_workflow.compile()


@tool
def answer(response: str) -> str:
    """
    Provide the final answer to the user's question.

    Args:
        response: The comprehensive answer to the user's question

    Returns:
        Confirmation that the answer was provided
    """
    return (
        f"Answer provided: {response[:100]}..."
        if len(response) > 100
        else f"Answer provided: {response}"
    )


async def load_document_node(state: AgentState) -> AgentState:
    """
    Node to load the document using the doc_id
    """
    doc_id = state["doc_id"]
    logger.info(f"📄 Loading document: {doc_id}")

    try:
        # Get the document content
        doc_content = await get_rongda_doc(doc_id)
        logger.info(
            f"📄 Document content loaded, length: {len(doc_content)} characters"
        )

        # Load it into the chunker
        result = load_document.func(doc_content)
        logger.debug(f"📄 Document chunked successfully: {result}")

        # Update state
        state["document_loaded"] = True
        state["messages"].append(
            AIMessage(content=f"Document {doc_id} loaded successfully. {result}")
        )

    except Exception as e:
        logger.exception(f"❌ Failed to load document {doc_id}")
        state["document_loaded"] = False
        state["messages"].append(
            AIMessage(content=f"Failed to load document {doc_id}: {str(e)}")
        )

    return state


def should_continue(state: AgentState) -> str:
    """
    Determine whether to continue the agent loop or end
    """
    logger.trace("🔄 Evaluating whether to continue agent workflow...")

    # If document failed to load, end
    if not state["document_loaded"]:
        logger.trace("❌ Document not loaded - ending workflow")
        return "end"

    # If we have a final answer, end
    if state.get("final_answer"):
        logger.trace("✅ Final answer available - ending workflow")
        return "end"

    # Check the last message to see if it's an answer tool call
    last_message = state["messages"][-1] if state["messages"] else None
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            if tool_call["name"] == "answer":
                logger.trace("✅ Answer tool called - ending workflow")
                return "end"

    # Continue the agent loop
    logger.trace("🔄 Continuing agent workflow...")
    return "continue"


def create_document_agent():
    """
    Create the document reading agent with LangGraph
    """
    # Get the LLM
    llm = get_llm()

    # All tools including the answer tool
    all_tools = document_tools + [answer]

    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(all_tools)

    # Create system prompt
    system_prompt = """You are a document analysis agent. Your job is to:

1. Search through the loaded document to find relevant information
2. Read specific chunks that contain relevant information
3. Navigate between chunks to gather comprehensive context
4. Provide a thorough answer to the user's question

Available tools:
- search_document: Find chunks containing keywords
- get_chunk: Read full content of a specific chunk
- get_next_chunk/get_previous_chunk: Navigate between chunks
- get_document_info: Get document overview
- answer: Provide your final answer (call this when you have enough information)

Strategy:
1. Start by searching for keywords related to the user's question
2. Due to the length of document, you may find lots of related place, if so, refine your search keywords to narrow the scope
3. Read the relevant chunks found in search results
4. Due to the doc is from OCR, table may be split to a few tables, read the around section to avoid missing lines
5. If needed, read adjacent chunks for more context
6. Gather comprehensive information before answering
7. Call the 'answer' tool with your complete response

Be thorough and make sure you have sufficient information before providing an answer."""

    async def agent_node(state: AgentState) -> AgentState:
        """
        Main agent node that processes messages and calls tools
        """
        logger.trace("🤖 Agent called - processing messages and making decisions")

        messages = [SystemMessage(content=system_prompt)]
        messages.extend(state["messages"])

        # Add the user question as the latest human message if not already present
        if not any(
            isinstance(msg, HumanMessage) and state["user_question"] in msg.content
            for msg in messages
        ):
            messages.append(
                HumanMessage(
                    content=f"Please answer this question about the document: {state['user_question']}"
                )
            )
            logger.trace(f"❓ User question added: {state['user_question']}")

        # Get LLM response
        logger.debug("🧠 Calling LLM for reasoning...")
        response = await llm_with_tools.ainvoke(messages)
        logger.info(
            f"🧠 LLM response received with {len(response.tool_calls) if response.tool_calls else 0} tool calls"
        )

        # Update state with the response
        state["messages"].append(response)

        # If there are tool calls, execute them
        if response.tool_calls:
            logger.trace(f"🔧 Executing {len(response.tool_calls)} tool calls")
            for i, tool_call in enumerate(response.tool_calls, 1):
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                logger.debug(
                    f"🔧 Tool {i}/{len(response.tool_calls)}: {tool_name} with args: {tool_args}"
                )

                # Find and execute the tool
                tool_func = None
                for tool in all_tools:
                    if tool.name == tool_name:
                        # For async tools, the function might be in 'coroutine' attribute instead of 'func'
                        tool_func = tool.func or tool.coroutine
                        break

                if tool_func:
                    try:
                        logger.trace(f"⚡ Executing tool: {tool_name}")
                        # Check if tool is async
                        if asyncio.iscoroutinefunction(tool_func):
                            tool_result = await tool_func(**tool_args)
                        else:
                            tool_result = tool_func(**tool_args)

                        # Special handling for answer tool
                        if tool_name == "answer":
                            state["final_answer"] = tool_args.get("response", "")
                            logger.debug(
                                f"✅ Final answer provided: {tool_args.get('response', '')[:100]}..."
                            )

                        logger.debug(
                            f"✅ Tool {tool_name} executed successfully: {tool_result[:100]}..."
                        )

                        # Add tool result to messages
                        state["messages"].append(
                            ToolMessage(
                                content=tool_result, tool_call_id=tool_call["id"]
                            )
                        )
                    except Exception as e:
                        logger.exception(f"❌ Error executing tool {tool_name}")
                        state["messages"].append(
                            ToolMessage(
                                content=f"Error executing {tool_name}: {str(e)}",
                                tool_call_id=tool_call["id"],
                            )
                        )
                else:
                    logger.error(f"❌ Tool not found: {tool_name}")
        else:
            logger.info("💭 No tool calls in LLM response - continuing reasoning")

        logger.trace("🤖 Agent node completed")
        return state

    # Create the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("load_document", load_document_node)
    workflow.add_node("agent", agent_node)

    # Add edges
    workflow.set_entry_point("load_document")
    workflow.add_conditional_edges(
        "load_document", should_continue, {"continue": "agent", "end": END}
    )
    workflow.add_conditional_edges(
        "agent", should_continue, {"continue": "agent", "end": END}
    )

    return workflow.compile()


async def process_document_question(
    user_question: str,
    company_code: List[str],
    doc_id: str = None,
    messages: List[str] = [],
) -> str:
    """
    Process a user question - first search for relevant documents, then analyze the selected document

    Args:
        user_question: The user's question about financial documents
        company_code: List of company codes to search in
        doc_id: Optional specific document ID to analyze (skips search phase)

    Returns:
        The agent's answer to the question
    """
    logger.debug(f"🚀 Starting two-phase document processing")
    logger.debug(f"❓ User Question: {user_question}")
    logger.debug(f"🏢 Company codes: {company_code}")

    selected_doc_id = doc_id
    selected_doc_title = ""

    # Phase 1: Search for documents (if doc_id not provided)
    if not selected_doc_id:
        logger.info("🔍 Phase 1: Searching for relevant documents...")

        # Create search agent
        search_agent = create_search_agent()

        # Initialize search state
        search_state = SearchAgentState(
            user_question=user_question,
            company_code=company_code,
            messages=messages,
            found_documents=[],
            selected_doc_id="",
        )

        # Run search agent
        try:
            logger.info("🔍 Running document search workflow...")
            final_search_state = await search_agent.ainvoke(search_state)
            selected_doc_id = final_search_state.get("selected_doc_id")

            if not selected_doc_id:
                logger.warning("⚠️ No document selected by search agent")
                return "I was unable to find a relevant document for your question. Please try rephrasing your question or providing more specific keywords."

            logger.info(
                f"✅ Search phase completed. Selected document: {selected_doc_id}"
            )

        except Exception as e:
            logger.exception("❌ Error during document search")
            return f"An error occurred while searching for documents: {str(e)}"
    else:
        logger.info(
            f"📄 Skipping search phase - using provided doc_id: {selected_doc_id}"
        )

    # Phase 2: Analyze the selected document
    logger.info(f"📊 Phase 2: Analyzing document {selected_doc_id}...")

    # Create analysis agent
    logger.trace("🤖 Creating document analysis agent...")
    analysis_agent = create_document_agent()

    # Initialize analysis state
    analysis_state = AgentState(
        doc_id=selected_doc_id,
        user_question=user_question,
        messages=messages,
        document_loaded=False,
        final_answer="",
    )
    logger.trace("📊 Analysis state created")

    # Run analysis agent
    try:
        logger.trace("🎯 Running document analysis workflow...")
        final_analysis_state = await analysis_agent.ainvoke(analysis_state)

        # Return the final answer
        if final_analysis_state.get("final_answer"):
            logger.info(f"✅ Analysis completed successfully")
            return final_analysis_state["final_answer"]
        else:
            logger.warning("⚠️ No final answer provided by analysis agent")
            return "I was unable to provide a complete answer to your question. Please try rephrasing or asking a more specific question."

    except Exception as e:
        logger.exception(f"❌ Error during document analysis")
        return f"An error occurred while analyzing the document: {str(e)}"
    finally:
        # TODO: ugly cleanup, maybe use a context manager instead
        if get_rongda_seesion.session:
            await get_rongda_seesion.session.close()


# Convenience function for backward compatibility
async def process_document_question_with_doc_id(doc_id: str, user_question: str) -> str:
    """
    Process a question with a specific document ID (backward compatibility)
    """
    # Clear company codes for direct document access
    return await process_document_question(
        user_question, company_code=[], doc_id=doc_id
    )


if __name__ == "__main__":
    # Example with document search
    import sys

    # logger.remove()
    # logger.add(sys.stdout, level="INFO")

    async def main():
        result = await process_document_question(
            user_question="用中文，在 2023年年度报告 里搜索 '成本构成项目'里不同“项目”的 成本，汇总到一张表格上，单位要精确到元\n",
            company_code=["600276 恒瑞医药"],
        )
        print(result)

    asyncio.run(main())
