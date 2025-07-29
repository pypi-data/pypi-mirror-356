# PuQTSqlite

Пакет для распространения файлов программы PyQt с SQLite.

## Установка

```bash
pip install PuQTSqlite
```

## Использование

```python
from PuQTSqlite import copy_file, list_available_files

# Посмотреть список доступных файлов
list_available_files()

# Скопировать файл в текущую директорию
copy_file('main.py')

# Скопировать файл в указанную директорию
copy_file('database.py', 'path/to/destination')
```

## Доступные файлы

- main.py
- database.py
- material_calc.py
- requirements.txt
- partners.db
- Мастер пол.png 