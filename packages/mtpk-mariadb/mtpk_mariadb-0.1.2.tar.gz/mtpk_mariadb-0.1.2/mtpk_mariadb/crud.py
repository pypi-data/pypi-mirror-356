#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
# --------------------------
# Creado 01-06-2025
# jjandres 2025
# --------------------------
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
# pylint: disable=too-many-lines
# pylint: disable=broad-except


from typing import Any, Optional, Tuple
from .core_sync import Tabla
from .async_adapter import AsyncDatabase
from .utils import construir_condiciones_sql, resolver_orden_sql
from .excepciones import MtpkErrorValidacionDb, MtpkErrorDb
import uuid

class AsyncCrudBase:
    def __init__(self, tabla: Tabla, config: dict, logger: Optional[Any] = None):
        """
        Inicializa una instancia CRUD para la tabla especificada.

        Args:
            tabla (Tabla): Objeto de definición de tabla.
            config (dict): Configuración de conexión a la base de datos.
        """
        self.tabla = tabla
        self.config = config
        self.logger = logger

    async def _inst_db_si_necesario(self, db: Optional[AsyncDatabase]) -> AsyncDatabase:
        """
        Si `db` ya es una instancia AsyncDatabase, lo reutiliza.
        Si no, la crea para usar la tabla actual.
        La conexión no se establece aquí, solo se registra la tabla.
        Args:
            db (Optional[AsyncDatabase]): Instancia AsyncDatabase existente o None.

        Returns:
            AsyncDatabase: Instancia AsyncDatabase con la tabla registrada.
        """
        if db is not None:
            return db
        db = AsyncDatabase(**self.config)
        db.add_tabla(self.tabla)
        return db

    async def insertar(self, datos: dict, aplicar_protegidos: bool = False, db: Optional[AsyncDatabase] = None, conexion: Any = None) -> int:
        """
        Inserta un nuevo registro en la tabla.

        Args:
            db (Optional[AsyncDatabase]): Conexión activa o None.
            datos (dict): Datos a insertar.
            aplicar_protegidos (bool): Si se deben excluir columnas protegidas.
            conexion (Any): Conexión reutilizable, si aplica.

        Returns:
            int: ID del nuevo registro insertado.
        """
        try:
            db = await self._inst_db_si_necesario(db)
            campos_validos = {
                col.nombre for col in self.tabla.columnas
                if not (aplicar_protegidos and getattr(col, "protegido_insertar", False))
            }
            datos_filtrados = {k: v for k, v in datos.items() if k in campos_validos}
            columnas = ", ".join(f"`{k}`" for k in datos_filtrados)
            valores = ", ".join(["%s"] * len(datos_filtrados))
            sql = f"INSERT INTO `{self.tabla.nombre}` ({columnas}) VALUES ({valores})"
            await db.query(sql, tuple(datos_filtrados.values()), conexion=conexion)
            return db.ultimo_insert_id
        
        except Exception as e:
            identificador = str(uuid.uuid4())
            raise MtpkErrorDb("Error insertando registro", identificador, logger=self.logger) from e

    async def actualizar(self, id: int, datos: dict, aplicar_protegidos: bool = False, db: Optional[AsyncDatabase] = None, conexion: Any = None) -> int:
        """
        Actualiza un registro por ID.

        Args:
            id (int): ID del registro a actualizar.
            datos (dict): Campos a modificar.
            aplicar_protegidos (bool): Si se deben excluir columnas protegidas.
            db (Optional[AsyncDatabase]): Conexión activa o None.
            conexion (Any): Conexión reutilizable, si aplica.

        Returns:
            int: Número de filas afectadas.
        """
        try:
            db = await self._inst_db_si_necesario(db)
            campos_validos = {
                col.nombre for col in self.tabla.columnas
                if not (aplicar_protegidos and getattr(col, "protegido_actualizar", False))
            }
            datos_filtrados = {k: v for k, v in datos.items() if k in campos_validos}
            asignaciones = ", ".join(f"`{k}` = %s" for k in datos_filtrados)
            sql = f"UPDATE `{self.tabla.nombre}` SET {asignaciones} WHERE id = %s"
            num_filas = await db.query(sql, tuple(datos_filtrados.values()) + (id,), conexion=conexion)
            return num_filas
        except Exception as e:
            identificador = str(uuid.uuid4())
            raise MtpkErrorDb("Error actualizando registro", identificador, logger=self.logger) from e
            
            
    async def eliminar(self, id: int,  db: Optional[AsyncDatabase] = None, conexion: Any = None) -> int:
        """
        Elimina un registro por ID.

        Args:
            db (Optional[AsyncDatabase]): Conexión activa o None.
            id (int): ID del registro a eliminar.
            conexion (Any): Conexión reutilizable, si aplica.

        Returns:
            int: Número de filas eliminadas.
        """
        try:
            db = await self._inst_db_si_necesario(db)
            sql = f"DELETE FROM `{self.tabla.nombre}` WHERE id = %s"
            num_filas = await db.query(sql, (id,), conexion=conexion)
            return num_filas
        except Exception as e:
            identificador = str(uuid.uuid4())
            raise MtpkErrorDb("Error eliminando registro", identificador, logger=self.logger) from e
            
            
    async def obtener(self, id: Any, alias: Optional[dict[str, str]] = None, db: Optional[AsyncDatabase] = None, conexion: Any = None) -> Optional[dict]:
        """
        Obtiene un registro por su ID.

        Args:
            `db` (Optional[AsyncDatabase]): Conexión activa o None.
            `id` (Any): ID del registro a buscar.
            `conexion` (Any): Conexión reutilizable, si aplica.
            `alias`     (Optional[dict[str, str]]): Alias SQL por campo.

        Returns:
            Optional[dict]: Registro encontrado o None si no existe.
        """
        try:
            db = await self._inst_db_si_necesario(db)
            sql = f"SELECT * FROM `{self.tabla.nombre}` WHERE id = %s"
            return await db.query(sql, (id,), uno=True, conexion=conexion)
        
        except Exception as e:
            identificador = str(uuid.uuid4())
            if self.logger:
                self.logger.error("%s] Error obteniendo registro: %s", identificador, e, exc_info=True)
            raise MtpkErrorDb("Error al obtener registro", identificador, logger=self.logger) from e

    async def listar(self, offset: int = 0, limit: int = 100, orden: str = "id ASC", filtros: Optional[dict] = None, alias: Optional[dict[str, str]] = None, db: Optional[Any] = None, conexion: Any = None) -> Tuple[list[dict], int]:
        """
        Lista registros aplicando filtros, alias, ordenación y paginación.

        Args:
            `offset`    (int): Desplazamiento inicial.
            `limit`     (int): Número máximo de registros a devolver.
            `orden`     (str): Orden SQL, como "a.nombre DESC", por defecto "id ASC".
            `filtros`   (Optional[dict]): Diccionario con condiciones de filtrado.
            `alias`     (Optional[dict[str, str]]): Alias SQL por campo.
            `db`        (Optional[AsyncDatabase]): Conexión existente, si aplica.
            `conexion`  (Any): Conexión interna reutilizable.

        Returns:
            Tuple[list[dict], int]: Lista de registros y total de registros sin paginar.
        """
        try:
            db = await self._inst_db_si_necesario(db)
            condiciones_sql, valores = construir_condiciones_sql(filtros or {}, alias)
            orden_sql = resolver_orden_sql(orden, alias)
            
            where_sql = f"WHERE {condiciones_sql}" if condiciones_sql else ""

            sql_base = f"""
                SELECT * FROM `{self.tabla.nombre}`
                {where_sql}
            """

            sql_final = f"""{sql_base} ORDER BY {orden_sql} LIMIT %s OFFSET %s"""

            valores_total = valores.copy()
            valores += [limit, offset]
            filas = await db.query(sql_final, valores, conexion=conexion)

            total = len(filas)
            if total == limit:
                sql_total = f"SELECT COUNT(*) as total FROM ({sql_base}) as subquery"
                resultado = await db.query(sql_total, valores_total, uno=True, conexion=conexion)
                total = resultado.get("total", total)

            return filas, total
        
        except Exception as e:
            identificador = str(uuid.uuid4())
            raise MtpkErrorDb("Error al obtener registro", identificador, logger=self.logger) from e
