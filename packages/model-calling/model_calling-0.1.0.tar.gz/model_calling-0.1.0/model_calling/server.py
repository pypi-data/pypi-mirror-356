"""
FastAPI server for the model-calling service.
"""
import json
import logging
import asyncio
import os
from typing import Dict, Any, List, Optional, Union
from fastapi import FastAPI, Request, Response, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

import httpx
import json
from model_calling.registry import registry
from model_calling.ollama_adapter import OllamaAdapter
from model_calling.cache import embedding_cache
from model_calling.embedding_adapter import create_openai_embedding_response, EmbeddingAdapter
from model_calling.granite_guardian_adapter import GraniteGuardianAdapter

# Load environment variables from .env file if present
load_dotenv()

app = FastAPI(title="Model Calling Service", version="0.1.0")

logger = logging.getLogger(__name__)


# Models for API validation
class Message(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    function_call: Optional[Dict[str, Any]] = None
    name: Optional[str] = None


class FunctionParameters(BaseModel):
    type: str
    properties: Dict[str, Any]
    required: Optional[List[str]] = None


class FunctionDefinition(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: FunctionParameters


class Tool(BaseModel):
    type: str = "function"
    function: FunctionDefinition


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    tools: Optional[List[Tool]] = None
    user: Optional[str] = None
    response_format: Optional[Dict[str, str]] = None


# Embedding model request schema
class EmbeddingRequest(BaseModel):
    model: str
    input: Union[str, List[str]]
    dimensions: Optional[int] = None
    user: Optional[str] = None


class ModerationRequest(BaseModel):
    input: Union[str, List[str]]
    model: Optional[str] = None


@app.post("/v1/moderations")
async def moderations(request: Request):
    """OpenAI-compatible content moderation endpoint"""
    # Parse the request body
    body = await request.json()
    
    # Validate request format
    try:
        validated_request = ModerationRequest(**body)
    except Exception as e:
        logger.error(f"Invalid request format: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request format: {e}")
    
    # Get the appropriate adapter
    model_name = validated_request.model or "granite-guardian"
    adapter = registry.get_adapter(model_name)
    
    if not adapter:
        # Create a new adapter instance if not found
        adapter = GraniteGuardianAdapter({"model_name": model_name})
        registry.register_adapter_class("granite-guardian", GraniteGuardianAdapter)
    
    # Convert to model-specific format
    try:
        translated_request = await adapter.translate_request(body)
    except Exception as e:
        logger.error(f"Error translating request: {e}")
        raise HTTPException(status_code=500, detail=f"Error translating request: {e}")
    
    # Call the model
    try:
        model_response = await adapter.call_model(translated_request)
        translated_response = await adapter.translate_response(model_response)
        
        # Return the moderation results
        return translated_response
    except Exception as e:
        logger.error(f"Error calling model: {e}")
        raise HTTPException(status_code=500, detail=f"Error calling model: {e}")


@app.get("/")
async def root():
    """Service health check endpoint"""
    return {"status": "ok", "service": "model-calling"}


@app.get("/v1/models")
async def list_models():
    """List available models with their capabilities"""
    # Get models from registry
    models = await registry.list_available_models()
    
    # If no models found, return a static list for testing
    if not models:
        models = [
            {"id": "ollama/mistral-small3.1:24b", "object": "model"},
            {"id": "ollama/llama3:8b", "object": "model"},
            {"id": "ollama/qwen:7b", "object": "model"},
            {"id": "vllm/mistral-7b", "object": "model"}
        ]
    else:
        # Update capabilities for vision models
        for model in models:
            model_id = model.get("id")
            if model_id and "llava" in model_id.lower():
                # Get fresh adapter to ensure capabilities are up-to-date
                adapter = registry.get_adapter(model_id)
                if adapter and hasattr(adapter, "supports_vision"):
                    # Update vision capability
                    model["capabilities"]["supports_vision"] = adapter.supports_vision
                    model["capabilities"]["verified"] = True
                    logger.info(f"Updated vision capabilities for {model_id}: {adapter.supports_vision}")
    
    return {
        "object": "list",
        "data": models
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """OpenAI-compatible chat completions endpoint"""
    # Parse the request body
    body = await request.json()
    
    # Validate request format
    try:
        validated_request = ChatCompletionRequest(**body)
    except Exception as e:
        logger.error(f"Invalid request format: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request format: {e}")
    
    # Get the appropriate adapter
    model_name = validated_request.model
    adapter = registry.get_adapter(model_name)
    
    if not adapter:
        raise HTTPException(status_code=404, detail=f"Model not found: {model_name}")
    
    # Get model capabilities
    capabilities = registry.get_capabilities(model_name)
    
    # Check for unsupported features and provide warnings
    warnings = []
    
    # Check if tools are requested but not supported
    if validated_request.tools and not capabilities.supports_function_call:
        warning_msg = f"Model {model_name} does not support tools/functions. The tools will be ignored."
        warnings.append(warning_msg)
        logger.warning(warning_msg)
    
    # Check if streaming is requested but not supported
    if validated_request.stream and not capabilities.supports_streaming:
        warning_msg = f"Model {model_name} does not support streaming. Falling back to non-streaming mode."
        warnings.append(warning_msg)
        logger.warning(warning_msg)
        # Force non-streaming mode
        validated_request.stream = False
        
    # Check if JSON mode is requested but not supported
    if (validated_request.response_format and 
        validated_request.response_format.get("type") == "json_object" and 
        not capabilities.supports_json_mode):
        warning_msg = f"Model {model_name} may not reliably support JSON mode. Results may be inconsistent."
        warnings.append(warning_msg)
        logger.warning(warning_msg)
        
    # Check for reasoning capabilities
    # Look for reasoning-related prompts in the messages
    reasoning_keywords = ["step by step", "think through", "reasoning", "solve this problem", "explain your thinking"]
    
    # Check if any message contains reasoning keywords
    has_reasoning_prompt = False
    for message in validated_request.messages:
        if message.content and any(keyword in message.content.lower() for keyword in reasoning_keywords):
            has_reasoning_prompt = True
            break
    
    # Warn if reasoning is requested but not well supported
    if has_reasoning_prompt and not capabilities.supports_reasoning:
        warning_msg = f"Model {model_name} may not have strong reasoning capabilities. Results may be inconsistent."
        warnings.append(warning_msg)
        logger.warning(warning_msg)
    
    # Convert to model-specific format
    try:
        translated_request = await adapter.translate_request(body)
    except Exception as e:
        logger.error(f"Error translating request: {e}")
        raise HTTPException(status_code=500, detail=f"Error translating request: {e}")
    
    # Stream or normal response
    if validated_request.stream:
        return StreamingResponse(
            stream_response(adapter, translated_request),
            media_type="text/event-stream"
        )
    else:
        # Call the model
        try:
            model_response = await adapter.call_model(translated_request)
            translated_response = await adapter.translate_response(model_response)
            
            # Add warnings to response if any
            if warnings:
                if "warnings" not in translated_response:
                    translated_response["warnings"] = []
                translated_response["warnings"].extend(warnings)
            return translated_response
        except Exception as e:
            logger.error(f"Error calling model: {e}")
            raise HTTPException(status_code=500, detail=f"Error calling model: {e}")


@app.post("/v1/embeddings")
async def create_embeddings(request: Request):
    """OpenAI-compatible embeddings endpoint"""
    # Parse the request body
    body = await request.json()
    
    # Validate request format
    try:
        validated_request = EmbeddingRequest(**body)
    except Exception as e:
        logger.error(f"Invalid embedding request format: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid embedding request format: {e}")
    
    # Get the appropriate embedding adapter
    model_name = validated_request.model
    adapter = registry.get_embedding_adapter(model_name)
    
    if not adapter:
        raise HTTPException(status_code=404, detail=f"Embedding model not found: {model_name}")
    
    # Let the adapter validate the request first
    try:
        # Create a copy of the request for validation
        validation_request = validated_request.dict()
        await adapter.translate_request(validation_request)
    except Exception as e:
        logger.error(f"Request validation failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
        
    # If validation passed, handle single/batch inputs
    inputs = validated_request.input
    if isinstance(inputs, str):
        inputs = [inputs]
    
    # Process inputs - differs by adapter type
    try:
        # Check if using Ollama adapter which needs special batch handling
        if model_name.startswith("ollama/") or (not "/" in model_name):
            # Ollama doesn't support batch processing natively, handle manually
            all_embeddings = []
            
            for input_text in inputs:
                # Check cache first
                cached_embedding = embedding_cache.get(model_name, input_text)
                if cached_embedding is not None:
                    all_embeddings.append({"embedding": cached_embedding})
                    continue
                
                # Create a single-input request
                # For Ollama, we need to pass just the model name without the prefix
                model_short_name = validated_request.model.split("/")[-1] if "/" in validated_request.model else validated_request.model
                single_request = {
                    "model": model_short_name,
                    "input": input_text  # This will be converted to 'prompt' in translate_request
                }
                
                logger.debug(f"Processing single input for Ollama model {model_short_name}: {input_text[:50]}...")
                
                # Add optional parameters
                if validated_request.dimensions:
                    single_request["dimensions"] = validated_request.dimensions
                
                # Translate request for the model (converts 'input' to 'prompt' for Ollama)
                translated_request = await adapter.translate_request(single_request)
                
                # Call the model for each input
                model_response = await adapter.call_model(translated_request)
                all_embeddings.append(model_response)
                
                # Cache the result
                if "embedding" in model_response:
                    embedding_cache.set(model_name, input_text, model_response["embedding"])
            
            # Combine all results
            if len(inputs) == 1:
                return await adapter.translate_response(all_embeddings[0], inputs)
            else:
                # Extract embeddings from each response
                embeddings = []
                for emb_response in all_embeddings:
                    if "embedding" in emb_response:
                        embeddings.append(emb_response["embedding"])
                
                # Make a combined response with all embeddings
                combined_response = {"embeddings": embeddings}
                return await adapter.translate_response(combined_response, inputs)
        else:
            # Other providers support batching natively
            # Check if all inputs are in cache
            all_cached = True
            cached_embeddings = []
            
            for input_text in inputs:
                cached_embedding = embedding_cache.get(model_name, input_text)
                if cached_embedding is None:
                    all_cached = False
                    break
                cached_embeddings.append(cached_embedding)
            
            # If all items are cached, return directly
            if all_cached:
                logger.info(f"Using cached embeddings for all {len(inputs)} inputs")
                return create_openai_embedding_response(
                    model=model_name,
                    embeddings=cached_embeddings,
                    input_texts=inputs
                )
            
            # Otherwise, make API request
            single_request = {
                "model": validated_request.model.split("/")[-1] if "/" in validated_request.model else validated_request.model,
                "input": inputs
            }
            
            # Add optional parameters
            if validated_request.dimensions:
                single_request["dimensions"] = validated_request.dimensions
            
            # Translate request for the model
            translated_request = await adapter.translate_request(single_request)
            
            # Call the model with all inputs
            model_response = await adapter.call_model(translated_request)
            
            # Cache individual results
            response_data = model_response.get("data", [])
            for i, data_item in enumerate(response_data):
                if i < len(inputs) and "embedding" in data_item:
                    embedding_cache.set(model_name, inputs[i], data_item["embedding"])
            
            return await adapter.translate_response(model_response, inputs)
    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating embeddings: {str(e)}")


async def stream_response(adapter, translated_request):
    """Stream the model response"""
    try:
        # Ensure streaming is enabled
        translated_request["stream"] = True
        
        # Call the model with streaming
        async with httpx.AsyncClient() as client:
            endpoint = f"{adapter.base_url}/api/chat" if isinstance(adapter, OllamaAdapter) else f"{adapter.base_url}/v1/chat/completions"
            
            async with client.stream("POST", endpoint, json=translated_request, timeout=60.0) as response:
                async for chunk in response.aiter_lines():
                    if not chunk.strip():
                        continue
                    
                    try:
                        # For vLLM OpenAI-compatible endpoints, remove "data: " prefix
                        if chunk.startswith("data: "):
                            chunk = chunk[6:]
                            
                        if chunk == "[DONE]":
                            yield f"data: [DONE]\n\n"
                            break
                            
                        chunk_data = json.loads(chunk)
                        translated_chunk = await adapter.translate_streaming_chunk(chunk_data)
                        
                        # Format as SSE
                        yield f"data: {json.dumps(translated_chunk)}\n\n"
                    except json.JSONDecodeError:
                        logger.error(f"Failed to parse streaming chunk: {chunk}")
    except Exception as e:
        logger.error(f"Error in streaming: {e}")
        error_response = {
            "error": {
                "message": f"Error in streaming: {str(e)}",
                "type": "server_error"
            }
        }
        yield f"data: {json.dumps(error_response)}\n\n"


@app.post("/v1/config/update")
async def update_config(request: Request):
    """Update configuration for a model type"""
    body = await request.json()
    prefix = body.get("prefix")
    config = body.get("config", {})
    
    if not prefix:
        raise HTTPException(status_code=400, detail="Missing prefix parameter")
        
    # Update the registry configuration
    registry.update_config(prefix, config)
    
    return {"status": "ok", "message": f"Updated configuration for {prefix}"}


@app.post("/v1/models/refresh")
async def refresh_model(request: Request):
    """Force refresh of model capabilities"""
    body = await request.json()
    model_name = body.get("model")
    
    if not model_name:
        raise HTTPException(status_code=400, detail="Missing model parameter")
    
    # Clear the adapter cache to force re-verification
    registry.adapters = {}
    
    # Get the adapter to trigger capability detection
    adapter = registry.get_adapter(model_name)
    if not adapter:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
    
    # Return the updated capabilities
    capabilities = {
        "supports_function_call": adapter.supports_function_call if hasattr(adapter, "supports_function_call") else False,
        "supports_streaming": adapter.supports_streaming if hasattr(adapter, "supports_streaming") else False,
        "supports_system_messages": adapter.supports_system_messages if hasattr(adapter, "supports_system_messages") else False,
        "supports_vision": adapter.supports_vision if hasattr(adapter, "supports_vision") else False,
        "supports_json_mode": adapter.supports_json_mode if hasattr(adapter, "supports_json_mode") else False,
        "supports_reasoning": adapter.supports_reasoning if hasattr(adapter, "supports_reasoning") else False,
    }
    
    return {
        "model": model_name,
        "capabilities": capabilities,
        "status": "refreshed"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
