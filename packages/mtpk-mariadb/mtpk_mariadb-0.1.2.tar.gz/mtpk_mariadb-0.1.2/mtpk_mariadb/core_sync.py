#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
# ----------------------------------------
# jjandres 2025 - 13-05-2025)
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


# Esta librería es un wrapper (envolvente) del conector pymysql para menjo de Mariadb


from dataclasses import dataclass, field
from typing import Optional, Union, Literal, List, Dict
import pymysql
import logging
import re
import traceback
from contextlib import contextmanager

@dataclass
class SQLLiteral:
    valor: str
    def __str__(self):
        return self.valor
    
@dataclass
class Columna:
    """
    Representa una columna SQL para crear tablas en MariaDB.
    """

    nombre: str
    """Nombre de la columna"""

    tipo: Literal[
        "TINYINT", "SMALLINT", "MEDIUMINT", "INT", "INTEGER", "BIGINT", "DECIMAL", "NUMERIC", "FLOAT", "DOUBLE",
        "CHAR", "VARCHAR", "TEXT", "TINYTEXT", "MEDIUMTEXT", "LONGTEXT", "BINARY", "VARBINARY", "BLOB", "TINYBLOB", "MEDIUMBLOB", "LONGBLOB",
        "DATE", "TIME", "YEAR", "DATETIME", "TIMESTAMP", "ENUM", "SET", "BOOLEAN", "GEOMETRY", "POINT", "LINESTRING", "POLYGON"
    ]
    """Tipo de dato según MariaDB"""

    longitud: Optional[int] = None
    """Longitud para tipos como VARCHAR(n), CHAR(n), BINARY(n), etc."""

    precision: Optional[int] = None
    """Precisión para DECIMAL(p, s), FLOAT(p), etc."""

    escala: Optional[int] = None
    """Escala para DECIMAL(p, s), opcional"""

    not_null: bool = False
    """Si la columna debe ser NOT NULL"""

    primary_key: bool = False
    """Si esta columna es clave primaria"""

    unique: bool = False
    """Si esta columna tiene restricción UNIQUE"""

    auto_increment: bool = False
    """Si es autoincremental (solo para enteros y claves primarias)"""

    default: Optional[Union[str, int, float, Literal["CURRENT_TIMESTAMP"]]] = None
    """Valor por defecto. Usar CURRENT_TIMESTAMP como literal string si aplica."""

    comentario: Optional[str] = None
    """Comentario SQL para la columna"""

    enum_opciones: Optional[list[str]] = None
    """Lista de valores posibles si tipo es ENUM o SET"""
    
    protegido_insertar: bool = False
    """Si esta columna está protegida contra inserciones (Solo cuando se indique al método CRUB)"""

    protegido_actualizar: bool = False
    """Si esta columna está protegida contra actualizaciones (Solo cuando se indique al método CRUB)"""

    tabla: Optional["Tabla"] = field(default=None, repr=False)

    def to_sql(self) -> str:
        """
        Genera la definición SQL de esta columna.
        """
        partes = [f"`{self.nombre}`"]

        # Tipo + parámetros
        tipo_upper = self.tipo.upper()

        if tipo_upper in {"VARCHAR", "CHAR", "BINARY", "VARBINARY"}:
            partes.append(f"{tipo_upper}({self.longitud})")
        elif tipo_upper in {"DECIMAL", "NUMERIC", "FLOAT", "DOUBLE"}:
            if self.precision is not None and self.escala is not None:
                partes.append(f"{tipo_upper}({self.precision},{self.escala})")
            elif self.precision is not None:
                partes.append(f"{tipo_upper}({self.precision})")
            else:
                partes.append(f"{tipo_upper}")
        elif tipo_upper in {"ENUM", "SET"} and self.enum_opciones:
            opciones = ", ".join(f"'{o}'" for o in self.enum_opciones)
            partes.append(f"{tipo_upper}({opciones})")
        else:
            partes.append(tipo_upper)

        # Modificadores
        if self.auto_increment:
            partes.append("AUTO_INCREMENT")

        partes.append("NOT NULL" if self.not_null or self.primary_key else "NULL")

        if self.default is not None:
            if isinstance(self.default, SQLLiteral):
                partes.append(f"DEFAULT {self.default}")
            elif isinstance(self.default, str) and not self.default.upper().startswith("CURRENT_TIMESTAMP"):
                partes.append(f"DEFAULT '{self.default}'")
            else:
                partes.append(f"DEFAULT {self.default}")

        if self.unique:
            partes.append("UNIQUE")

        if self.primary_key:
            partes.append("PRIMARY KEY")

        if self.comentario:
            partes.append(f"COMMENT '{self.comentario}'")

        return " ".join(partes)


@dataclass
class ForeignKey:
    """
    Representa una clave foránea (FOREIGN KEY) en una tabla SQL.

    - Atributos:
        - `columna`               (str): Nombre de la columna local en esta tabla que actúa como clave foránea.
        - `referencia_tabla`      (str): Nombre de la tabla referenciada.
        - `referencia_columna`    (str): Columna de la tabla referenciada a la que apunta esta clave foránea.
        - `nombre`                (str, opcional): Nombre explícito del constraint. Si no se proporciona, MariaDB generará uno automáticamente.
        - `on_delete`             (str, opcional): Acción a realizar al eliminar la fila referenciada ('CASCADE', 'RESTRICT', 'SET NULL', etc.).
        - `on_update`             (str, opcional): Acción a realizar al actualizar la fila referenciada.
        - `tabla`                 (Tabla, opcional): Referencia a la tabla actual que contiene esta clave. Se asigna automáticamente.
    """
    columna: str
    referencia_tabla: str
    referencia_columna: str
    nombre: Optional[str] = None
    on_delete: Optional[str] = None
    on_update: Optional[str] = None
    tabla: Optional["Tabla"] = field(default=None, repr=False)
        
    def to_sql(self) -> str:
        sql = ""
        if self.nombre:
            sql += f"CONSTRAINT `{self.nombre}` "
        sql += f"FOREIGN KEY (`{self.columna}`) REFERENCES `{self.referencia_tabla}`(`{self.referencia_columna}`)"
        if self.on_delete:
            sql += f" ON DELETE {self.on_delete}"
        if self.on_update:
            sql += f" ON UPDATE {self.on_update}"
        return sql


@dataclass
class Index:
    """
    Representa un índice (normal o único) sobre una o más columnas de una tabla SQL.

    - Atributos:
        - `columnas`    (List[str]): Lista de nombres de columnas incluidas en el índice. Pueden ser una o varias (índice compuesto).
        - `nombre`      (str, opcional): Nombre personalizado del índice. Si no se indica, se generará automáticamente combinando los nombres de las columnas.
        - `unico`       (bool): Indica si el índice es único (`UNIQUE`). Por defecto es `False`.
        - `tabla`       (Tabla, opcional): Referencia a la tabla que contiene este índice. Se asigna automáticamente al añadir el índice a la tabla.
    """
    columnas: List[str]
    nombre: Optional[str] = None
    unico: bool = False
    tabla: Optional["Tabla"] = field(default=None, repr=False)
    
    def to_sql(self) -> str:
        cols = ", ".join(f"`{c}`" for c in self.columnas)
        if self.unico:
            return f"UNIQUE KEY `{self.nombre or '_'.join(self.columnas)}_uk` ({cols})"
        else:
            return f"KEY `{self.nombre or '_'.join(self.columnas)}_idx` ({cols})"


@dataclass
class Tabla:
    """
    Representa la definición estructural de una tabla SQL para MariaDB.

    - Atributos:
        - `nombre`              (str): Nombre de la tabla en la base de datos.
        - `columnas`            (List[Columna]): Lista de objetos `Columna` que definen los campos de la tabla.
        - `indices`             (List[Index]): Lista de índices adicionales (simples o compuestos), excluyendo claves primarias y claves foráneas.
        - `foreign_keys`        (List[ForeignKey]): Lista de claves foráneas que definen relaciones con otras tablas.
        - `claves_primarias`    (List[str]): Lista de nombres de columnas que componen la clave primaria (si es compuesta).
        - `comentario`          (str, opcional): Comentario descriptivo opcional para la tabla.
        - `engine`              (str): Motor de almacenamiento, por defecto `"InnoDB"`.
        - `charset`             (str): Conjunto de caracteres, por defecto `"utf8mb4"`.
        - `registros_iniciales` (Optional[List[Dict[str, Union[str, int, float]]]]): 
                                Lista de diccionarios con registros que deben insertarse automáticamente tras crear la tabla. 
                                Cada diccionario representa un registro, con las claves como nombres de columnas.
        - `vistas`              (Optional[List[str]]): Lista de vistas asociadas a esta tabla, que serán insertadas en la base de datos.
        - `db_name`             (str, opcional): Nombre de la base de datos asociada a esta tabla. Solo se usa para clasificar la tabla y saber a que base de datos pertenece.
        - `database`            (Database, opcional): Referencia a la instancia de `Database` a la que pertenece esta tabla. Se asigna automáticamente al añadir la tabla a una base de datos.
        
    """
    nombre: str
    columnas: List[Columna]
    indices: List[Index] = field(default_factory=list)
    foreign_keys: List[ForeignKey] = field(default_factory=list)
    claves_primarias: List[str] = field(default_factory=list)
    comentario: Optional[str] = None
    engine: str = "InnoDB"
    charset: str = "utf8mb4"
    registros_iniciales: Optional[List[Dict[str, Union[str, int, float]]]] = field(default_factory=list)
    vistas: Optional[List[str]] = field(default_factory=list)
    database: Optional["Database"] = None
    db_name: Optional[str] = None  # ← nuevo campo, sin conflicto con Database
    
    def add_columna(self, columna: Columna):
        """
        Añade una columna a la tabla si no existe ya.

        - Args:
            - `columna` (Columna): Objeto columna a añadir.

        Raises:
            ValueError: Si ya existe una columna con el mismo nombre.
        """
        
        if any(col.nombre == columna.nombre for col in self.columnas):
            raise ValueError(f"La columna '{columna.nombre}' ya está definida en la tabla '{self.nombre}'.")
        columna.tabla = self
        self.columnas.append(columna)
    
    def set_columnas(self, columnas: List[Columna]):
        """
        Reemplaza la lista completa de columnas con una nueva, validando que no haya duplicados.

        - Args:
            - `columnas` (List[Columna]): Lista de objetos Columna.

        Raises:
            ValueError: Si hay columnas con nombres duplicados.
        """
        nombres = [col.nombre for col in columnas]
        duplicados = {nombre for nombre in nombres if nombres.count(nombre) > 1}
        if duplicados:
            raise ValueError(f"Columnas duplicadas encontradas: {', '.join(duplicados)}")
        for col in columnas:
            col.tabla = self
        self.columnas = columnas
    
    def add_index(self, index: Index):
        if any(set(index.columnas) == set(idx.columnas) for idx in self.indices):
            raise ValueError(f"Ya existe un índice para las columnas {index.columnas} en la tabla '{self.nombre}'.")
        index.tabla = self
        self.indices.append(index)

    def set_indices(self, indices: List[Index]):
        seen = set()
        for idx in indices:
            key = tuple(sorted(idx.columnas))
            if key in seen:
                raise ValueError(f"Índice duplicado con columnas: {key}")
            seen.add(key)
            idx.tabla = self
        self.indices = indices
    
    def add_foreign_key(self, fk: ForeignKey):
        if any((fk.columna == f.columna and fk.referencia_tabla == f.referencia_tabla and fk.referencia_columna == f.referencia_columna) for f in self.foreign_keys):
            raise ValueError(f"Ya existe una clave foránea similar en la tabla '{self.nombre}'.")
        fk.tabla = self
        self.foreign_keys.append(fk)
    
    def set_foreign_keys(self, foreign_keys: List[ForeignKey]):
        """
        Asigna la lista completa de claves foráneas, validando duplicados y asignando la tabla padre.

        Args:
            foreign_keys (List[ForeignKey]): Lista de claves foráneas.

        Raises:
            ValueError: Si hay duplicados por columna/referencia.
        """
        claves_unicas = set()
        for fk in foreign_keys:
            clave = (fk.columna, fk.referencia_tabla, fk.referencia_columna)
            if clave in claves_unicas:
                raise ValueError(f"Clave foránea duplicada: {clave}")
            claves_unicas.add(clave)
            fk.tabla = self
        self.foreign_keys = foreign_keys

    
    def set_database(self, db):
        """
        Establece la base de datos a la que pertenece esta tabla.
        """
        self.database = db
        
    def to_sql(self) -> str:
        """
        Genera la sentencia SQL CREATE TABLE IF NOT EXISTS con columnas, índices, claves primarias y foráneas.
        """
        elementos_sql = []

        # Columnas
        for col in self.columnas:
            elementos_sql.append(col.to_sql())

        # Clave primaria compuesta (si no están definidas en las columnas)
        if self.claves_primarias:
            pk = ", ".join(f"`{c}`" for c in self.claves_primarias)
            elementos_sql.append(f"PRIMARY KEY ({pk})")

        # Índices definidos
        for idx in self.indices:
            elementos_sql.append(idx.to_sql())

        # Claves foráneas
        for fk in self.foreign_keys:
            elementos_sql.append(fk.to_sql())

        cuerpo = ",\n  ".join(elementos_sql)
        comentario_sql = f" COMMENT='{self.comentario}'" if self.comentario else ""

        # print(f"[DEBUG] claves_primarias en {self.nombre} = {self.claves_primarias}")  #@log


        return (
            f"CREATE TABLE IF NOT EXISTS `{self.nombre}` (\n"
            f"  {cuerpo}\n"
            f") ENGINE={self.engine} DEFAULT CHARSET={self.charset}{comentario_sql};"
    )


    def extraer_longitud_campo(self, tipo_sql: str) -> Optional[int]:
        """Extrae la longitud de un tipo SQL como VARCHAR(255) o DECIMAL(10,2).
            Función auxiliar para sacar la longitud del tipo si viene con paréntesis, por ejemplo:
            'VARCHAR(100)' → 100
            'DECIMAL(10,2)' → 10
        Args:
            - `tipo_sql` (str): Tipo SQL con o sin longitud.
        Returns:
            Optional[int]: Longitud extraída o None si no se puede determinar.
        """
        if "(" in tipo_sql:
            try:
                return int(tipo_sql.split("(")[1].split(")")[0].split(",")[0])
            except:
                return None
        return None
    
    def obtener_columnas_mariadb(self, conexion, dbname=None) -> List[Columna]:
        """
        Obtiene la definición de columnas de una tabla en una base de datos MySQL/MariaDB.
        Conecta a MariaDB usando pymysql.
        Ejecuta una consulta a INFORMATION_SCHEMA.COLUMNS, que es donde el motor guarda los metadatos de todas las tablas.
        Itera por cada fila y crea un objeto Columna con los datos reales de la tabla.
        Args:
            - `conexion`: Conexión pymysql abierta.
            - `dbname`: (Opcional) Nombre de la base de datos, 
                        si se deja vacío se toma de self.database.db emparentado a la tabla.
        Returns:
            - `columnas`: Lista de objetos Columna con la definición de cada columna.
        """
        if not dbname:
            if not self.database or not hasattr(self.database, 'db'):
                raise ValueError("No se ha especificado el nombre de la base de datos y la tabla no está asociada a una instancia Database.")
            dbname = self.database.db

        columnas = []
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                """SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY, EXTRA
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s""",
                (dbname, self.nombre)
            )
            for fila in cursor.fetchall():
                tipo_raw = fila["COLUMN_TYPE"]
                tipo_base = tipo_raw.split("(")[0].upper()

                # Extraer enum/set si aplica
                enum_opciones = None
                if tipo_base in {"ENUM", "SET"}:
                    enum_opciones = re.findall(r"'(.*?)'", tipo_raw)

                col = Columna(
                    nombre=fila["COLUMN_NAME"],
                    tipo=tipo_base,
                    longitud=self.extraer_longitud_campo(tipo_raw),
                    not_null=(fila["IS_NULLABLE"] == "NO"),
                    default=fila["COLUMN_DEFAULT"],
                    auto_increment=("auto_increment" in fila["EXTRA"].lower()),
                    primary_key=(fila["COLUMN_KEY"] == "PRI"),
                    unique=(fila["COLUMN_KEY"] == "UNI"),
                    enum_opciones=enum_opciones
                )
                columnas.append(col)

        return columnas
    
    def obtener_indices_mariadb(self, conexion, dbname: str) -> List["Index"]:
        """
        Obtiene la definición de índices de una tabla en una base de datos MySQL/MariaDB.

        - Args:
            - `conexion`: Conexión pymysql abierta.
            - `dbname`: (Opcional) Nombre de la base de datos, 
                        si se deja vacío se toma de self.database.db emparentado a la tabla.

        Returns:
            List[Index]: Lista de índices no primarios definidos en la tabla.
        """
        cursor = conexion.cursor()

        sql = f"SHOW INDEX FROM `{self.nombre}` FROM `{dbname}`;"
        cursor.execute(sql)
        filas = cursor.fetchall()

        resultado = {}
        for fila in filas:
            nombre = fila["Key_name"]
            columna = fila["Column_name"]
            if nombre == "PRIMARY":
                continue
            if nombre not in resultado:
                resultado[nombre] = []
            resultado[nombre].append(columna)

        return [Index(nombre=k, columnas=v) for k, v in resultado.items()]


    def obtener_fks_mariadb(self, conexion, dbname: str) -> List["ForeignKey"]:
        """
        Recupera las claves foráneas existentes en la tabla actual desde MariaDB.
        - Args:
            - `conexion`: Conexión pymysql abierta.
            - `dbname`: (Opcional) Nombre de la base de datos, 
                        si se deja vacío se toma de self.database.db emparentado a la tabla.

        Returns:
            List[Index]: Lista de FKs definidas en la tabla.
        """
        cursor = conexion.cursor()

        sql = """
            SELECT
                kcu.CONSTRAINT_NAME,
                kcu.COLUMN_NAME,
                kcu.REFERENCED_TABLE_NAME,
                kcu.REFERENCED_COLUMN_NAME,
                rc.UPDATE_RULE,
                rc.DELETE_RULE
            FROM information_schema.KEY_COLUMN_USAGE kcu
            JOIN information_schema.REFERENTIAL_CONSTRAINTS rc
                ON kcu.CONSTRAINT_NAME = rc.CONSTRAINT_NAME
                AND kcu.CONSTRAINT_SCHEMA = rc.CONSTRAINT_SCHEMA
            WHERE kcu.TABLE_SCHEMA = %s
            AND kcu.TABLE_NAME = %s
            AND kcu.REFERENCED_TABLE_NAME IS NOT NULL;
        """
        cursor.execute(sql, (dbname, self.nombre))
        filas = cursor.fetchall()

        resultado = []
        for fila in filas:
            fk = ForeignKey(
                columna=fila["COLUMN_NAME"],
                referencia_tabla=fila["REFERENCED_TABLE_NAME"],
                referencia_columna=fila["REFERENCED_COLUMN_NAME"],
                nombre=fila["CONSTRAINT_NAME"],
                on_update=fila["UPDATE_RULE"],
                on_delete=fila["DELETE_RULE"]
            )
            resultado.append(fk)

        return resultado

    def comparar_generar_alter(self, conexion, dbname=None, permitir_drop=False) -> List[str]:
        """
        Obtiene la definición de claves foráneas de una tabla en una base de datos MySQL/MariaDB.

        Args:
            - `conexion`: Conexión pymysql abierta.
            - `dbname`: (Opcional) Nombre de la base de datos, 
                        si se deja vacío se toma de self.database.db emparentado a la tabla.

        Returns:
            List[ForeignKey]: Lista de claves foráneas activas en la tabla.
        """
        
        if not dbname:
            if not self.database or not hasattr(self.database, 'db'):
                raise ValueError("No se ha especificado el nombre de la base de datos y la tabla no está asociada a Database.")
            dbname = self.database.db

        alteraciones = []

        reales = {col.nombre: col for col in self.obtener_columnas_mariadb(conexion, dbname)}
        definidas = {col.nombre: col for col in self.columnas}

        def norm(val):
            return str(val).replace("'", "").replace("()", "").strip().lower() if val is not None else None

        def default_eq(real, definido):
            if isinstance(definido, SQLLiteral):
                definido = definido.valor
            val_real = norm(real)
            val_def = norm(definido)
            null_equivalentes = {None, "null"}
            if val_real in null_equivalentes and val_def in null_equivalentes:
                return True
            equivalentes = {
                ("curdate", "current_date"),
                ("current_timestamp", "now"),
                ("current_timestamp", "current_timestamp on update current_timestamp"),
                ("current_timestamp", "current_timestamp on update current_timestamp()"),
            }
            return (val_real, val_def) in equivalentes or (val_def, val_real) in equivalentes or val_real == val_def

        def iguales(col_real, col_def):
            return (
                norm(col_real.tipo) == norm(col_def.tipo) and
                (col_real.not_null == col_def.not_null or col_def.primary_key) and
                default_eq(col_real.default, col_def.default) and
                bool(col_real.auto_increment) == bool(col_def.auto_increment) and
                bool(col_real.primary_key) == bool(col_def.primary_key) and
                bool(col_real.unique) == bool(col_def.unique) and
                set(col_real.enum_opciones or []) == set(col_def.enum_opciones or [])
            )

        # --- COLUMNAS ---
        for nombre, col_def in definidas.items():
            col_real = reales.get(nombre)
            if not col_real:
                alteraciones.append(f"ADD COLUMN {col_def.to_sql()}")
            elif not iguales(col_real, col_def):
                alteraciones.append(f"MODIFY COLUMN {col_def.to_sql()}")

        # --- ÍNDICES ---
        reales_idx = {tuple(i.columnas): i for i in self.obtener_indices_mariadb(conexion, dbname)}
        definidos_idx = {tuple(i.columnas): i for i in self.indices}

        for clave, idx_def in definidos_idx.items():
            if clave not in reales_idx:
                alteraciones.append(f"ADD {idx_def.to_sql()}")

        if permitir_drop:
            for clave, idx_real in reales_idx.items():
                if clave not in definidos_idx:
                    # Evitar eliminar índices implícitos de FKs
                    if any(
                        fk.columna in idx_real.columnas and fk.nombre == idx_real.nombre
                        for fk in self.foreign_keys
                    ):
                        continue
                    alteraciones.append(f"DROP INDEX `{idx_real.nombre}`")

        # --- CLAVES FORÁNEAS ---
        reales_fk_set = {
            (fk.columna, fk.referencia_tabla, fk.referencia_columna): fk
            for fk in self.obtener_fks_mariadb(conexion, dbname)
        }
        definidos_fk_set = {
            (fk.columna, fk.referencia_tabla, fk.referencia_columna): fk
            for fk in self.foreign_keys
        }

        for clave, fk_def in definidos_fk_set.items():
            if clave not in reales_fk_set:
                alteraciones.append(f"ADD {fk_def.to_sql()}")

        if permitir_drop:
            for clave, fk_real in reales_fk_set.items():
                if clave not in definidos_fk_set:
                    alteraciones.append(f"DROP FOREIGN KEY `{fk_real.nombre}`")

        return [f"ALTER TABLE `{self.nombre}`\n  " + ",\n  ".join(alteraciones) + ";"] if alteraciones else []


    def extraer_estructura(self, db_name: str) -> list[tuple[str, str, str, str | None, str]]:
        """
        Devuelve la estructura de la tabla, según definiciones, como una lista de tuplas:
        (db_name, tabla, tipo, nombre, definicion)
        """
        est = [(db_name, self.nombre, 'tabla', None, self.to_sql())]

        for col in self.columnas:
            est.append((db_name, self.nombre, 'columna', col.nombre, col.to_sql()))

        for idx in self.indices:
            est.append((db_name, self.nombre, 'indice', idx.nombre, idx.to_sql()))

        for fk in self.foreign_keys:
            est.append((db_name, self.nombre, 'fk', fk.nombre, fk.to_sql()))

        return est


    
class Database:
    def __init__(self, host: str, user: str, password: str, db: str, port: int = 3306, logger: Optional[logging.Logger] = None):
        """clase Database que:
        Almacena los parámetros de conexión.
        Mantiene una lista (o diccionario) de objetos Tabla.
        Genere una única conexión compartida (p. ej. con pymysql.connect()).
        Permita añadir tablas y reutilizar esa conexión para leer o sincronizar.
        Args:
            - `host`:       Host de la base de datos.
            - `user`:       Usuario de la base de datos.
            - `password`:   Contraseña del usuario.
            - `db`:         Nombre de la base de datos.
            - `port`      (int): Puerto de conexión (default 3306).
            - `logger`:     (opcional) Instancia de logger para registrar eventos .
        """
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        # Esto es una anotación de tipo que le dice al intérprete que self.tablas será un diccionario donde 
        # las claves son de tipo str (nombre de la tabla) y los valores son instancias de la clase Tabla.
        self.tablas: Dict[str, Tabla] = {}
        self._conexion = None  # connection
        self.logger = logger  # logger 
        self.ultimo_insert_id: Optional[int] = None
    
    @contextmanager
    def transaccion(self):
        """
        Context manager para ejecutar múltiples operaciones dentro de una transacción (modo síncrono).
        """
        conn = self._conexion
        try:
            conn.begin()
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        
    def conectar(self, autocommit=False):
        """
        Abre una única conexión reutilizable.
        Args:
            - `autocommit`: Si se debe activar el autocommit (por defecto False las transacciones se controlan manualmente.
        returns:
            - `conexion`: Conexión pymysql abierta.
        """
        if self._conexion is None or not self._conexion.open:
            self._conexion = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db,
                port=self.port,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit = autocommit
            )
        return self._conexion

    def cerrar(self):
        """cierra la conexión si está abierta. No interviene en la transacción activa."""
        if self._conexion and self._conexion.open:
            self._conexion.close()
    
    def commit(self):
        """
        Confirma la transacción activa si existe y cierra la conexión.
        Si no hay transacción activa o la conexión está cerrada, no hace nada.
        """
        if self._conexion and self._conexion.open:
            autocommit = self._conexion.get_autocommit()
            in_tx = getattr(self._conexion, "in_transaction", False)
            if not autocommit and in_tx:
                try:
                    self._conexion.commit()
                except Exception as e:
                    raise RuntimeError(f"Error al hacer commit: {e}") from e
            self.cerrar()
    
    def rollback(self):
        """
        Revierte la transacción activa si existe y cierra la conexión.
        Si no hay transacción activa o la conexión está cerrada, no hace nada.
        """
        if self._conexion and self._conexion.open:
            autocommit = self._conexion.get_autocommit()
            in_tx = getattr(self._conexion, "in_transaction", False)
            if not autocommit and in_tx:
                try:
                    self._conexion.rollback()
                except Exception as e:
                    raise RuntimeError(f"Error al hacer rollback: {e}") from e
            self.cerrar()

    

    def add_tabla(self, tabla: Tabla):
        """
        Añade un objeto Tabla al conjunto de esta base de datos.
        Args:
            - `tabla`: Objeto Tabla a añadir.
        """
        self.tablas[tabla.nombre] = tabla
        tabla.set_database(self) # Establece la referencia a la base de datos
        
        
    def get_tabla(self, nombre: str) -> Tabla:
        """
        Devuelve la tabla del nombre indicado. Si nombre no existe lanza un KeyError.
        Args:
            - `nombre`: Nombre de la tabla a devolver.
        """
        
        if nombre not in self.tablas:
            raise KeyError(f"La tabla '{nombre}' no está registrada en esta base de datos.")
        return self.tablas[nombre]

    

    def _query_select(self, sql: str, params=None, conexion=None, uno: bool = False) -> List[Dict]:
        """
        Ejecuta una consulta SELECT y devuelve los registros como lista de diccionarios.

        Args:
            - `sql`         (str): Consulta SQL.
            - `params`      (tuple or dict, optional): Parámetros para el SQL.
            - `conexion`    (pymysql.Connection, optional): Conexión externa abierta. Si no se indica, se abre una.

        Returns:
            List[Dict]: Lista de registros obtenidos.
        """
        propia = False
        if conexion is None:
            conexion = self.conectar()
            propia = True

        try:
            with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, params)
                if uno:
                    return cursor.fetchone()
                return cursor.fetchall()
        finally:
            if propia:
                self.cerrar()
    
    def _query_accion(self, sql: str, params=None, conexion=None) -> int:
        """
        Ejecuta una acción tipo INSERT, UPDATE, DELETE.

        - Args:
            - `sql`         - (str): Sentencia SQL.
            - `params`      - (tuple or dict, optional): Parámetros para la consulta.
            - `conexion`    - (pymysql.Connection, optional): Conexión externa abierta. Si no se indica, se abre una.
                        
        Returns:
            int: Número de filas afectadas.
        """
        propia = False
        if conexion is None:
            conexion = self.conectar()
            propia = True
        try:
            with conexion.cursor() as cursor:
                filas = cursor.execute(sql, params)
                self.ultimo_insert_id = cursor.lastrowid
                if propia:
                    conexion.commit()
                return filas
        except Exception as e:
            if propia:
                conexion.rollback()
            if self.logger:
                self.logger.error(f"Error al ejecutar acción: {e}")
            raise
        finally:
            if propia:
                self.cerrar()

    def query(self, sql: str, params=None, conexion=None, uno: bool = False):
        """
        Ejecuta automáticamente una consulta SQL detectando si es de lectura (SELECT)
        o de acción (INSERT, UPDATE, DELETE).

        - Args:
            - `sql`         - (str): Sentencia SQL.
            - `params`      - (tuple or dict, optional): Parámetros para la consulta.
            - `conexion`    - (pymysql.Connection, optional): Conexión externa abierta. Si no se indica, se abre una.
            - `uno`         - (bool):  Si True, se espera un único resultado (SELECT).
            
        Returns:
            Resultado de la operación:
                - List[Dict] si es SELECT, SHOW, DESC, etc.
                - int (nº de filas afectadas) si es INSERT/UPDATE/DELETE
        """
        sql_limpia = sql.strip().lstrip("/*- ").upper()
        comando = sql_limpia.split()[0]

        if comando in {"SELECT", "SHOW", "DESCRIBE", "DESC", "EXPLAIN"}:
            return self._query_select(sql, params=params, conexion=conexion, uno=uno)
        else:
            return self._query_accion(sql, params=params, conexion=conexion)

    

class DatabaseSync(Database):
    """
    Extensión de la clase Database que implementa lógica avanzada de verificación,
    simulación y aplicación de cambios estructurales, comparando contra la tabla 'estructura_actual'.
    """

    def crear_tablas_si_no_existen(self) -> dict:
        """
        Crea las tablas registradas en la base de datos usando CREATE TABLE IF NOT EXISTS.
        No aplica ALTERs.

        Returns:
            dict: Diccionario con:
                - clave: nombre de la tabla
                - valor: sentencia SQL ejecutada
        """
        resultados = {}
        try:
            conexion = self.conectar()
            with conexion.cursor() as cursor:
                for nombre_tabla, tabla in self.tablas.items():
                    sql_creacion = tabla.to_sql()  # Ya incluye IF NOT EXISTS
                    cursor.execute(sql_creacion)
                    resultados[nombre_tabla] = sql_creacion
                    if self.logger:
                        self.logger.info(f"Intento crear `{nombre_tabla}`.")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error al crear tablas: {e}")
            raise RuntimeError(f"Error al crear tablas: {e}") from e
        finally:
            self.cerrar()
        
        return resultados
    

    def simular_cambios(self, permitir_drop=False) -> dict:
        """
        Simula los cambios que aplicarían ALTER TABLE o CREATE TABLE (no ejecuta nada).
        Devuelve un diccionario con las sentencias que se generarían por tabla.
        """
        self.tablas = {t.nombre: t for t in self._ordenar_tablas_por_dependencias()}
        resultados = {}
        try:
            self.conectar()
            cursor = self._conexion.cursor()

            for nombre_tabla, tabla in self.tablas.items():
                # Comprobar si la tabla existe
                cursor.execute("SHOW TABLES LIKE %s", (nombre_tabla,))
                existe = cursor.fetchone() is not None

                if not existe:
                    resultados[nombre_tabla] = [tabla.to_sql()]
                else:
                    alter = tabla.comparar_generar_alter(self._conexion, permitir_drop=permitir_drop)
                    resultados[nombre_tabla] = alter if alter else []

        except Exception:
            resultados["error"] = traceback.format_exc()
            if self.logger:
                self.logger.error("Error al simular cambios:\n" + resultados["error"])
        finally:
            self.cerrar()

        return resultados

    def aplicar_cambios(self, permitir_drop: bool = True) -> dict:
        """
        Aplica todos los cambios estructurales en la base de datos:
        - Crea tablas que no existen (con CREATE TABLE IF NOT EXISTS)
        - Aplica ALTER TABLEs para sincronizar columnas, índices y claves foráneas
        - Registra cada cambio aplicado en la tabla _migraciones

        Todo dentro de una única transacción. Si ocurre un error, se revierte todo.

        Args:
            - `permitir_drop` (bool): Si se permiten DROP INDEX y DROP FOREIGN KEY.

        Returns:
            dict: Resultados por tabla (sentencias ejecutadas o errores).
        """
        self.tablas = {t.nombre: t for t in self._ordenar_tablas_por_dependencias()}
        resultados = {}
        try:
            conexion = self.conectar(autocommit=False)
            with conexion.cursor() as cursor:
                # Asegurar existencia de la tabla _migraciones
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS _migraciones (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        tabla VARCHAR(100),
                        sentencia TEXT,
                        fecha DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # --- Crear tablas nuevas ---
                for nombre_tabla, tabla in self.tablas.items():
                    sql_create = tabla.to_sql()
                    cursor.execute(sql_create)
                    self._registrar_migracion(conexion, nombre_tabla, sql_create)
                    resultados[nombre_tabla] = [sql_create]
                    if self.logger:
                        self.logger.info(f"Tabla `{nombre_tabla}`: ejecutado CREATE IF NOT EXISTS.")

                # --- Aplicar ALTER TABLEs ---
                for nombre_tabla, tabla in self.tablas.items():
                    alter_sqls = tabla.comparar_generar_alter(conexion, permitir_drop=permitir_drop)
                    for alter_sql in alter_sqls:
                        cursor.execute(alter_sql)
                        self._registrar_migracion(conexion, nombre_tabla, alter_sql)
                        resultados[nombre_tabla].append(alter_sql)
                        if self.logger:
                            self.logger.info(f"Tabla `{nombre_tabla}`: ejecutado ALTER -> {alter_sql}")

            conexion.commit()
            if self.logger:
                self.logger.info("Todos los cambios aplicados y confirmados.")

        except Exception:
            self.rollback()
            resultados["error"] = traceback.format_exc()
            if self.logger:
                self.logger.error("Error durante aplicar_cambios():\n" + resultados["error"])
        finally:
            self.cerrar()

        return resultados


    def _registrar_migracion(self, conexion, tabla: str, sentencia: str):
        """
        Registra una sentencia estructural (CREATE o ALTER) aplicada a una tabla en el historial de migraciones.

        Crea automáticamente la tabla `_migraciones` si no existe. Antes de registrar, verifica que la sentencia
        no haya sido previamente aplicada para evitar duplicados. Se utiliza una combinación de `tabla + sentencia`
        como criterio de unicidad.

        Este método está pensado para ser llamado automáticamente desde `aplicar_cambios()` tras ejecutar cada cambio.

        Args:
            - `conexion`    (pymysql.Connection): Conexión activa a la base de datos.
            - `tabla`       (str): Nombre de la tabla afectada por la sentencia.
            - `sentencia`   (str): Sentencia SQL completa que ha sido ejecutada (CREATE, ALTER, etc.).
        """
        with conexion.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS _migraciones (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tabla VARCHAR(100),
                    sentencia TEXT,
                    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                SELECT 1 FROM _migraciones
                WHERE tabla = %s AND sentencia = %s
            """, (tabla, sentencia))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO _migraciones (tabla, sentencia)
                    VALUES (%s, %s)
                """, (tabla, sentencia))


    def verificar_contra_estructura_actual(self) -> dict[str, list[str]]:
        """
        Compara la estructura definida en los modelos locales con la registrada previamente
        en la tabla 'estructura_actual'. Usa conexión gestionada internamente y acceso explícito
        por clave para evitar errores si se está usando DictCursor.

        Returns:
            dict[str, list[str]]: Diccionario con diferencias detectadas, agrupadas por tabla.
        """
        divergencias: dict[str, list[str]] = {}
        conn = self.conectar()

        try:
            with conn.cursor() as cur:
                for tabla in self.tablas.values():
                    cur.execute("""
                        SELECT tipo, nombre, definicion FROM estructura_actual
                        WHERE db_name = %s AND tabla = %s
                    """, (self.db, tabla.nombre))
                    registros_previos = cur.fetchall()

                    prev_dict = {
                        (r['tipo'], r['nombre']): r['definicion'].strip() if r['definicion'] else ""
                        for r in registros_previos
                    }

                    actual_dict = {('tabla', None): tabla.to_sql().strip()}

                    for col in tabla.columnas:
                        actual_dict[('columna', col.nombre)] = col.to_sql().strip()

                    for idx in tabla.indices:
                        nombre_idx = idx.nombre or "_".join(idx.columnas)
                        actual_dict[('indice', nombre_idx)] = idx.to_sql().strip()

                    for fk in tabla.foreign_keys:
                        nombre_fk = fk.nombre or f"fk_{tabla.nombre}_{fk.columna}"
                        actual_dict[('fk', nombre_fk)] = fk.to_sql().strip()

                    for clave, nueva_def in actual_dict.items():
                        antigua_def = prev_dict.get(clave)
                        if antigua_def is not None and nueva_def != antigua_def:
                            tipo, nombre = clave
                            nombre_txt = f"'{nombre}'" if nombre else "(sin nombre)"
                            divergencias.setdefault(tabla.nombre, []).append(
                                f"✏️ Cambio en {tipo} {nombre_txt}:\n  - Antes: {antigua_def}\n  - Ahora:  {nueva_def}"
                            )

                    for clave in prev_dict:
                        if clave not in actual_dict:
                            tipo, nombre = clave
                            if tipo == "columna":
                                continue
                            if tipo == "tabla" and nombre is None:
                                continue
                            nombre_txt = f"'{nombre}'" if nombre else "(sin nombre)"
                            divergencias.setdefault(tabla.nombre, []).append(
                                f"❌ {tipo.capitalize()} {nombre_txt} eliminado respecto a estructura registrada."
                            )

                    for clave in actual_dict:
                        if clave not in prev_dict:
                            tipo, nombre = clave
                            nombre_txt = f"'{nombre}'" if nombre else "(sin nombre)"
                            divergencias.setdefault(tabla.nombre, []).append(
                                f"➕ {tipo.capitalize()} {nombre_txt} añadido."
                            )
        finally:
            self.cerrar()

        return divergencias


    def _ordenar_tablas_por_dependencias_OLD(self) -> List[Tabla]:
        """
        Ordena las tablas internas considerando las claves foráneas (dependencias).

        Returns:
            List[Tabla]: Lista ordenada por orden de creación seguro.
        """
        tablas = list(self.tablas.values())
        dependencias = {t.nombre: set(fk.referencia_tabla for fk in t.foreign_keys) for t in tablas}
        tabla_dict = {t.nombre: t for t in tablas}
        ordenadas = []
        visitadas = set()
        procesadas_en_curso = set()  
        
        # def visitar(nombre):
        #     if nombre in visitadas:
        #         return
        #     for dep in dependencias.get(nombre, []):
        #         if dep in tabla_dict:
        #             visitar(dep)
        #     visitadas.add(nombre)
        #     ordenadas.append(tabla_dict[nombre])
        
        def visitar(nombre):
            if nombre in visitadas:
                return
            if nombre in procesadas_en_curso:
                raise RuntimeError(f"🚫 Ciclo de dependencias detectado en la tabla '{nombre}'")

            procesadas_en_curso.add(nombre)
            for dep in dependencias.get(nombre, []):
                visitar(dep)
            procesadas_en_curso.remove(nombre)

            visitadas.add(nombre)
            ordenadas.append(tablas[nombre])
        
        
        for nombre in tabla_dict:
            visitar(nombre)

        return ordenadas
    
    def _ordenar_tablas_por_dependencias(self) -> List[Tabla]:
        """
        Ordena las tablas internas considerando las claves foráneas (dependencias).

        Returns:
            List[Tabla]: Lista ordenada por orden de creación seguro.
        """
        tablas = {t.nombre: t for t in self.tablas.values()}
        dependencias = {
            t.nombre: [fk.referencia_tabla for fk in t.foreign_keys]
            for t in self.tablas.values()
        }
        ordenadas = []
        visitadas = set()
        en_curso = set()

        def visitar(nombre):
            if nombre in visitadas:
                return
            if nombre in en_curso:
                raise RuntimeError(f"🚫 Ciclo de dependencias detectado al visitar la tabla '{nombre}'.")

            en_curso.add(nombre)
            for dep in dependencias.get(nombre, []):
                visitar(dep)
            en_curso.remove(nombre)

            visitadas.add(nombre)
            ordenadas.append(tablas[nombre])

        for nombre in tablas:
            visitar(nombre)

        return ordenadas
    
    
    
    def simular_cambios_avanzado(self) -> dict[str, dict[str, list[str]]]:
        """
        Simula diferencias entre los modelos y:
        - La estructura real actual de la base de datos.
        - La estructura registrada en estructura_actual, si existe.

        Si la tabla estructura_actual no existe o está vacía, se asume primera ejecución
        y solo se compara contra la base de datos real.

        Returns:
            dict: Contiene claves:
                - 'comparacion_bd': Diferencias con la base de datos real.
                - 'comparacion_estructura_actual': Diferencias con la estructura registrada (si aplica).
        """
        print("🔍 Comparando estructura de modelos con base de datos real...")
        diferencias_bd = self.simular_cambios(permitir_drop=True)

        conn = self.conectar()
        usar_estructura_actual = False

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*) AS total FROM information_schema.tables
                    WHERE table_schema = %s AND table_name = 'estructura_actual'
                """, (self.db,))
                existe = cur.fetchone()
                if existe and existe.get("total", 0) > 0:
                    cur.execute("SELECT COUNT(*) AS filas FROM estructura_actual WHERE db_name = %s", (self.db,))
                    filas = cur.fetchone()
                    if filas and filas.get("filas", 0) > 0:
                        usar_estructura_actual = True
        finally:
            self.cerrar()

        if usar_estructura_actual:
            print("🔍 Comparando estructura de modelos con estructura_actual registrada...")
            diferencias_guardadas = self.verificar_contra_estructura_actual()
        else:
            print("ℹ️  Tabla 'estructura_actual' no existe o está vacía. Se asume primera ejecución.")
            diferencias_guardadas = {}

        return {
            "comparacion_bd": diferencias_bd,
            "comparacion_estructura_actual": diferencias_guardadas
        }


    def _aplicar_cambios_respecto_a_estructura_actual(self, permitir_drop: bool = False) -> dict[str, list[str]]:
        """
        Implementación interna que compara los modelos contra la estructura registrada en estructura_actual.
        Aplica ALTER TABLE o CREATE TABLE según sea necesario. Nunca elimina columnas.

        Args:
            permitir_drop (bool): Permite eliminar índices y claves foráneas. No afecta a columnas.

        Returns:
            dict[str, list[str]]: Acciones aplicadas agrupadas por tabla.
        """
        resultado: dict[str, list[str]] = {}
        conn = self.conectar(autocommit=False)

        try:
            with conn.cursor() as cur:
                for tabla in self.tablas.values():
                    cur.execute("""
                        SELECT tipo, nombre, definicion FROM estructura_actual
                        WHERE db_name = %s AND tabla = %s
                    """, (self.db, tabla.nombre))
                    registros_previos = cur.fetchall()
                    prev_dict = {(tipo, nombre): definicion.strip() if definicion else "" for tipo, nombre, definicion in registros_previos}

                    actual_dict = {('tabla', None): tabla.to_sql().strip()}

                    for col in tabla.columnas:
                        actual_dict[('columna', col.nombre)] = col.to_sql().strip()

                    for idx in tabla.indices:
                        nombre_idx = idx.nombre or "_".join(idx.columnas)
                        actual_dict[('indice', nombre_idx)] = idx.to_sql().strip()

                    for fk in tabla.foreign_keys:
                        nombre_fk = fk.nombre or f"fk_{tabla.nombre}_{fk.columna}"
                        actual_dict[('fk', nombre_fk)] = fk.to_sql().strip()

                    crear_tabla = False
                    cur.execute("""
                        SELECT COUNT(*) AS total FROM information_schema.tables
                        WHERE table_schema = %s AND table_name = %s
                    """, (self.db, tabla.nombre))
                    existe_bd = cur.fetchone()
                    if not existe_bd or existe_bd.get("total", 0) == 0:
                        crear_tabla = True

                    if crear_tabla:
                        cur.execute(tabla.to_sql())
                        resultado[tabla.nombre] = [tabla.to_sql()]
                    else:
                        alter_sqls = tabla.comparar_generar_alter(conn, permitir_drop=permitir_drop)
                        for alter_sql in alter_sqls:
                            cur.execute(alter_sql)
                            resultado.setdefault(tabla.nombre, []).append(alter_sql)

            conn.commit()
            self.guardar_estructura_actual(conn)

        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Error aplicando cambios en '{self.db}': {e}") from e

        finally:
            self.cerrar()

        return resultado



    def aplicar_cambios_respecto_a_estructura_actual(self, permitir_drop: bool = False) -> dict[str, list[str]]:
        """
        Aplica cambios estructurales comparando los modelos con la estructura registrada en 'estructura_actual'.
        Si la tabla no existe o está vacía, se considera primera ejecución y se aplican los cambios comparando contra
        la base de datos real, generando después la tabla estructura_actual.

        Args:
            permitir_drop (bool): Permite eliminar índices o claves foráneas si ya no existen en los modelos.
                                Nunca se eliminan columnas.

        Returns:
            dict[str, list[str]]: Acciones realizadas, agrupadas por tabla.
        """
        self.tablas = {t.nombre: t for t in self._ordenar_tablas_por_dependencias()}
        conn = self.conectar()
        usar_estructura_actual = False

        try:
            with conn.cursor() as cur:
                # Verificar existencia de la tabla estructura_actual
                cur.execute("""
                    SELECT COUNT(*) AS total FROM information_schema.tables
                    WHERE table_schema = %s AND table_name = 'estructura_actual'
                """, (self.db,))
                existe = cur.fetchone()
                if existe and existe.get("total", 0) > 0:
                    # Verificar si tiene contenido
                    cur.execute("SELECT COUNT(*) AS filas FROM estructura_actual WHERE db_name = %s", (self.db,))
                    filas = cur.fetchone()
                    if filas and filas.get("filas", 0) > 0:
                        usar_estructura_actual = True
        finally:
            self.cerrar()

        if not usar_estructura_actual:
            print("ℹ️  No hay estructura registrada. Se considera primera ejecución.")
            resultado = self.aplicar_cambios(permitir_drop=permitir_drop)
            conn = self.conectar()
            self.guardar_estructura_actual(conn)
            self.cerrar()
            return resultado

        print("🔄 Aplicando cambios comparando contra estructura_actual registrada...")
        return self._aplicar_cambios_respecto_a_estructura_actual(permitir_drop)





    def crear_tabla_estructura_si_no_existe(self, conn):
        """
        Crea la tabla estructura_actual si no existe.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS estructura_actual (
            id INT AUTO_INCREMENT PRIMARY KEY,
            db_name VARCHAR(100) NOT NULL,
            tabla VARCHAR(100) NOT NULL,
            tipo ENUM('tabla', 'columna', 'indice', 'fk') NOT NULL,
            nombre VARCHAR(100),
            definicion TEXT NOT NULL,
            fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY uniq_estructura (db_name, tabla, tipo, nombre)
        )
        """
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    
    
    def guardar_estructura_actual(self, conn):
        """
        Guarda en la tabla 'estructura_actual' la estructura actual de los modelos
        tras aplicar cambios correctamente. Borra primero los datos anteriores por tabla.

        - Args:
            - conn (pymysql.connections.Connection): Conexión activa a la base de datos.
        """
        try:
            self.crear_tabla_estructura_si_no_existe(conn)

            with conn.cursor() as cur:
                for tabla in self.tablas.values():
                    cur.execute(
                        "DELETE FROM estructura_actual WHERE db_name=%s AND tabla=%s",
                        (self.db, tabla.nombre)
                    )
                    for fila in tabla.extraer_estructura(self.db):
                        # Solo se permiten tipos válidos, evitamos errores como ('nombre', None) o cabeceras mal insertadas
                        if fila[2] not in {'tabla', 'columna', 'indice', 'fk'}:
                            if self.logger:
                                self.logger.warning(f"[IGNORADO] Tipo inválido '{fila[2]}' detectado en tabla '{tabla.nombre}': {fila}")
                            continue
                        
                        cur.execute("""
                            INSERT INTO estructura_actual (db_name, tabla, tipo, nombre, definicion)
                            VALUES (%s, %s, %s, %s, %s)
                        """, fila)

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Error guardando estructura actual para {self.db}: {e}") from e

    def insertar_registros_iniciales(self):
        """
        Inserta automáticamente los registros definidos en `tabla.registros_iniciales`
        para cada tabla sincronizada, si aún no existen.

        Se asume que la clave primaria es el campo 'id'.
        """
        conn = self.conectar()
        cursor = conn.cursor()

        for tabla in self.tablas.values():
            if not tabla.registros_iniciales:
                continue

            for registro in tabla.registros_iniciales:
                if "id" not in registro:
                    print(f"⚠️  Registro sin campo 'id' en tabla '{tabla.nombre}', se omite.")
                    continue

                try:
                    sql_check = f"SELECT 1 FROM `{tabla.nombre}` WHERE `id` = %s LIMIT 1"
                    cursor.execute(sql_check, (registro["id"],))

                    if not cursor.fetchone():
                        columnas = ", ".join(f"`{k}`" for k in registro)
                        placeholders = ", ".join(["%s"] * len(registro))
                        valores_insert = tuple(registro.values())
                        sql_insert = f"INSERT INTO `{tabla.nombre}` ({columnas}) VALUES ({placeholders})"
                        cursor.execute(sql_insert, valores_insert)
                except Exception as e:
                    print(f"❌ Error insertando en '{tabla.nombre}': {e}")

        conn.commit()
        self.cerrar()
        
    def crear_vistas(self):
        """
        Crea o reemplaza las vistas definidas en cada tabla usando `CREATE OR REPLACE VIEW`.
        Las vistas se recrean siempre, sin comparar con el estado previo.

        Se asume que las vistas están correctamente definidas en el atributo `tabla.vistas`.
        El orden se resuelve automáticamente si una vista depende de otra.
        """
        

        conn = self.conectar()
        cursor = conn.cursor()

        # Reunir todas las vistas como {nombre: SQL}
        vistas_dict: Dict[str, str] = {}
        for tabla in self.tablas.values():
            if tabla.vistas:
                for vista_sql in tabla.vistas:
                    if not vista_sql.strip().lower().startswith("create"):
                        print(f"⚠️  Vista en tabla '{tabla.nombre}' no comienza por 'CREATE':\n{vista_sql.strip().splitlines()[0]}")
                        continue
                    nombre_vista = self._extraer_nombre_vista(vista_sql)
                    if nombre_vista:
                        vistas_dict[nombre_vista] = vista_sql

        if not vistas_dict:
            print("ℹ️  No se encontraron vistas para crear.")
            return

        # Ordenar por dependencias entre vistas (mejorado)
        dependencias = {}
        for nombre, sql in vistas_dict.items():
            sql_lower = sql.lower()
            deps = []
            for otro in vistas_dict:
                if otro == nombre:
                    continue
                # Patrón flexible: busca vista entre espacios, comillas, acentos graves o delimitadores SQL
                patron = rf"""[\s`"'(,]({re.escape(otro.lower())})[\s`"'.,)]"""
                if re.search(patron, sql_lower):
                    deps.append(otro)
            dependencias[nombre] = set(deps)

        ordenadas = []
        visitadas = set()

        def visitar(v):
            if v in visitadas:
                return
            for dep in dependencias.get(v, []):
                visitar(dep)
            visitadas.add(v)
            ordenadas.append(v)

        for vista in vistas_dict:
            visitar(vista)

        print(f"🏗️  Se van a crear {len(ordenadas)} vistas: {', '.join(ordenadas)}")

        for nombre in ordenadas:
            sql = vistas_dict[nombre]
            try:
                cursor.execute(sql)
                print(f"✅ Vista creada: {nombre}")
                if self.logger:
                    self.logger.info(f"[Vista] Ejecutada: {nombre}")
            except Exception as e:
                print(f"❌ Error al crear vista '{nombre}': {e}")
                print("\n📄 SQL con error:\n" + sql + "\n")
                if self.logger:
                    self.logger.error(f"Error al crear vista '{nombre}': {e}")
                raise RuntimeError(f"Error al crear vista '{nombre}': {e}") from e

        conn.commit()
        self.cerrar()



    def _extraer_nombre_vista(self, sql: str) -> Optional[str]:
        """
        Extrae el nombre de la vista desde una sentencia CREATE VIEW.
        Admite CREATE OR REPLACE VIEW `nombre` AS ...
        """
        match = re.search(r"CREATE\s+(OR\s+REPLACE\s+)?VIEW\s+`?(\w+)`?", sql, re.IGNORECASE)
        return match.group(2) if match else None


    def crear_todo(self, permitir_drop: bool = True):
        """
        Ejecuta todo el ciclo de sincronización completo:
        - Aplica cambios estructurales respecto a estructura_actual (creación/modificación de tablas)
        - Inserta registros iniciales
        - Crea o reemplaza las vistas

        Args:
            permitir_drop (bool): Permite eliminar claves foráneas e índices si ya no existen en los modelos.
        """
        print(f"🔄 Aplicando cambios estructurales en '{self.db}'...")
        resultado = self.aplicar_cambios_respecto_a_estructura_actual(permitir_drop=permitir_drop)
        print(f"🔄 Insertando registros iniciales en '{self.db}'...")
        self.insertar_registros_iniciales()
        print(f"🏗️  Creando vistas en '{self.db}'...")
        self.crear_vistas()
        return resultado