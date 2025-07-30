import asyncio
import json
import os
from functools import wraps
from typing import Any, Dict, List, Optional

from flask import Flask, Response, jsonify, request
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from xxy.rongda_agent import process_document_question
from xxy.stream import (
    create_sync_generator,
    generate_stream_response,
    run_async_in_thread,
    send_reasoning,
    setup_streaming_queue,
)

app = Flask(__name__, static_folder="chatbot", static_url_path="/chatbot")

# Get API key from environment variable
API_KEY = os.getenv("XXY_API_KEY")
if not API_KEY:
    raise ValueError("XXY_API_KEY environment variable is not set")

# Model registry to store available models
MODELS = {
    "rongda": {
        "id": "rongda",
        "object": "model",
        "created": 1677652288,
        "owned_by": "xxy",
        "permission": [],
        "root": "rongda",
        "parent": None,
        "description": "Document Q&A model for financial reports",
    }
}


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "No API key provided"}), 401

        # Check if the Authorization header starts with "Bearer "
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Invalid API key format"}), 401

        # Extract the API key
        api_key = auth_header.split(" ")[1]

        # Verify the API key
        if api_key != API_KEY:
            return jsonify({"error": "Invalid API key"}), 401

        return f(*args, **kwargs)

    return decorated


def extract_messages_from_history(messages: List[Dict[str, Any]]) -> List[BaseMessage]:
    """Extract messages from the chat history in OpenAI format."""
    return [
        BaseMessage(content=msg["content"], role=msg["role"])
        for msg in messages[:-1]
        if msg["role"] == "user" or msg["role"] == "assistant"
    ]


async def process_with_model(
    model_id: str,
    user_question: str,
    request_body: Dict[str, Any],
    messages: List[BaseMessage],
) -> str:
    """Process the request based on the model type."""
    if model_id == "rongda":
        # Extract company_code from the request body
        company_code = request_body.get("company_code", "")

        return await process_document_question(
            user_question=user_question,
            company_code=company_code.split(",") if company_code else [],
            messages=messages,
        )
    else:
        raise ValueError(f"Unsupported model: {model_id}")


@app.route("/v1/models", methods=["GET"])
# @require_api_key
def list_models():
    """List available models."""
    return jsonify({"object": "list", "data": list(MODELS.values())})


@app.route("/v1/models/<model_id>", methods=["GET"])
# @require_api_key
def get_model(model_id: str):
    """Get specific model information."""
    if model_id not in MODELS:
        return jsonify({"error": "Model not found"}), 404

    return jsonify(MODELS[model_id])


@app.route("/v1/chat/completions", methods=["POST"])
@require_api_key
def chat_completions():
    try:
        data = request.json

        # Extract model from the request
        model = data.get("model", "xxy-document-qa")
        if model not in MODELS:
            return jsonify({"error": f"Model '{model}' not found"}), 400

        # Extract messages from the request
        messages = data.get("messages", [])
        if not messages:
            return jsonify({"error": "No messages provided"}), 400

        # Get the last user message
        user_messages = [msg for msg in messages if msg["role"] == "user"]
        if not user_messages:
            return jsonify({"error": "No user message found"}), 400
        user_question = user_messages[-1]["content"]

        # Check if streaming is requested
        stream = data.get("stream", False)

        if stream:
            # Set up streaming queue
            setup_streaming_queue()

            async def create_stream():
                # Start the processing task
                processing_task = asyncio.create_task(
                    process_with_model(
                        model_id=model,
                        user_question=user_question,
                        request_body=data,
                        messages=extract_messages_from_history(messages),
                    )
                )

                # Generate streaming response
                async for chunk in generate_stream_response(processing_task):
                    yield chunk

            # Convert async generator to sync generator for Flask
            return Response(
                create_sync_generator(create_stream()),
                mimetype="text/plain",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Content-Type": "text/event-stream",
                },
            )
        else:
            # Non-streaming response
            response = run_async_in_thread(
                process_with_model,
                model_id=model,
                user_question=user_question,
                request_body=data,
                messages=extract_messages_from_history(messages),
            )

            # Format response in OpenAI style
            return jsonify(
                {
                    "id": "chatcmpl-123",
                    "object": "chat.completion",
                    "created": 1677652288,
                    "model": model,
                    "choices": [
                        {
                            "index": 0,
                            "message": {"role": "assistant", "content": response},
                            "finish_reason": "stop",
                        }
                    ],
                }
            )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
