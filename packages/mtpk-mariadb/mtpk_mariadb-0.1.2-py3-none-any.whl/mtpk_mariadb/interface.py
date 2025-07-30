#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
# ----------------------------------------
# jjandres 2025 - 17-05-2025)
# ----------------------------------------
# pylint: disable=multiple-imports
# pylint: disable=line-too-long
# pylint: disable=trailing-whitespace
# pylint: disable=wrong-import-position
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=unused-argument
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=unused-variable
# pylint: disable=bare-except
# pylint: disable=protected-access
# pylint: disable=ungrouped-imports
# pylint: disable=wrong-import-order
# pylint: disable=redefined-builtin
# pylint: disable=unidiomatic-typecheck
# pylint: disable=singleton-comparison
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-lines
# pylint: disable=anomalous-backslash-in-string
# pylint: disable=broad-except
# pylint: disable=too-many-arguments
# pylint: disable=broad-exception-raised
# pylint: disable=consider-using-f-string
# 
# 

from typing import TYPE_CHECKING
import asyncio
from importlib import import_module
from .core_sync import SQLLiteral 

# Solo para análisis de tipos
if TYPE_CHECKING:
    from .core_sync import Tabla, Database, Columna, ForeignKey, Index
    
# Importa ambos backends
_sync = import_module("mtpk_mariadb.core_sync")
_async = import_module("mtpk_mariadb.async_adapter")


# Modo por defecto
DEFAULT_ASYNC_MODE = False

def set_async_mode(value: bool):
    """Permite cambiar dinámicamente el modo por defecto (por código o startup FastAPI).""" 
    global DEFAULT_ASYNC_MODE # pylint: disable=global-statement
    DEFAULT_ASYNC_MODE = value

def is_async_context():
    """Detecta si estamos dentro de un bucle async activo."""
    try:
        return asyncio.current_task() is not None
    except RuntimeError:
        return False

def resolve_backend(async_mode=None):
    """Decide qué backend usar."""
    if async_mode is None:
        async_mode = DEFAULT_ASYNC_MODE or is_async_context()
    return _async if async_mode else _sync

# Fábricas para clases
def get_Tabla(async_mode=None): 
    return resolve_backend(async_mode).Tabla

def get_Columna(async_mode=None): 
    return resolve_backend(async_mode).Columna

def get_ForeignKey(async_mode=None): 
    return resolve_backend(async_mode).ForeignKey

def get_Index(async_mode=None): 
    return resolve_backend(async_mode).Index

def get_Database(async_mode=None): 
    return resolve_backend(async_mode).Database

# Exposición por defecto usando el backend predeterminado (útil para autocompletado)
Tabla = get_Tabla()
Columna = get_Columna()
ForeignKey = get_ForeignKey()
Index = get_Index()
Database = get_Database()

__all__ = [
    "Tabla", "Columna", "ForeignKey", "Index", "Database",
    "get_Tabla", "get_Columna", "get_ForeignKey", "get_Index", "get_Database",
    "set_async_mode", "is_async_context", "SQLLiteral"
]
