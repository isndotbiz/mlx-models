#!/usr/bin/env python3
"""
MLX LM Server - OpenAI-compatible API server for MLX models.
Serves Qwen3-30B-A3B MoE models directly via mlx_lm, bypassing LM Studio.
"""

import argparse
import json
import time
import uuid
from contextlib import asynccontextmanager
from typing import Optional

import mlx.core as mx
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from mlx_lm import load, generate
from mlx_lm.utils import generate_step
from pydantic import BaseModel, Field

# Global model state
MODEL = None
TOKENIZER = None
MODEL_ID = None

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


# --- Request/Response schemas ---

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

def apply_chat_template(messages: list[ChatMessage]) -> str:
    """Apply the tokenizer's chat template to format messages."""
    formatted = [{"role": m.role, "content": m.content} for m in messages]
    return TOKENIZER.apply_chat_template(
        formatted, tokenize=False, add_generation_prompt=True
    )


def generate_text(prompt: str, max_tokens: int, temperature: float,
                   top_p: float, repetition_penalty: float) -> tuple[str, int, int]:
    """Generate text and return (text, prompt_tokens, completion_tokens)."""
    tokens = mx.array(TOKENIZER.encode(prompt))
    prompt_len = tokens.shape[0]

    # Use mlx_lm.generate for simplicity
    response = generate(
        MODEL,
        TOKENIZER,
        prompt=prompt,
        max_tokens=max_tokens,
        temp=temperature,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
    )

    completion_tokens = len(TOKENIZER.encode(response))
    return response, prompt_len, completion_tokens


def generate_stream(prompt: str, max_tokens: int, temperature: float,
                    top_p: float, repetition_penalty: float):
    """Generate text token by token for streaming."""
    tokens = mx.array(TOKENIZER.encode(prompt))
    prompt_len = tokens.shape[0]
    detokenizer = TOKENIZER._tokenizer  # sentencepiece/tiktoken detokenizer

    generated = 0
    for (token, _), _ in zip(
        generate_step(
            tokens,
            MODEL,
            temp=temperature,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
        ),
        range(max_tokens),
    ):
        token_id = token.item()
        # Check for EOS
        if token_id == TOKENIZER.eos_token_id:
            break
        text = TOKENIZER.decode([token_id])
        generated += 1
        yield text, prompt_len, generated


# --- API Endpoints ---

@app.get("/v1/models")
async def list_models():
    models = []
    for key, info in AVAILABLE_MODELS.items():
        models.append({
            "id": key,
            "object": "model",
            "owned_by": "local",
            "created": int(time.time()),
        })
    return {"object": "list", "data": models}


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    # Switch model if needed
    if request.model != MODEL_ID and request.model in AVAILABLE_MODELS:
        load_model(request.model)

    prompt = apply_chat_template(request.messages)
    request_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    created = int(time.time())

    if request.stream:
        async def stream_response():
            for text, p_tokens, c_tokens in generate_stream(
                prompt, request.max_tokens, request.temperature,
                request.top_p, request.repetition_penalty
            ):
                chunk = {
                    "id": request_id,
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": MODEL_ID,
                    "choices": [{
                        "index": 0,
                        "delta": {"content": text},
                        "finish_reason": None,
                    }],
                }
                yield f"data: {json.dumps(chunk)}\n\n"

            # Final chunk
            final = {
                "id": request_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": MODEL_ID,
                "choices": [{
                    "index": 0,
                    "delta": {},
                    "finish_reason": "stop",
                }],
            }
            yield f"data: {json.dumps(final)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(stream_response(), media_type="text/event-stream")

    # Non-streaming
    text, prompt_tokens, completion_tokens = generate_text(
        prompt, request.max_tokens, request.temperature,
        request.top_p, request.repetition_penalty
    )

    return ChatCompletionResponse(
        id=request_id,
        created=created,
        model=MODEL_ID,
        choices=[Choice(message=ChatMessage(role="assistant", content=text))],
        usage=Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        ),
    )


@app.get("/health")
async def health():
    return {"status": "ok", "model": MODEL_ID}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MLX LM Server")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        choices=list(AVAILABLE_MODELS.keys()),
                        help=f"Model to load (default: {DEFAULT_MODEL})")
    parser.add_argument("--port", type=int, default=8080,
                        help="Port to serve on (default: 8080)")
    parser.add_argument("--host", default="127.0.0.1",
                        help="Host to bind to (default: 127.0.0.1)")
    args = parser.parse_args()

    app.state.initial_model = args.model
    print(f"Starting MLX LM Server on {args.host}:{args.port}")
    print(f"Available models: {list(AVAILABLE_MODELS.keys())}")
    uvicorn.run(app, host=args.host, port=args.port)
