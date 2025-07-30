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


# Esta librería es un wrapper (envolvente) del conector pymysql para menjo de Mariadb con funciones asíncronas.

import aiomysql
from typing import Optional, Union, List, Dict
from .core_sync import Tabla, SQLLiteral
from logging import Logger
from contextlib import asynccontextmanager

class AsyncDatabase:
    """
    Clase AsyncDatabase para entornos asíncronos como FastAPI con Uvicorn.
    Usa aiomysql como backend de conexión.
    """

    def __init__(self, host: str, user: str, password: str, db: str, port: int = 3306, logger: Optional[Logger] = None):
        """
        Inicializa la configuración de conexión.

        - Args:
            - `host`      (str): Dirección del servidor de base de datos.
            - `user`      (str): Usuario.
            - `password`  (str): Contraseña.
            - `db`        (str): Nombre de la base de datos.
            - `port`      (int): Puerto de conexión (default 3306).
            - `logger`    (Logger, opcional): Logger para eventos e informes.
        """
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.logger = logger
        self.pool = None
        self.tablas: Dict[str, Tabla] = {}
        self.ultimo_insert_id: Optional[int] = None
    
    @asynccontextmanager
    async def transaccion(self):
        """
        Context manager para ejecutar múltiples operaciones dentro de una transacción.
        """
        await self.conectar()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await conn.begin()
                    yield conn
                    await conn.commit()
                except Exception as e:
                    await conn.rollback()
                    raise e
                
                
    async def conectar(self):
        """
        Crea un pool de conexiones asíncronas si no está ya activo.
        """
        if self.pool is None:
            self.pool = await aiomysql.create_pool(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db,
                port=self.port,
                autocommit=False
            )

    async def cerrar(self):
        """
        Cierra el pool de conexiones si está abierto.
        """
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None

    def add_tabla(self, tabla: Tabla):
        """
        Añade un objeto `Tabla` a la base de datos.

        - Args:
            - `tabla` (Tabla): Objeto que representa una tabla definida por el usuario.
        """
        self.tablas[tabla.nombre] = tabla
        tabla.set_database(self)

    def get_tabla(self, nombre: str) -> Tabla:
        """
        Recupera una tabla registrada por su nombre.

        - Args:
            `nombre` (str): Nombre de la tabla.

        Returns:
            Tabla: Objeto de tabla registrada.
        """
        if nombre not in self.tablas:
            raise KeyError(f"La tabla '{nombre}' no está registrada.")
        return self.tablas[nombre]

    async def query(self, sql: str, params=None, conexion=None, uno: bool = False):
        """
        Ejecuta una consulta SQL, detectando automáticamente si es de lectura o acción.

        - Args:
            - `sql`         (str): Consulta SQL.
            - `params`      (tuple o dict, opcional): Parámetros para la consulta.
            - `conexion`    (aiomysql.Connection, opcional): Conexión externa si se desea controlar la transacción.
            - `uno` (bool): Si True, se espera un único resultado (SELECT).

        Returns:
            List[Dict] si es SELECT, o int si es acción (nº de filas afectadas).
        """
        comando = sql.strip().split()[0].upper()
        if comando in {"SELECT", "SHOW", "DESC", "DESCRIBE", "EXPLAIN"}:
            return await self._query_select(sql, params, conexion, uno)
        else:
            return await self._query_accion(sql, params, conexion)
    
    
        
    async def _query_select(self, sql: str, params=None, conexion=None, uno: bool = False) -> List[Dict]:
        """
        Ejecuta una consulta de lectura (SELECT, SHOW, DESC...).

        - Args:
            - `sql`         (str): Consulta SQL de lectura.
            - `params`      (tuple o dict, opcional): Parámetros de la consulta.
            - `conexion`    (aiomysql.Connection, opcional): Conexión a reutilizar si se gestiona externamente.
            - `uno`         (bool): Si True, se espera un único resultado.

        Returns:
            List[Dict]: Lista de resultados como diccionarios.
        """
        propia = False
        if conexion is None:
            await self.conectar()
            conexion = await self.pool.acquire()
            propia = True

        try:
            async with conexion.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(sql, params)
                if uno:
                    return await cursor.fetchone()
                return await cursor.fetchall()
        finally:
            if propia:
                self.pool.release(conexion)

    async def _query_accion(self, sql: str, params=None, conexion=None) -> int:
        """
        Ejecuta una acción de escritura (INSERT, UPDATE, DELETE, etc.).
        Guarda `ultimo_insert_id` si aplica.

        - Args:
            - `sql`         (str): Sentencia SQL.
            - `params`      (tuple o dict, opcional): Parámetros de la consulta.
            - `conexion`    (aiomysql.Connection, opcional): Conexión a reutilizar.

        Returns:
            int: Número de filas afectadas por la operación.
        """
        propia = False
        if conexion is None:
            await self.conectar()
            conexion = await self.pool.acquire()
            propia = True

        try:
            async with conexion.cursor() as cursor:
                filas = await cursor.execute(sql, params)
                self.ultimo_insert_id = cursor.lastrowid
                if propia:
                    await conexion.commit()
                return filas
        except Exception as e:
            if propia:
                await conexion.rollback()
            if self.logger:
                self.logger.error(f"Error en _query_accion: {e}")
            raise
        finally:
            if propia:
                self.pool.release(conexion)
