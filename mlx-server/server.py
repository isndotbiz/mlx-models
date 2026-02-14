#!/usr/bin/env python3
"""
MLX LM Server - OpenAI-compatible API server for MLX models.
Serves Qwen3-30B-A3B MoE models directly via mlx_lm, bypassing LM Studio.

Usage:
    ./mlx-server/.venv/bin/python3 mlx-server/server.py
    ./mlx-server/.venv/bin/python3 mlx-server/server.py --model qwen3-coder-30b-a3b
    ./mlx-server/.venv/bin/python3 mlx-server/server.py --port 8080 --no-thinking
"""

import argparse
import json
import re
import time
import uuid
from contextlib import asynccontextmanager
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from mlx_lm import load, generate
from mlx_lm.generate import stream_generate
from mlx_lm.sample_utils import make_sampler
from pydantic import BaseModel

# Global state
MODEL = None
TOKENIZER = None
MODEL_ID = None
NO_THINKING = False

AVAILABLE_MODELS = {
    "josiefied-qwen3-30b-a3b-abliterated": {
        "path": "/Users/jonathanmallinger/.lmstudio/models/mlx-community/Josiefied-Qwen3-30B-A3B-abliterated-v2-4bit",
        "display": "Josiefied Qwen3 30B A3B Abliterated v2 4bit",
    },
    "qwen3-coder-30b-a3b": {
        "path": "/Users/jonathanmallinger/.lmstudio/models/lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-MLX-4bit",
        "display": "Qwen3 Coder 30B A3B Instruct MLX 4bit",
    },
}

DEFAULT_MODEL = "josiefied-qwen3-30b-a3b-abliterated"


def load_model(model_key: str):
    global MODEL, TOKENIZER, MODEL_ID
    if model_key not in AVAILABLE_MODELS:
        raise ValueError(f"Unknown model: {model_key}. Available: {list(AVAILABLE_MODELS.keys())}")

    info = AVAILABLE_MODELS[model_key]
    print(f"Loading model: {info['display']}...")
    print(f"  Path: {info['path']}")
    start = time.time()
    MODEL, TOKENIZER = load(info["path"])
    MODEL_ID = model_key
    elapsed = time.time() - start
    print(f"  Loaded in {elapsed:.1f}s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model(app.state.initial_model)
    yield


app = FastAPI(title="MLX LM Server", lifespan=lifespan)


# --- Schemas ---

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = DEFAULT_MODEL
    messages: list[ChatMessage]
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 2048
    stream: bool = False
    repetition_penalty: float = 1.0


class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class Choice(BaseModel):
    index: int = 0
    message: ChatMessage
    finish_reason: str = "stop"


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[Choice]
    usage: Usage


# --- Helpers ---

def strip_thinking(text: str) -> str:
    """Remove <think>...</think> blocks from response."""
    return re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL).strip()


def apply_chat_template(messages: list[ChatMessage]) -> str:
    """Apply the tokenizer's chat template to format messages."""
    formatted = [{"role": m.role, "content": m.content} for m in messages]
    kwargs = {"tokenize": False, "add_generation_prompt": True}
    if NO_THINKING:
        kwargs["enable_thinking"] = False
    return TOKENIZER.apply_chat_template(formatted, **kwargs)


# --- API Endpoints ---

@app.get("/v1/models")
async def list_models():
    models = []
    for key in AVAILABLE_MODELS:
        models.append({
            "id": key,
            "object": "model",
            "owned_by": "local",
            "created": int(time.time()),
        })
    return {"object": "list", "data": models}


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    global MODEL, TOKENIZER, MODEL_ID

    # Switch model if needed
    if request.model != MODEL_ID and request.model in AVAILABLE_MODELS:
        load_model(request.model)

    prompt = apply_chat_template(request.messages)
    request_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    created = int(time.time())
    sampler = make_sampler(
        temp=request.temperature,
        top_p=request.top_p,
    )

    if request.stream:
        async def stream_response():
            full_text = ""
            in_think = False
            prompt_tokens = 0

            for resp in stream_generate(
                MODEL, TOKENIZER, prompt=prompt,
                max_tokens=request.max_tokens, sampler=sampler,
            ):
                prompt_tokens = resp.prompt_tokens
                text = resp.text
                full_text += text

                # If --no-thinking, skip content inside <think> tags
                if NO_THINKING:
                    if "<think>" in full_text and not in_think:
                        in_think = True
                    if in_think:
                        if "</think>" in full_text:
                            # Strip everything up to and including </think>
                            after = full_text.split("</think>", 1)[1].lstrip()
                            full_text = after
                            in_think = False
                            text = after  # emit what's after
                        else:
                            continue  # skip emitting while thinking
                    if not text:
                        continue

                chunk = {
                    "id": request_id,
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": MODEL_ID,
                    "choices": [{"index": 0, "delta": {"content": text}, "finish_reason": None}],
                }
                yield f"data: {json.dumps(chunk)}\n\n"

                if resp.finish_reason:
                    break

            final = {
                "id": request_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": MODEL_ID,
                "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
            }
            yield f"data: {json.dumps(final)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(stream_response(), media_type="text/event-stream")

    # Non-streaming
    response_text = generate(
        MODEL, TOKENIZER, prompt=prompt,
        max_tokens=request.max_tokens, sampler=sampler,
    )

    prompt_tokens = len(TOKENIZER.encode(prompt))

    if NO_THINKING:
        response_text = strip_thinking(response_text)

    completion_tokens = len(TOKENIZER.encode(response_text))

    return ChatCompletionResponse(
        id=request_id,
        created=created,
        model=MODEL_ID,
        choices=[Choice(message=ChatMessage(role="assistant", content=response_text))],
        usage=Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        ),
    )


@app.get("/health")
async def health():
    return {"status": "ok", "model": MODEL_ID, "no_thinking": NO_THINKING}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MLX LM Server")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        choices=list(AVAILABLE_MODELS.keys()),
                        help=f"Model to load (default: {DEFAULT_MODEL})")
    parser.add_argument("--port", type=int, default=8080,
                        help="Port to serve on (default: 8080)")
    parser.add_argument("--host", default="127.0.0.1",
                        help="Host to bind to (default: 127.0.0.1)")
    parser.add_argument("--no-thinking", action="store_true",
                        help="Disable thinking/reasoning mode for faster responses")
    args = parser.parse_args()

    NO_THINKING = args.no_thinking
    app.state.initial_model = args.model
    print(f"Starting MLX LM Server on {args.host}:{args.port}")
    print(f"Model: {args.model}")
    print(f"Thinking mode: {'disabled' if NO_THINKING else 'enabled'}")
    uvicorn.run(app, host=args.host, port=args.port)
