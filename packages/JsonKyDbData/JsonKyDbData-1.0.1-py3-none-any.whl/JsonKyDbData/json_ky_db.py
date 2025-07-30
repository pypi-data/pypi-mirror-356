# -*- coding: gbk -*-
import json
from typing import Dict, List, Optional, Any


class JsonKVDB:
    def __init__(self, file_path: str, key_field: str = "id"):
        """
        :param file_path: JSON File Path
        :param key_field: The field name used as a keyword (default is 'id')
        """
        self.file_path = file_path
        self.key_field = key_field
        self._init_storage()

    def _init_storage(self):
        """Initialize storage files"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
                if not isinstance(self.data, dict):
                    raise ValueError("Invalid JSON format")
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {"records": [], "index": {}}
            self._save_data()

    def _save_data(self):
        """Save data to file"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def _update_index(self, record: Dict):
        """Update keyword index"""
        if self.key_field in record:
            key_value = str(record[self.key_field])
            self.data["index"][key_value] = len(self.data["records"]) - 1

    def insert(self, record: Dict) -> str:
        """
        Insert new record
        :return: Generated keyword values
        """
        if self.key_field not in record:
            raise KeyError(f"Required field '{self.key_field}' missing")

        key_value = str(record[self.key_field])
        if key_value in self.data["index"]:
            raise ValueError(f"Key '{key_value}' already exists")

        self.data["records"].append(record)
        self._update_index(record)
        self._save_data()
        return key_value

    def get(self, key_value: str) -> Optional[Dict]:
        """Search records based on keywords"""
        idx = self.data["index"].get(str(key_value))
        return self.data["records"][idx] if idx is not None else None

    def update(self, key_value: str, new_data: Dict) -> bool:
        """Update records for specified keywords"""
        idx = self.data["index"].get(str(key_value))
        if idx is None:
            return False

        # 保留原关键字值
        if self.key_field in new_data:
            del new_data[self.key_field]

        self.data["records"][idx].update(new_data)
        self._save_data()
        return True

    def delete(self, key_value: str) -> bool:
        """Delete records of specified keywords"""
        idx = self.data["index"].pop(str(key_value), None)
        if idx is None:
            return False

        self.data["records"].pop(idx)
        # rebuild index
        self.data["index"] = {
            str(r[self.key_field]): i
            for i, r in enumerate(self.data["records"])
        }
        self._save_data()
        return True

    def query_by_condition(self, condition_func) -> List[Dict]:
        """Conditional query of all records that meet the conditions"""
        return [r for r in self.data["records"] if condition_func(r)]

    def query_by_index(self) -> List[Dict]:
        """Search for all keywords"""
        return [r for r in self.data['index']]
