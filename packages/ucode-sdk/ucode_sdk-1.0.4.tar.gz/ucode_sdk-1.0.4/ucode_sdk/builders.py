# ucode_sdk/builders.py - FIXED AND STANDARDIZED VERSION
"""
UCode Python SDK - Builders Module (Fixed)

All builders now use the same ApiResponse class for consistency.
"""

import json
from typing import Dict, List, Any, Tuple, Optional
from urllib.parse import quote
from .models import (
    ActionBody, Request, Response, ApiResponse, GetListAggregationClientApiResponse
)
from .config import Config
from .helper import do_request


class CreateItemBuilder:
    """CreateItemBuilder - standardized to use ApiResponse"""
    
    def __init__(self, collection: str, config: Config, data: ActionBody):
        self.collection = collection
        self.config = config
        self.data = data
    
    def disable_faas(self, is_disable: bool) -> 'CreateItemBuilder':
        self.data.disable_faas = is_disable
        return self
    
    def exec(self) -> Tuple[Optional[ApiResponse], Response, Optional[Exception]]:
        """Execute create request with standardized response"""
        response = Response(status="done", error="", data={})
        
        disable_faas = str(self.data.disable_faas).lower()
        url = f"{self.config.base_url}/v2/items/{self.collection}?from-ofs={disable_faas}"
        
        app_id = self.config.app_id
        headers = {
            "authorization": "API-KEY",
            "X-API-KEY": app_id,
        }
        
        request_body = {
            "data": self.data.body,
            "disable_faas": self.data.disable_faas
        }
        
        try:
            response_bytes = do_request(
                url=url,
                method="POST",
                body=request_body,
                headers=headers
            )
            
            # Parse response using standardized ApiResponse
            api_response = ApiResponse.from_bytes(response_bytes)
            
            response.data = {
                "status": api_response.status,
                "description": api_response.description,
                "operation": "create"
            }
            
            return api_response, response, None
            
        except Exception as err:
            response.data = {
                "message": "Error creating item",
                "error": str(err)
            }
            response.status = "error"
            return None, response, err


class UpdateItemBuilder:
    """UpdateItemBuilder - standardized to use ApiResponse"""
    
    def __init__(self, collection: str, config: Config, data: ActionBody):
        self.collection = collection
        self.config = config
        self.data = data
        self._filter_params = {}
    
    def disable_faas(self, is_disable: bool) -> 'UpdateItemBuilder':
        self.data.disable_faas = is_disable
        return self
    
    def filter(self, filter_params: Dict[str, Any]) -> 'UpdateItemBuilder':
        """Add filter parameters for update operation"""
        self._filter_params.update(filter_params)
        return self
    
    def exec(self) -> Tuple[Optional[ApiResponse], Response, Optional[Exception]]:
        """Execute update request with standardized response"""
        response = Response(status="done", error="", data={})
        
        disable_faas = str(self.data.disable_faas).lower()
        url = f"{self.config.base_url}/v2/items/{self.collection}?from-ofs={disable_faas}"
        
        app_id = self.config.app_id
        headers = {
            "authorization": "API-KEY",
            "X-API-KEY": app_id,
        }
        
        # Include filter parameters in request body
        request_body = {
            "data": self.data.body,
            "disable_faas": self.data.disable_faas
        }
        
        # Add filter parameters if provided
        if self._filter_params:
            request_body.update(self._filter_params)
        
        try:
            response_bytes = do_request(
                url=url,
                method="PUT",
                body=request_body,
                headers=headers
            )
            
            # Parse response using standardized ApiResponse
            api_response = ApiResponse.from_bytes(response_bytes)
            
            response.data = {
                "status": api_response.status,
                "description": api_response.description,
                "operation": "update"
            }
            
            return api_response, response, None
            
        except Exception as err:
            response.data = {
                "message": "Error updating item",
                "error": str(err)
            }
            response.status = "error"
            return None, response, err


class DeleteItemBuilder:
    """DeleteItemBuilder - standardized to use ApiResponse"""
    
    def __init__(self, collection: str, config: Config, disable_faas: bool):
        self.collection = collection
        self.config = config
        self.disable_faas = disable_faas
        self.item_id = ""
        self._filter_params = {}
    
    def disable_faas(self, disable: bool) -> 'DeleteItemBuilder':
        self.disable_faas = disable
        return self
    
    def single(self, id: str) -> 'DeleteItemBuilder':
        """Set single item ID for deletion"""
        self.item_id = id
        return self
    
    def filter(self, filter_params: Dict[str, Any]) -> 'DeleteItemBuilder':
        """Add filter parameters for delete operation"""
        self._filter_params.update(filter_params)
        return self
    
    def exec(self) -> Tuple[Optional[ApiResponse], Response, Optional[Exception]]:
        """Execute delete request with standardized response"""
        response = Response(status="done", error="", data={})
        
        # Validate parameters
        if not self.item_id and not self._filter_params:
            error = Exception("Either item ID or filter parameters are required for delete operation")
            response.status = "error"
            response.data = {"message": "Error deleting item", "error": str(error)}
            return None, response, error
        
        disable_faas_str = str(self.disable_faas).lower()
        
        # Build URL based on operation type
        if self.item_id:
            # Single item delete
            url = f"{self.config.base_url}/v2/items/{self.collection}/{self.item_id}?from-ofs={disable_faas_str}"
            method = "DELETE"
            body = None
        else:
            # Filtered delete
            url = f"{self.config.base_url}/v2/items/{self.collection}?from-ofs={disable_faas_str}"
            method = "DELETE"
            body = self._filter_params
        
        app_id = self.config.app_id
        headers = {
            "authorization": "API-KEY",
            "X-API-KEY": app_id,
        }
        
        try:
            response_bytes = do_request(
                url=url,
                method=method,
                body=body,
                headers=headers
            )
            
            # Handle empty response (common for DELETE operations)
            if not response_bytes or response_bytes.strip() == b'':
                response.data = {
                    "message": "Item deleted successfully",
                    "deleted_id": self.item_id if self.item_id else "filtered",
                    "operation": "delete"
                }
                return None, response, None
            
            # Parse response using standardized ApiResponse
            try:
                api_response = ApiResponse.from_bytes(response_bytes)
                response.data = {
                    "status": api_response.status,
                    "description": api_response.description,
                    "operation": "delete"
                }
                return api_response, response, None
            except:
                # Handle non-JSON responses
                response.data = {
                    "message": "Item deleted successfully",
                    "operation": "delete"
                }
                return None, response, None
            
        except Exception as err:
            response.data = {
                "message": "Error deleting item",
                "error": str(err)
            }
            response.status = "error"
            return None, response, err


class GetSingleItemBuilder:
    """GetSingleItemBuilder - FIXED to use standardized ApiResponse"""
    
    def __init__(self, collection: str, config: Config, guid: str):
        self.collection = collection
        self.config = config
        self.guid = guid
    
    def exec(self) -> Tuple[Optional[ApiResponse], Response, Optional[Exception]]:
        """Execute get single request with standardized response"""
        response = Response(status="done", error="", data={})
        
        if not self.guid:
            error = Exception("GUID is required")
            response.status = "error"
            response.data = {"message": "GUID is required"}
            return None, response, error
        
        url = f"{self.config.base_url}/v2/items/{self.collection}/{self.guid}?from-ofs=true"
        
        app_id = self.config.app_id
        headers = {
            "authorization": "API-KEY",
            "X-API-KEY": app_id,
        }
        
        try:
            response_bytes = do_request(
                url=url,
                method="GET",
                body=None,
                headers=headers
            )
            
            # Parse response using standardized ApiResponse (FIXED!)
            api_response = ApiResponse.from_bytes(response_bytes)
            
            response.data = {
                "status": api_response.status,
                "description": api_response.description,
                "operation": "get_single"
            }
            
            return api_response, response, None
            
        except Exception as err:
            response.data = {
                "message": "Error getting single item",
                "error": str(err)
            }
            response.status = "error"
            return None, response, err


class GetListItemBuilder:
    """GetListItemBuilder - already using ApiResponse correctly"""
    
    def __init__(self, collection: str, config: Config, request: Request):
        self.collection = collection
        self.config = config
        self.request = request
        self._limit = 10
        self._page = 1
    
    def limit(self, limit: int) -> 'GetListItemBuilder':
        if limit <= 0:
            limit = 10
        self._limit = limit
        self.request.data["limit"] = limit
        return self
    
    def page(self, page: int) -> 'GetListItemBuilder':
        if page <= 0:
            page = 1
        self._page = page
        self.request.data["offset"] = (page - 1) * self._limit
        return self
    
    def filter(self, filter_params: Dict[str, Any]) -> 'GetListItemBuilder':
        """Add filter parameters"""
        for key, value in filter_params.items():
            self.request.data[key] = value
        return self
    
    def search(self, search: str) -> 'GetListItemBuilder':
        self.request.data["search"] = search
        return self
    
    def sort(self, sort: Dict[str, Any]) -> 'GetListItemBuilder':
        self.request.data["order"] = sort
        return self
    
    def view_fields(self, fields: List[str]) -> 'GetListItemBuilder':
        self.request.data["view_fields"] = fields
        return self
    
    def with_relations(self, with_: bool) -> 'GetListItemBuilder':
        self.request.data["with_relations"] = with_
        return self
    
    def exec(self) -> Tuple[Optional[ApiResponse], Response, Optional[Exception]]:
        """Execute get list request with standardized response"""
        response = Response(status="done", error="", data={})
        url = f"{self.config.base_url}/v2/items/{self.collection}?from-ofs=true"
        
        try:
            req_object_bytes = json.dumps(self.request.data).encode('utf-8')
        except Exception as err:
            response.status = "error"
            response.data = {"message": "Error marshalling request", "error": str(err)}
            return None, response, err
        
        # Ensure pagination defaults
        if self._page <= 0:
            self._page = 1
        if self._limit <= 0:
            self._limit = 10
        
        encoded_data = quote(req_object_bytes.decode('utf-8'))
        url = f"{url}&data={encoded_data}&offset={(self._page-1)*self._limit}&limit={self._limit}"
        
        app_id = self.config.app_id
        headers = {
            "authorization": "API-KEY",
            "X-API-KEY": app_id,
        }
        
        try:
            response_bytes = do_request(
                url=url,
                method="GET",
                body=None,
                headers=headers
            )
            
            # Parse response using standardized ApiResponse
            api_response = ApiResponse.from_bytes(response_bytes)
            
            response.data = {
                "status": api_response.status,
                "description": api_response.description,
                "operation": "get_list"
            }
            
            return api_response, response, None
            
        except Exception as err:
            response.data = {
                "message": "Error getting list",
                "error": str(err)
            }
            response.status = "error"
            return None, response, err


class GetListAggregationBuilder:
    """
    GetListAggregationBuilder class - equivalent to GetListAggregation struct operations in Go.
    """
    
    def __init__(self, collection: str, config: Config, request: Request):
        """
        Initialize GetListAggregationBuilder.
        
        Args:
            collection: Collection/table name
            config: SDK configuration
            request: Request object with aggregation data
        """
        self.collection = collection
        self.config = config
        self.request = request
    
    def exec_aggregation(self) -> Tuple[GetListAggregationClientApiResponse, Response, Exception]:
        """
        Execute aggregation request.
        
        Returns:
            Tuple of (GetListAggregationClientApiResponse, Response, Exception)
        """
        from .helper import do_request
        
        response = Response(status="done", error="", data={})
        url = f"{self.config.base_url}/v2/items/{self.collection}/aggregation"
        
        app_id = self.config.app_id
        headers = {
            "authorization": "API-KEY",
            "X-API-KEY": app_id,
        }
        
        try:
            get_list_aggregation_response_bytes = do_request(
                url=url,
                method="POST",
                body=self.request,
                headers=headers
            )
            
            get_list_aggregation_dict = json.loads(get_list_aggregation_response_bytes.decode('utf-8'))
            get_list_aggregation = GetListAggregationClientApiResponse(**get_list_aggregation_dict)
            
            return get_list_aggregation, response, None
            
        except Exception as err:
            response.data = {
                "description": str(get_list_aggregation_response_bytes) if 'get_list_aggregation_response_bytes' in locals() else "",
                "message": "Can't sent request",
                "error": str(err)
            }
            response.status = "error"
            return GetListAggregationClientApiResponse(), response, err

# Export all builders
__all__ = [
    'CreateItemBuilder',
    'UpdateItemBuilder', 
    'DeleteItemBuilder',
    'GetSingleItemBuilder',
    'GetListItemBuilder'
]