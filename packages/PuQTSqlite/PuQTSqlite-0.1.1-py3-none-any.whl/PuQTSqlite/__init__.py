import os
import shutil
from pathlib import Path

def copy_file(filename, destination=None):
    """
    Копирует файл из пакета в текущую директорию
    
    Args:
        filename (str): Имя файла для копирования
        destination (str, optional): Путь назначения. По умолчанию текущая директория
    """
    package_dir = Path(__file__).parent
    source_file = package_dir / 'req' / filename
    
    if not source_file.exists():
        raise FileNotFoundError(f"Файл {filename} не найден в пакете")
    
    if destination is None:
        destination = Path.cwd()
    else:
        destination = Path(destination)
    
    shutil.copy2(source_file, destination)
    print(f"Файл {filename} успешно скопирован в {destination}")

def list_available_files():
    """
    Выводит список всех доступных файлов в пакете
    """
    package_dir = Path(__file__).parent
    req_dir = package_dir / 'req'
    
    if not req_dir.exists():
        raise FileNotFoundError("Директория req не найдена в пакете")
    
    files = [f.name for f in req_dir.iterdir() if f.is_file()]
    print("Доступные файлы:")
    for file in files:
        print(f"- {file}") 