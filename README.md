# Sistema de Gestión de Información

**Autor:** Juan Diego Cartagena  
**Ficha:** 3406211

---

## Descripción

Aplicación de consola en Python para gestionar registros de personas. Permite crear, listar, buscar, actualizar y eliminar registros con persistencia en archivo JSON, menú interactivo con colores y generación de datos falsos con Faker.

---

## Estructura del proyecto

```
gestion-info/
├── README.md
├── requirements.txt
├── data/
│   └── records.json
├── src/
│   ├── main.py          # Punto de entrada
│   ├── menu.py          # Menú interactivo (UI)
│   ├── service.py       # Lógica de negocio (CRUD)
│   ├── file.py          # Persistencia (leer/guardar JSON)
│   ├── validate.py      # Validaciones de campos
│   └── integration.py   # Generación de datos con Faker
└── tests/
    ├── conftest.py
    ├── test_service.py
    └── test_validate.py
```

---

## Requisitos

- Python 3.10 o superior
- pip

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/gestion-info.git
cd gestion-info

# 2. Instalar dependencias
pip install -r requirements.txt
```

---

## Cómo ejecutar

```bash
# Desde la raíz del proyecto
python src/main.py
```

Al ejecutar se abre el menú interactivo con las siguientes opciones:

```
[1] Crear registro
[2] Listar registros
[3] Buscar registro
[4] Obtener registro por ID
[5] Actualizar registro
[6] Eliminar registro
[7] Generar registros falsos (Faker)
[0] Salir
```

---

## Módulos

### Módulo 1 — Estructura de datos y validaciones
Define la estructura del registro (`id`, `name`, `email`) y las validaciones en `validate.py`. Usa un `set` interno en `RecordService` para garantizar IDs únicos.

### Módulo 2 — Persistencia en archivos JSON
`file.py` expone `load_data()` y `save_data()`. Si el archivo no existe lo crea automáticamente; si está dañado muestra advertencia y arranca con datos vacíos.

### Módulo 3 — CRUD completo
`service.py` implementa las operaciones completas:

| Método | Descripción |
|---|---|
| `new_register(record)` | Crea un registro validado |
| `list_records(order_by)` | Lista ordenado por campo |
| `search_record(query)` | Busca por nombre o email (ignora acentos) |
| `get_record_by_id(id)` | Obtiene un registro por su ID |
| `update_record(id, data)` | Actualiza campos de un registro |
| `delete_record(id)` | Elimina un registro |

### Módulo 4 — Menú interactivo
`menu.py` con interfaz de consola usando `colorama`. El menú se repite hasta seleccionar "Salir" y maneja entradas inválidas sin romperse.

### Módulo 5 — Integración con Faker (`*args` / `**kwargs`)
`integration.py` genera registros falsos realistas en español (locale `es_MX`).

`build_record(*args, **kwargs)` — función genérica que acepta campos posicionales o nombrados:

```python
# Solo args
build_record("F01", "Ana Torres", "ana@gmail.com")

# Solo kwargs
build_record(id="F01", name="Ana Torres", email="ana@gmail.com")

# Mixto
build_record("F01", name="Ana Torres", email="ana@gmail.com")
```

`generate_fake_records(n, **overrides)` — genera `n` registros falsos; acepta `**overrides` para fijar campos en todos:

```python
generate_fake_records(5, email="test@gmail.com")
```

`bulk_insert` en `service.py` también usa `**kwargs`:

```python
service.bulk_insert(records, skip_errors=True, prefix="[Faker]")
```

### Módulo 6 — Pruebas con pytest
56 pruebas organizadas por clases en `tests/`:

| Archivo | Clases de prueba |
|---|---|
| `test_validate.py` | `TestValidateId`, `TestValidateName`, `TestValidateEmail`, `TestValidateRecord` |
| `test_service.py` | `TestNewRegister`, `TestListRecords`, `TestSearchRecord`, `TestGetRecordById`, `TestUpdateRecord`, `TestDeleteRecord`, `TestBulkInsert` |

---

## Cómo ejecutar las pruebas

```bash
# Desde la raíz del proyecto
pytest tests/ -v
```

Resultado esperado:

```
56 passed in 0.8s
```

---

## Dependencias

```
colorama   # Colores en consola
faker      # Generación de datos falsos
pytest     # Framework de pruebas
```

Instalar con:

```bash
pip install -r requirements.txt
```

---

## Validaciones aplicadas

- **ID:** no puede estar vacío, debe ser `str` o `int`
- **Nombre:** requerido, mínimo 2 caracteres
- **Email:** debe contener `@` y terminar en `.com`