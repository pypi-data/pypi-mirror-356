from pathlib import Path
from importlib import import_module
from typing import Dict, Type, Optional, List, Tuple
from difflib import get_close_matches
from loguru import logger
from .base import BaseSchema

class SchemaRegistry:
    _instance = None
    _schemas: Dict[str, Type[BaseSchema]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._load_schemas()
        return cls._instance

    @classmethod
    def _load_schemas(cls):
        schemas_dir = Path(__file__).parent
        for file_path in schemas_dir.glob("*.py"):
            if file_path.stem in ("__init__", "base", "registry"):
                continue
            try:
                module_name = f"{__package__}.{file_path.stem}"
                import_module(module_name)
            except Exception as e:
                print(f"Warning: Failed to load schema module {file_path.stem}: {e}")

    @classmethod
    def register(cls, name: str):
        def decorator(schema_class: Type[BaseSchema]):
            cls._schemas[name] = schema_class
            return schema_class
        return decorator

    @classmethod
    def _normalize_name(cls, name: str) -> str:
        """Normalize schema name for comparison"""
        if not name:
            return ""
        return name.strip().lower().replace(" ", "_").replace("-", "_")
        
    @classmethod
    def get_schema_class(cls, name: str) -> Tuple[Optional[Type[BaseSchema]], str]:
        """
        Get schema class by name with fuzzy matching
        
        Args:
            name: Schema name to look up
            
        Returns:
            Tuple of (schema_class, matched_name) where matched_name is the actual schema name that was matched
        """
        if not name:
            return None, ""
            
        # Try exact match first (case-insensitive)
        normalized_name = cls._normalize_name(name)
        for schema_name, schema_class in cls._schemas.items():
            if cls._normalize_name(schema_name) == normalized_name:
                return schema_class, schema_name
                
        # Try with common suffixes if no exact match
        for suffix in ["_schema", "_form", ""]:
            test_name = normalized_name
            if suffix and not test_name.endswith(suffix):
                test_name = f"{test_name}{suffix}"
            for schema_name, schema_class in cls._schemas.items():
                if cls._normalize_name(schema_name) == test_name:
                    return schema_class, schema_name
        
        # Try fuzzy matching as last resort
        all_names = [cls._normalize_name(n) for n in cls._schemas.keys()]
        matches = get_close_matches(normalized_name, all_names, n=1, cutoff=0.6)
        if matches:
            matched_name = next((n for n in cls._schemas.keys() 
                              if cls._normalize_name(n) == matches[0]), None)
            if matched_name:
                return cls._schemas[matched_name], matched_name
                
        return None, ""
        
    @classmethod
    def get_schema_class_with_fallback(cls, name: str, default: str = "GENERIC") -> Type[BaseSchema]:
        """
        Get schema class with fallback to default if not found
        
        Args:
            name: Schema name to look up
            default: Default schema name if not found
            
        Returns:
            Schema class (never None)
        """
        schema_class, matched_name = cls.get_schema_class(name)
        if schema_class is None:
            logger.warning(f"Schema '{name}' not found, falling back to '{default}'")
            schema_class, _ = cls.get_schema_class(default)
            if schema_class is None:
                raise ValueError(f"Default schema '{default}' not found in registry")
        return schema_class

    @classmethod
    def list_schemas(cls) -> Dict[str, str]:
        """List all registered schemas with their source locations"""
        return {
            name: f"{cls.get_schema_source(schema)} (aliases: {', '.join(cls._get_aliases(name))})"
            for name, schema in cls._schemas.items()
        }
        
    @classmethod
    def _get_aliases(cls, name: str) -> List[str]:
        """Get all aliases for a schema name"""
        normalized = cls._normalize_name(name)
        return [n for n in cls._schemas.keys() 
                if n != name and cls._normalize_name(n) == normalized]

    @staticmethod
    def get_schema_source(schema_class: Type[BaseSchema]) -> str:
        return f"{schema_class.__module__}.{schema_class.__name__}"
