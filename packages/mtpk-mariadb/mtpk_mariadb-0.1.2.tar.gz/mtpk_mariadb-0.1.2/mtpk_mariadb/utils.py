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
 

import bcrypt
from typing import Optional, List, Dict, Any, Union, Literal
from .core_sync import Columna  # o el path correcto según tu proyecto
from pydantic import BaseModel

def hash_password(plain_password: str) -> str:
    """
    Genera un hash seguro de una contraseña en texto plano.

    Args:
        plain_password (str): Contraseña original en texto plano.

    Returns:
        str: Hash seguro (en formato string) listo para almacenar en la base de datos.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode(), salt)
    return hashed.decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash almacenado.

    Args:
        plain_password (str): Contraseña introducida por el usuario.
        hashed_password (str): Hash previamente almacenado.

    Returns:
        bool: True si coinciden, False si no.
    """
    return bcrypt.checkpw(
        plain_password.encode(), 
        hashed_password.encode()
    )


def generar_lista_campos(campos, alias=None, excluir=None, prefijo_alias=None):
    """
    Genera una lista de campos SQL a partir de un diccionario, lista de strings o lista de objetos Columna,
    con alias opcional, campos a excluir y alias renombrado con prefijo.

    :param `campos`:           (Requerido) Diccionario {nombre_campo: Column}, lista de strings o lista de objetos Columna
    :param `alias`:            (Opcional) Alias para los campos (string), ej: 'u'
    :param `excluir`:          (Opcional) Lista de campos a excluir (lista de strings)
    :param `prefijo_alias`:    (Opcional) Prefijo para renombrar los campos con alias: <alias>.<campo> AS <prefijo><campo>
    :return:                   String con lista de campos separados por coma
    """
    excluir = excluir or []
    lista = []

    if isinstance(campos, dict):
        iterable = campos.items()
    elif isinstance(campos, list):
        if all(hasattr(col, 'nombre') for col in campos):
            iterable = [(col.nombre, col) for col in campos]
        else:
            iterable = [(nombre, None) for nombre in campos]
    else:
        raise TypeError("El parámetro 'campos' debe ser un dict, una lista de strings o una lista de objetos Columna.")

    for nombre, _ in iterable:
        if nombre in excluir:
            continue
        if alias:
            campo_sql = f"{alias}.{nombre}"
        else:
            campo_sql = nombre

        if prefijo_alias:
            alias_sql = f"{prefijo_alias}{nombre}"
            lista.append(f"{campo_sql} AS {alias_sql}")
        else:
            lista.append(campo_sql)

    return ", ".join(lista)


class FiltroCampo(BaseModel):
    """Crea modelo para definir un filtro de campo SQL."""
    op: Literal["=", "!=", ">", "<", ">=", "<=", "like", "in", "between"]
    valor: Any
    
def construir_condiciones_sql(filtros: dict[str, dict[str, Union[str, Any]]], alias: Optional[dict[str, str]] = None) -> tuple[str, list[Any]]:
    """
    Construye una cláusula WHERE SQL a partir de un diccionario de filtros.

    Cada entrada del diccionario debe tener la forma:
        campo: {"op": operador_sql, "valor": valor_o_lista}

    Operadores soportados:
        '=', '!=', '>', '<', '>=', '<=', 'like', 'in', 'between'

    Parámetros:
        - `filtros`:    Diccionario de filtros con campo, operador y valor, según se detalla en la descripción.
        - `alias`:      Diccionario opcional con alias por campo, por ejemplo {'nombre': 'a.nombre'}

    Returns:
        - Una tupla (condiciones_sql, valores) donde:
            - condiciones_sql: str con la cláusula WHERE sin "WHERE" inicial.
            - valores: lista de parámetros a enlazar en la consulta.
    """
    condiciones = []
    valores = []

    for campo, cond in filtros.items():
        if not isinstance(cond, dict):
            continue

        op = cond.get("op")
        val = cond.get("valor")
        campo_sql = alias.get(campo, campo) if alias else campo

        if op == "in":
            if not isinstance(val, list) or not val:
                continue
            placeholders = ', '.join(['%s'] * len(val))
            condiciones.append(f"{campo_sql} IN ({placeholders})")
            valores.extend(val)

        elif op == "between":
            if not isinstance(val, list) or len(val) != 2:
                continue
            condiciones.append(f"{campo_sql} BETWEEN %s AND %s")
            valores.extend(val)

        elif op == "like":
            condiciones.append(f"{campo_sql} LIKE %s")
            valores.append(val)

        elif op in {"=", "!=", ">", "<", ">=", "<="}:
            condiciones.append(f"{campo_sql} {op} %s")
            valores.append(val)

        else:
            continue  # Operador no soportado

    condiciones_sql = " AND ".join(condiciones)
    return condiciones_sql, valores

def resolver_orden_sql(orden: str, alias: Optional[dict[str, str]] = None) -> str:
    """
    Convierte una cadena de orden (como 'nombre DESC') en una cláusula SQL segura,
    aplicando alias si están definidos.

    Ejemplo:
        orden = "nombre DESC"
        alias = {"nombre": "a.nombre"}
        => "a.nombre DESC"

    Si el campo no está en alias, se usa tal cual (bajo tu responsabilidad).

    Args:
        orden (str): Campo o campos por los que ordenar, separados por coma.
        alias (dict[str, str], optional): Diccionario de alias.

    Returns:
        str: Expresión segura de ordenación SQL.
    """
    if not orden:
        return ""

    campos_orden = []
    for parte in orden.split(","):
        tokens = parte.strip().split()
        campo = tokens[0]
        direccion = tokens[1].upper() if len(tokens) > 1 and tokens[1].upper() in {"ASC", "DESC"} else "ASC"

        campo_sql = alias.get(campo, campo) if alias else campo
        campos_orden.append(f"{campo_sql} {direccion}")

    return ", ".join(campos_orden)