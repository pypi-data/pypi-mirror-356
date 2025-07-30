# 🧠 dbtype_checker

A simple and lightweight tool to **detect columns stored in the wrong data type** in your database.  
It connects to your SQL database, samples data, and infers the **true data types** using intelligent pandas-based logic.

---

## 🚀 Features

- Detects `int`, `float`, `bool`, `datetime`, `str`
- Identifies type mismatches based on actual values
- Works with PostgreSQL, MySQL, Oracle (via SQLAlchemy)
- Easy to integrate into data pipelines
- No heavy dependencies — pure pandas + regex logic

---

## 📦 Installation

Install via pip:

```bash
pip install dbtype_checker " OR" pip install dbtype-checker==0.1.7


""" 
## EXAMPLE USAGE

For postgres:

from dbtype_checker.checker import print_mismatches

db_url = "postgresql+pg8000://user:password@localhost/database_name"
print_mismatches(db_url)

For MySQL:

from dbtype_checker.checker import print_mismatches

db_url = "mysql+pymysql://user:password@localhost/database"
print_mismatches(db_url)

For Oracle:
from dbtype_checker.checker import print_mismatches

db_url = (
    "oracle+cx_oracle://username:password@host:1521/"
    "?service_name=your_service_name"
)
print_mismatches(db_url)

"""
