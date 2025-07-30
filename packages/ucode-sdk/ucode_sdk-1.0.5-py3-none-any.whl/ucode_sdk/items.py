"""
UCode Python SDK - Items Module

This module provides CRUD operations for items/objects,
equivalent to items.go in the original Go SDK.
"""

import json
from typing import Dict, List, Any, Tuple, Protocol
from urllib.parse import quote
from .models import (
    ActionBody, Request, Response, ClientApiResponse,
)
from .builders import CreateItemBuilder, UpdateItemBuilder, DeleteItemBuilder, GetListItemBuilder, GetSingleItemBuilder
from .config import Config
from .helper import do_request

class ItemsI(Protocol):
    """
    ItemsI interface - equivalent to ItemsI interface in Go.
    Items interface defines methods related to item operations.
    """
    
    def create(self, data: Dict[str, Any]) -> 'CreateItemBuilder':
        """
        CreateObject is a function that creates new object.

        User disable_faas(False) method to enable faas: default True

        Works for [Mongo, Postgres]
        """
        ...
    
    def update(self, data: Dict[str, Any]) -> 'UpdateItemBuilder':
        """
        UpdateObject is a function that updates specific object or objects

        User disable_faas(False) method to enable faas: default True

        Works for [Mongo, Postgres]
        """
        ...
    
    def delete(self) -> 'DeleteItemBuilder':
        """
        Delete is a function that is used to delete one or multiple object
        User disable_faas(False) method to enable faas: default True
        map[guid]="actual_guid"

        Works for [Mongo, Postgres]
        """
        ...
    
    def get_list(self) -> 'GetListItemBuilder':
        """
        GetList is function that get list of objects from specific table using filter.

        sdk.items("table_name").get_list().page(1).limit(10).with_relations(True).filter({"field_name": "value"}).exec()
        
        It has three options: exec, exec_slim, exec_aggregation(use with pipelines)
        Exec option works slower because it gets all the information
        about the table, fields and view. User exec_slim for faster response.
        Works for [Mongo, Postgres]
        """
        ...
    
    def get_single(self, id: str) -> 'GetSingleItemBuilder':
        """
        GetSingleSlim is function that get one object with its fields.
        It is light and fast to use.

        guid="your_guid"
        sdk.items("table_name").get_single(guid).exec_slim()
        It has two options: exec, exec_slim

        Works for [Mongo, Postgres]
        """
        ...


class APIItem:
    """
    APIItem class - equivalent to APIItem struct in Go.
    """

    def __init__(self, sdk_instance, collection: str):
        """
        Initialize APIItem with SDK instance and collection name.
        
        Args:
            sdk_instance: The main SDK instance
            collection: Collection/table name
        """
        self.collection = collection
        self.config = sdk_instance.config()
        self._sdk = sdk_instance
        
    def create(self, data: Dict[str, Any]) -> 'CreateItemBuilder':
        """
        CreateObject is a function that creates new object.

        User disable_faas(False) method to enable faas: default True

        Works for [Mongo, Postgres]
        
        Args:
            data: Object data to create
            
        Returns:    
            CreateItemBuilder: Builder for create operation
        """
        return CreateItemBuilder(
            collection=self.collection,
            config=self.config,
            data=ActionBody(body=data, disable_faas=True)
        )
    
    def update(self, data: Dict[str, Any]) -> 'UpdateItemBuilder':
        """
        UpdateObject is a function that updates specific object or objects

        User disable_faas(False) method to enable faas: default True

        Works for [Mongo, Postgres]
        
        Args:
            data: Object data to update
            
        Returns:
            UpdateItemBuilder: Builder for update operation
        """
        return UpdateItemBuilder(
            collection=self.collection,
            config=self.config,
            data=ActionBody(body=data, disable_faas=True)
        )
    
    def delete(self) -> 'DeleteItemBuilder':
        """
        Delete is a function that is used to delete one or multiple object
        User disable_faas(False) method to enable faas: default True
        map[guid]="actual_guid"

        Works for [Mongo, Postgres]
        
        Returns:
            DeleteItemBuilder: Builder for delete operation
        """
        return DeleteItemBuilder(
            collection=self.collection,
            config=self.config,
            disable_faas=True
        )
    
    def get_list(self) -> 'GetListItemBuilder':
        """
        GetList is function that get list of objects from specific table using filter.

        sdk.items("table_name").get_list().page(1).limit(10).with_relations(True).filter({"field_name": "value"}).exec()
        
        It has three options: exec, exec_slim, exec_aggregation(use with pipelines)
        Exec option works slower because it gets all the information
        about the table, fields and view. User exec_slim for faster response.
        Works for [Mongo, Postgres]
        
        Returns:
            GetListItemBuilder: Builder for get list operation
        """
        return GetListItemBuilder(
            collection=self.collection,
            config=self.config,
            request=Request(data={}, is_cached=False)
        )
    
    def get_single(self, id: str) -> 'GetSingleItemBuilder':
        """
        GetSingleSlim is function that get one object with its fields.
        It is light and fast to use.

        guid="your_guid"
        sdk.items("table_name").get_single(guid).exec_slim()
        It has two options: exec, exec_slim

        Works for [Mongo, Postgres]
        
        Args:
            id: Object GUID
            
        Returns:
            GetSingleItemBuilder: Builder for get single operation
        """
        return GetSingleItemBuilder(
            collection=self.collection,
            config=self.config,
            guid=id
        )



# Aliases for compatibility
Items = APIItem
ItemsInterface = ItemsI


__all__ = [
    'ItemsI',
    'APIItem',
    'Items',
    'ItemsInterface',
    'CreateItemBuilder',
    'UpdateItemBuilder',
    'DeleteItemBuilder',
    'DeleteMultipleItemBuilder',
    'GetSingleItemBuilder',
    'GetListItemBuilder',
    'GetListAggregationBuilder'
]