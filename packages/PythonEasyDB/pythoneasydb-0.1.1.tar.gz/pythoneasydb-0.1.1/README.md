# 🗉 PythonEasyDB

**PythonEasyDB** — bu Python kutubxonasi bo‘lib, u bir nechta turdagi ma'lumotlar bazalariga yagona interfeys orqali ulanish imkonini beradi:  
✅ **SQLite**  
✅ **PostgreSQL**  
✅ **MongoDB**  
✅ **Redis**

Ushbu kutubxona SQL yozmasdan, yuqori darajadagi (high-level) API orqali qulay ishlash imkonini beradi. 

---

## 🚀 O‘rnatish

```bash
pip install PythonEasyDB
```

Yoki manba koddan:

```bash
git clone https://github.com/asrorbekaliqulov/PythonEasyDB.git
cd unidb
pip install .
```

---

## 📆 Qo‘llab-quvvatlanadigan bazalar

| Engine     | Ulash uchun URI namunasi                  |
|------------|-------------------------------------------|
| SQLite     | `sqlite:///path/to/db.sqlite3`            |
| PostgreSQL | `postgresql://user:password@localhost/db` |
| MongoDB    | `mongodb://localhost:27017/db`            |
| Redis      | `redis://localhost:6379`                  |

---

## ⚡️ Quick Start

```python
from PythonEasyDB import easydb

# SQLite bilan ulanish
db = easydb("sqlite:///mydb.sqlite3")

# Jadval yaratish
db.create_table(
    "users",
    id={"type": "int", "primary_key": True, "auto_increment": True},
    name={"type": "str", "not_null": True},
    age="int",
    active={"type": "bool", "default": True}
)

# Ma'lumot qo‘shish
db.insert("users", {"name": "Asrorbek", "age": 20})

# Ma'lumot olish
users = db.select("users", where={"age__gte": 22}, order_by="name", desc=True)
print(users)
```

---

## 📘 API Hujjatlari

### ✅ `create_table`

```python
create_table(table_name, **columns)
```

**`columns`** dictionary formatda bo‘lishi kerak:

```python
{
    "id": {
        "type": "int",
        "primary_key": True,
        "auto_increment": True,
        "not_null": True,
        "unique": True,
        "default": 1,
        "foreign_key": ("other_table", "column"),
        "on_delete": "cascade"
    }
}
```

---

### ✅ `insert`

```python
insert(table_name, data)
```

Misol:

```python
db.insert("users", {"name": "Ali", "age": 20})
```

---

### ✅ `select`

```python
select(
    table_name,
    where=None,
    order_by=None,
    desc=False,
    limit=None,
    offset=None,
    group_by=None,
    having=None,
    distinct=False,
    joins=None
)
```

**Qo‘llab-quvvatlanadigan `where` operatorlari:**

| Operator  | Tavsif         | Misol (`where={}`)       |
|-----------|----------------|--------------------------|
| `eq`      | tenglik        | `"age__eq": 20`          |
| `ne`      | teng emas      | `"age__ne": 30`          |
| `lt/lte`  | kichik/≤        | `"age__lt": 18`          |
| `gt/gte`  | katta/≥        | `"age__gte": 16`         |
| `in`      | ro‘yxatda      | `"id__in": [1,2,3]`      |
| `like`    | LIKE qidiruv   | `"name__like": "%Ali%"`  |
| `isnull`  | `NULL` tekshiri | `"email__isnull": True`  |

---

### ✅ `update`

```python
update(table_name, where, values)
```

Misol:

```python
db.update("users", where={"id": 1}, values={"name": "Ali"})
```

---

### ✅ `delete`

```python
delete(table_name, where)
```

Misol:

```python
db.delete("users", where={"age__lt": 16})
```

---

### ✅ `close`

```python
db.close()
```

Bazani yopish uchun.

---

## ✅ Moslik (Compatibility)

- Python 3.7+
- SQLite 3+
- PostgreSQL 10+
- MongoDB 4.0+
- Redis 5+

---

## 🛠 Hissa qo‘shish (Contributing)

```bash
git clone https://github.com/asrorbekaliqulov/PythonEasyDB.git
cd PythonEasyDB
python3 -m venv venv
source venv/bin/activate
pip install -e .[dev]
pytest
```

Pull request yuborishdan oldin testlar ishlashiga ishonch hosil qiling.

---

## 📜 Litsenziya

Ushbu loyiha [MIT](LICENSE) litsenziyasi ostida.

---

## 📬 Muallif

**Asrorbek Aliqulov**  
📧 Email: asrorbekaliqulov08@gmail.com  
🌐 Sayt: [https://asrorbekaliqulov.uz](asrorbekaliqulov.uz)

---
