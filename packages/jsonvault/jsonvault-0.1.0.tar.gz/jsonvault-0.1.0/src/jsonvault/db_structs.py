from io import TextIOWrapper
from typing import List, Dict, Type, Any
from . import io
import json

class DataNotExist(Exception):
    ...

class DuplicateData(Exception):
    ...

class MetadataError(Exception):
    ...

class JSONDB: # Handle db operations
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.f: TextIOWrapper = self.open()
        self.data = DBData(json.loads(self.f.read())["Data"]) 
        self.metadata = DBMeta(json.loads(self.f.read())["Meta"]) 

    def get(self, key, default=None):
        return self.data.get(key, default) 

    def add(self, key, value):
        try:
            self.data.add(key, value) 
        except DuplicateData as e: 
            raise e

    def update(self, key, value):
        try:
            self.data.update(key, value) 
        except DataNotExist as e: 
            raise e

    def delete(self, key):
        try:
            self.data.delete(key) 
        except DataNotExist as e: 
            raise e

    def meta_get(self, key, default=None):
        return self.metadata.get(key, default)
    
    def open(self):
        return io._open(self.file_path)
    
    def close(self):
        return io.close(self.f)
    
    def flush(self):
        dt = {
            "Data": self.data,
            "Meta": self.metadata
        }
        self.f.write(json.dumps(dt))
        self.f.flush()


class DBTypes: # Handle database entry types
    # Each type entry is of the form:
    # types[key] = List[Type]

    def __init__(self) -> None:
        self.types: Dict[str, List[Type]] = {}

    def __entry_val_type(self, key: str):
        return self.types[key]
    
    def __add_val_type(self, key: str, rtype: Type):
        if rtype in self.types[key]:
            return
        self.types[key].append(rtype) # Because each types entry is mapped to a List

    def __update_val_type(self, key: str, rtype: Type, *, removeOldType = True, oldType: Type):
        if removeOldType:
            self.types[key].remove(oldType)
        self.types[key].append(rtype)


class DBData:
    # data is of the form:
    # {
    #    "key": <key>,
    #    "value": <value>
    # }
    def __init__(self, data: Dict[str, Any] = {}):
        self.data = data
        self.types = self.__load_types()

    def __load_types(self):
        types: DBTypes = DBTypes()
        for i in self.data:
            types.__add_val_type(i, type(self.data[i]))
        return types
    
    def get(self, key: str, default: Any = None):
        if key in self.data.keys():
            return self.data[key]
        return default
    
    def add(self, key: str, value: Any):
        if self.get(key):
            raise DuplicateData(f"Cannot add to db. Reason: {key} exists")
        self.data[key] = value
        self.types.__add_val_type(key, type(value))

    def update(self, key: str, value: Any):
        if key in self.data.keys():
            otype = type(self.get(key))
            self.data[key] = value
            self.types.__update_val_type(key, type(value), oldType=otype, removeOldType=True)
        else:
            raise DataNotExist("Data requested for update does not exist in DB.")

    def delete(self, key: str):
        if self.get(key):
            del self.data[key]
        else:
            raise DataNotExist("Data requested for deletion is not present")

    def export(self):
        return self.data


class DBMeta:
    def __init__(self, data: Dict[str, Any] = {}):
        self.data = data if data != {} else { "count": 0 }
        self.validate_data()

    def validate_data(self):
        if self.data == {}: 
            return
        
        if 'count' not in self.data:
            raise MetadataError("Total number of records not in database metadata")
        
    def update_count(self, record_count: int):
        self.data['count'] = record_count

    def get(self, key: str, default: Any = None):
        if not key in self.data.keys():
            return default
        return self.data[key]