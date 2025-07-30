# Documentación de la Librería mtpk_mariadb para Gestión de MariaDB

Esta librería es un **wrapper avanzado para la gestión de bases de datos MariaDB** utilizando `pymysql`. Está diseñada para facilitar la creación, sincronización y mantenimiento de estructuras de tablas en una base de datos.

## **Instalación**

```bash
pip install mtpk_mariadb
```

---

## **1. Gestión de Tablas y Columnas**
La librería permite definir tablas y columnas como objetos Python (`Tabla`, `Columna`, `ForeignKey`, `Index`) y generar automáticamente las sentencias SQL necesarias para crear o modificar estas estructuras.

### **Qué puedes hacer:**
- **Definir tablas y columnas:** Usa las clases `Tabla` y `Columna` para modelar tus tablas con sus atributos (tipos, claves primarias, valores por defecto, etc.).
- **Generar SQL automáticamente:** Convierte tus definiciones en sentencias SQL con métodos como `to_sql()`.
- **Añadir relaciones:** Define claves foráneas (`ForeignKey`) y índices (`Index`) fácilmente.

---

## **2. Sincronización de Estructuras**
La clase `DatabaseSync` permite comparar las estructuras definidas en tu código con las existentes en la base de datos y aplicar los cambios necesarios.

### **Qué puedes hacer:**
- **Simular cambios:** Usa `simular_cambios()` para ver qué sentencias SQL se generarían para sincronizar la base de datos.
- **Aplicar cambios:** Usa `aplicar_cambios()` para ejecutar las sentencias generadas y sincronizar la base de datos.
- **Evitar errores manuales:** La librería valida automáticamente duplicados y conflictos en columnas, índices y claves foráneas.

---

## **3. Registro de Migraciones**
La librería incluye una tabla especial (`_migraciones`) para registrar los cambios estructurales aplicados, lo que facilita el seguimiento de las modificaciones realizadas.

### **Qué puedes hacer:**
- **Historial de cambios:** Consulta la tabla `_migraciones` para ver qué cambios se han aplicado y cuándo.
- **Evitar duplicados:** La librería verifica que no se apliquen cambios ya registrados.

---

## **4. Comparación Avanzada**
La librería permite comparar la estructura actual de la base de datos con una estructura registrada previamente en la tabla `estructura_actual`.

### **Qué puedes hacer:**
- **Verificar diferencias:** Usa `verificar_contra_estructura_actual()` para detectar cambios entre la estructura actual y la registrada.
- **Actualizar registros:** Usa `guardar_estructura_actual()` para mantener actualizada la tabla `estructura_actual` con los modelos actuales.

---

## **5. Ejecución de Consultas**
La clase `Database` incluye métodos para ejecutar consultas SQL de lectura (`SELECT`) y acción (`INSERT`, `UPDATE`, `DELETE`) de forma sencilla.

### **Qué puedes hacer:**
- **Ejecución simplificada:** Usa `query()` para ejecutar cualquier consulta SQL sin preocuparte por abrir o cerrar conexiones.
- **Transacciones:** Controla transacciones manualmente con `commit()` y `rollback()`.

---

## **6. Casos de Uso**
Esta librería es ideal para:
- **Proyectos con cambios frecuentes en la base de datos:** Sincroniza automáticamente las estructuras sin necesidad de escribir manualmente sentencias SQL.
- **Gestión de bases de datos complejas:** Define relaciones, índices y claves foráneas de forma declarativa.
- **Migraciones controladas:** Lleva un registro de los cambios aplicados para facilitar el mantenimiento y la auditoría.


# Guía de Referencia de Clases y Métodos

## **Clases Principales**

### **1. `Columna`**
Representa una columna SQL para crear tablas en MariaDB.

#### **Atributos:**
- `nombre` (str): Nombre de la columna.
- `tipo` (str): Tipo de dato según MariaDB.
- `longitud` (Optional[int]): Longitud para tipos como VARCHAR(n), CHAR(n), etc.
- `precision` (Optional[int]): Precisión para DECIMAL(p, s), FLOAT(p), etc.
- `escala` (Optional[int]): Escala para DECIMAL(p, s).
- `not_null` (bool): Si la columna debe ser NOT NULL.
- `primary_key` (bool): Si esta columna es clave primaria.
- `unique` (bool): Si esta columna tiene restricción UNIQUE.
- `auto_increment` (bool): Si es autoincremental.
- `default` (Optional[Union[str, int, float, Literal["CURRENT_TIMESTAMP"]]]): Valor por defecto.
- `comentario` (Optional[str]): Comentario SQL para la columna.
- `enum_opciones` (Optional[list[str]]): Lista de valores posibles si el tipo es ENUM o SET.

#### **Métodos:**
- `to_sql() -> str`: Genera la definición SQL de esta columna.

---

### **2. `ForeignKey`**
Representa una clave foránea (FOREIGN KEY) en una tabla SQL.

#### **Atributos:**
- `columna` (str): Nombre de la columna local que actúa como clave foránea.
- `referencia_tabla` (str): Nombre de la tabla referenciada.
- `referencia_columna` (str): Columna de la tabla referenciada.
- `nombre` (Optional[str]): Nombre explícito del constraint.
- `on_delete` (Optional[str]): Acción al eliminar la fila referenciada.
- `on_update` (Optional[str]): Acción al actualizar la fila referenciada.

#### **Métodos:**
- `to_sql() -> str`: Genera la definición SQL de la clave foránea.

---

### **3. `Index`**
Representa un índice (normal o único) sobre una o más columnas de una tabla SQL.

#### **Atributos:**
- `columnas` (List[str]): Lista de nombres de columnas incluidas en el índice.
- `nombre` (Optional[str]): Nombre personalizado del índice.
- `unico` (bool): Indica si el índice es único (`UNIQUE`).

#### **Métodos:**
- `to_sql() -> str`: Genera la definición SQL del índice.

---

### **4. `Tabla`**
Representa la definición estructural de una tabla SQL para MariaDB.

#### **Atributos:**
- `nombre` (str): Nombre de la tabla.
- `columnas` (List[Columna]): Lista de columnas de la tabla.
- `indices` (List[Index]): Lista de índices adicionales.
- `foreign_keys` (List[ForeignKey]): Lista de claves foráneas.
- `claves_primarias` (List[str]): Lista de columnas que componen la clave primaria.
- `comentario` (Optional[str]): Comentario descriptivo opcional.
- `engine` (str): Motor de almacenamiento (por defecto `"InnoDB"`).
- `charset` (str): Conjunto de caracteres (por defecto `"utf8mb4"`).

#### **Métodos:**
- `add_columna(columna: Columna)`: Añade una columna a la tabla.
- `set_columnas(columnas: List[Columna])`: Reemplaza la lista completa de columnas.
- `add_index(index: Index)`: Añade un índice a la tabla.
- `set_indices(indices: List[Index])`: Reemplaza la lista completa de índices.
- `add_foreign_key(fk: ForeignKey)`: Añade una clave foránea a la tabla.
- `set_foreign_keys(foreign_keys: List[ForeignKey])`: Reemplaza la lista completa de claves foráneas.
- `to_sql() -> str`: Genera la sentencia SQL `CREATE TABLE`.
- `comparar_generar_alter(...) -> List[str]`: Compara la estructura actual con la base de datos y genera sentencias `ALTER TABLE`.

---

### **5. `Database`**
Clase base para gestionar conexiones y operaciones con MariaDB.

#### **Atributos:**
- `host` (str): Host de la base de datos.
- `user` (str): Usuario de la base de datos.
- `password` (str): Contraseña del usuario.
- `db` (str): Nombre de la base de datos.
- `port` (int): Puerto de conexión (por defecto `3306`).
- `tablas` (Dict[str, Tabla]): Diccionario de tablas registradas.

#### **Métodos:**
- `conectar(autocommit=False)`: Abre una conexión reutilizable.
- `cerrar()`: Cierra la conexión si está abierta.
- `commit()`: Confirma la transacción activa.
- `rollback()`: Revierte la transacción activa.
- `add_tabla(tabla: Tabla)`: Añade una tabla al conjunto de la base de datos.
- `get_tabla(nombre: str) -> Tabla`: Devuelve una tabla registrada.
- `query(sql: str, params=None, conexion=None)`: Ejecuta una consulta SQL (lectura o acción).

---

### **6. `DatabaseSync`**
Extensión de `Database` para sincronización avanzada de estructuras.

#### **Métodos:**
- `crear_tablas_si_no_existen() -> dict`: Crea las tablas registradas si no existen.
- `simular_cambios(permitir_drop=False) -> dict`: Simula los cambios necesarios para sincronizar la base de datos.
- `aplicar_cambios(permitir_drop=True) -> dict`: Aplica los cambios estructurales en la base de datos.
- `verificar_contra_estructura_actual() -> dict`: Compara los modelos locales con la estructura registrada en `estructura_actual`.
- `guardar_estructura_actual(conn)`: Guarda la estructura actual de los modelos en la tabla `estructura_actual`.

---

## **Ejemplo de Uso**

```python
from core_sync import Tabla, Columna, DatabaseSync

# Definir una tabla
tabla_usuarios = Tabla(
    nombre="usuarios",
    columnas=[
        Columna(nombre="id", tipo="INT", auto_increment=True, primary_key=True),
        Columna(nombre="nombre", tipo="VARCHAR", longitud=100, not_null=True),
        Columna(nombre="email", tipo="VARCHAR", longitud=150, unique=True),
    ],
    comentario="Tabla de usuarios"
)

# Crear una base de datos y registrar la tabla
db = DatabaseSync(host="localhost", user="root", password="1234", db="mi_base")
db.add_tabla(tabla_usuarios)

# Sincronizar la estructura
db.aplicar_cambios()
```

---

## **Notas Finales**
- Esta librería es ideal para proyectos con cambios frecuentes en la base de datos.
- Permite automatizar la creación y sincronización de estructuras, evitando errores manuales.
- Integra funcionalidades avanzadas como migraciones y comparación de estructuras.
