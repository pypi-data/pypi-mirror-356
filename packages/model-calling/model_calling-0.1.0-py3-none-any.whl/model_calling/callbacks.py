"""
Callback system for model-calling.

This module provides a callback interface that allows optional integration with external
services like tracers, loggers, etc. without tight coupling.
"""
from typing import Dict, List, Any, Optional


class Callback:
    """Base interface for callbacks to hook into model requests and responses"""
    
    async def on_request_start(self, model: str, messages: List[Dict[str, Any]], **kwargs) -> None:
        """Called before sending a request to the model
        
        Args:
            model: Name of the model being called
            messages: List of messages in the request
            **kwargs: Additional request parameters
        """
        pass
    
    async def on_request_end(self, model: str, messages: List[Dict[str, Any]], 
                           response: Dict[str, Any], **kwargs) -> None:
        """Called after receiving a response from the model
        
        Args:
            model: Name of the model being called
            messages: List of messages in the request
            response: The model's response
            **kwargs: Additional request parameters
        """
        pass
    
    async def on_stream_chunk(self, model: str, messages: List[Dict[str, Any]], 
                            chunk: Dict[str, Any], **kwargs) -> None:
        """Called for each chunk in a streaming response
        
        Args:
            model: Name of the model being called
            messages: List of messages in the request
            chunk: The streaming chunk from the model
            **kwargs: Additional request parameters
        """
        pass
    
    async def on_error(self, model: str, messages: List[Dict[str, Any]], 
                      error: Exception, **kwargs) -> None:
        """Called when an error occurs during the request
        
        Args:
            model: Name of the model being called
            messages: List of messages in the request
            error: The exception that occurred
            **kwargs: Additional request parameters
        """
        pass


class DummyCallback(Callback):
    """A simple callback implementation for testing"""
    
    def __init__(self):
        self.calls = []
    
    async def on_request_start(self, model: str, messages: List[Dict[str, Any]], **kwargs) -> None:
        self.calls.append(("start", model, messages, kwargs))
    
    async def on_request_end(self, model: str, messages: List[Dict[str, Any]], 
                           response: Dict[str, Any], **kwargs) -> None:
        self.calls.append(("end", model, messages, response, kwargs))
    
    async def on_stream_chunk(self, model: str, messages: List[Dict[str, Any]], 
                            chunk: Dict[str, Any], **kwargs) -> None:
        self.calls.append(("chunk", model, messages, chunk, kwargs))
    
    async def on_error(self, model: str, messages: List[Dict[str, Any]], 
                      error: Exception, **kwargs) -> None:
        self.calls.append(("error", model, messages, error, kwargs))
