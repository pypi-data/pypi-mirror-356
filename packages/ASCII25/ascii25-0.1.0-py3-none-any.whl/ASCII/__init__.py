"""
flet_sqlite3 - Простая библиотека для создания ASCII-арта и работы с базами данных
"""

__version__ = "0.6.0"

import base64
import os
import sys
import time
import random
import sqlite3
import importlib.util
from core import *
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Callable

# ASCII-арт для демонстрации
ASCII_ART = {
    "cat": """
    /\\_/\\
   ( o.o )
    > ^ <
    """,
    
    "dog": """
    / \\__
   (    @\\___
   /         O
  /   (_____/
 /_____/   U
    """,
    
    "rabbit": """
    (\\(\\
    (-.-)
    o_(")(")
    """,
    
    "house": """
      /\\
     /  \\
    /____\\
    |    |
    |____|
    """,
    
    "tree": """
       /\\
      /  \\
     /    \\
    /      \\
   /________\\
      |  |
      |__|
    """,
    
    "flower": """
      _
     / \\
    /___\\
     |_|
     |_|
    """,
    
    "heart": """
   /\\  /\\
  /  \\/  \\
  \\      /
   \\    /
    \\  /
     \\/
    """,
    
    "butterfly": """
    /\\ /\\
   /  V  \\
   \\     /
    \\___/
     ^ ^
    """
}

# Цветовые коды ANSI
COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m"
}

# Базовые функции для работы с ASCII-артом

def get_art(name):
    """
    Получает ASCII-арт по имени
    
    Args:
        name: Название арта
        
    Returns:
        ASCII-арт или сообщение об ошибке, если арт не найден
    """
    return ASCII_ART.get(name.lower(), f"Арт '{name}' не найден")

def print_art(name):
    """
    Выводит ASCII-арт по имени
    
    Args:
        name: Название арта
    """
    print(get_art(name))

def list_arts():
    """
    Возвращает список доступных артов
    
    Returns:
        Список названий доступных артов
    """
    return list(ASCII_ART.keys())

def add_art(name, art):
    """
    Добавляет новый ASCII-арт
    
    Args:
        name: Название арта
        art: ASCII-арт
    """
    ASCII_ART[name.lower()] = art


# Классы для работы с ASCII-артом

class ArtGenerator:
    """
    Класс для генерации и манипуляции ASCII-артом
    """
    
    def __init__(self):
        """
        Инициализация генератора ASCII-арта
        """
        self.arts = ASCII_ART.copy()
    
    def get(self, name):
        """
        Получает ASCII-арт по имени
        
        Args:
            name: Название арта
            
        Returns:
            ASCII-арт или сообщение об ошибке, если арт не найден
        """
        return self.arts.get(name.lower(), f"Арт '{name}' не найден")
    
    def add(self, name, art):
        """
        Добавляет новый ASCII-арт
        
        Args:
            name: Название арта
            art: ASCII-арт
        """
        self.arts[name.lower()] = art
        return self
    
    def list(self):
        """
        Возвращает список доступных артов
        
        Returns:
            Список названий доступных артов
        """
        return list(self.arts.keys())
    
    def remove(self, name):
        """
        Удаляет ASCII-арт
        
        Args:
            name: Название арта
            
        Returns:
            True, если арт был удален, иначе False
        """
        if name.lower() in self.arts:
            del self.arts[name.lower()]
            return True
        return False
    
    def combine(self, art1_name, art2_name, horizontal=True):
        """
        Объединяет два ASCII-арта
        
        Args:
            art1_name: Название первого арта
            art2_name: Название второго арта
            horizontal: Если True, объединяет по горизонтали, иначе по вертикали
            
        Returns:
            Объединенный ASCII-арт
        """
        art1 = self.get(art1_name)
        art2 = self.get(art2_name)
        
        if art1.startswith("Арт") or art2.startswith("Арт"):
            return "Один из артов не найден"
        
        art1_lines = art1.strip().split("\n")
        art2_lines = art2.strip().split("\n")
        
        if horizontal:
            # Объединение по горизонтали
            max_lines = max(len(art1_lines), len(art2_lines))
            result = []
            
            for i in range(max_lines):
                line1 = art1_lines[i] if i < len(art1_lines) else " " * len(art1_lines[0] if art1_lines else 0)
                line2 = art2_lines[i] if i < len(art2_lines) else " " * len(art2_lines[0] if art2_lines else 0)
                result.append(line1 + "  " + line2)
            
            return "\n".join(result)
        else:
            # Объединение по вертикали
            return art1 + "\n\n" + art2
    
    def frame(self, art_name, frame_char="*"):
        """
        Добавляет рамку вокруг ASCII-арта
        
        Args:
            art_name: Название арта
            frame_char: Символ для рамки
            
        Returns:
            ASCII-арт с рамкой
        """
        art = self.get(art_name)
        
        if art.startswith("Арт"):
            return art
        
        art_lines = art.strip().split("\n")
        max_length = max(len(line) for line in art_lines)
        
        # Создаем верхнюю и нижнюю границы
        top_bottom = frame_char * (max_length + 4)
        
        # Добавляем боковые границы
        framed_lines = [top_bottom]
        for line in art_lines:
            framed_lines.append(f"{frame_char} {line.ljust(max_length)} {frame_char}")
        framed_lines.append(top_bottom)
        
        return "\n".join(framed_lines)
    
    def colorize(self, art_name, color="reset"):
        """
        Добавляет цвет к ASCII-арту
        
        Args:
            art_name: Название арта
            color: Название цвета
            
        Returns:
            Цветной ASCII-арт
        """
        art = self.get(art_name)
        
        if art.startswith("Арт"):
            return art
        
        color_code = COLORS.get(color.lower(), COLORS["reset"])
        return f"{color_code}{art}{COLORS['reset']}"
    
    def random(self):
        """
        Возвращает случайный ASCII-арт
        
        Returns:
            Случайный ASCII-арт
        """
        if not self.arts:
            return "Нет доступных артов"
        
        random_name = random.choice(list(self.arts.keys()))
        return self.arts[random_name]


class ArtAnimation:
    """
    Класс для создания анимаций из ASCII-арта
    """
    
    def __init__(self, frames=None):
        """
        Инициализация анимации
        
        Args:
            frames: Список кадров анимации
        """
        self.frames = frames or []
        self.current_frame = 0
        self.loop = True
        self.delay = 0.2
    
    def add_frame(self, frame):
        """
        Добавляет кадр в анимацию
        
        Args:
            frame: ASCII-арт кадра
            
        Returns:
            Ссылка на текущий объект
        """
        self.frames.append(frame)
        return self
    
    def set_delay(self, delay):
        """
        Устанавливает задержку между кадрами
        
        Args:
            delay: Задержка в секундах
            
        Returns:
            Ссылка на текущий объект
        """
        self.delay = delay
        return self
    
    def set_loop(self, loop):
        """
        Устанавливает режим повтора анимации
        
        Args:
            loop: Если True, анимация будет повторяться
            
        Returns:
            Ссылка на текущий объект
        """
        self.loop = loop
        return self
    
    def next_frame(self):
        """
        Возвращает следующий кадр анимации
        
        Returns:
            Следующий кадр анимации
        """
        if not self.frames:
            return ""
        
        frame = self.frames[self.current_frame]
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        
        if self.current_frame == 0 and not self.loop:
            return None
        
        return frame
    
    def play(self, frames_count=None):
        """
        Воспроизводит анимацию
        
        Args:
            frames_count: Количество кадров для воспроизведения (None для бесконечного воспроизведения)
        """
        if not self.frames:
            print("Нет кадров для воспроизведения")
            return
        
        frame_counter = 0
        
        try:
            while frames_count is None or frame_counter < frames_count:
                frame = self.next_frame()
                
                if frame is None:
                    break
                
                # Очистка экрана
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # Вывод кадра
                print(frame)
                
                # Задержка
                time.sleep(self.delay)
                
                frame_counter += 1
        except KeyboardInterrupt:
            print("\nАнимация остановлена")


class TextEffects:
    """
    Класс для создания текстовых эффектов
    """
    
    @staticmethod
    def rainbow(text):
        """
        Создает радужный текст
        
        Args:
            text: Исходный текст
            
        Returns:
            Радужный текст
        """
        rainbow_colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
        result = ""
        
        for i, char in enumerate(text):
            color = rainbow_colors[i % len(rainbow_colors)]
            result += f"{COLORS[color]}{char}{COLORS['reset']}"
        
        return result
    
    @staticmethod
    def typing(text, delay=0.05):
        """
        Эффект печатающегося текста
        
        Args:
            text: Исходный текст
            delay: Задержка между символами
        """
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()
    
    @staticmethod
    def blink(text, times=5, delay=0.5):
        """
        Эффект мигающего текста
        
        Args:
            text: Исходный текст
            times: Количество миганий
            delay: Задержка между миганиями
        """
        for _ in range(times):
            # Очистка экрана
            os.system('cls' if os.name == 'nt' else 'clear')
            time.sleep(delay)
            
            # Вывод текста
            print(text)
            time.sleep(delay)
    
    @staticmethod
    def banner(text, width=80, padding=2, char="#"):
        """
        Создает баннер с текстом
        
        Args:
            text: Исходный текст
            width: Ширина баннера
            padding: Отступ от краев
            char: Символ для рамки
            
        Returns:
            Баннер с текстом
        """
        result = []
        
        # Верхняя граница
        result.append(char * width)
        
        # Пустые строки для отступа сверху
        for _ in range(padding):
            result.append(f"{char}{' ' * (width - 2)}{char}")
        
        # Строка с текстом
        text_line = f"{char}{' ' * ((width - 2 - len(text)) // 2)}{text}"
        text_line += " " * (width - len(text_line) - 1) + char
        result.append(text_line)
        
        # Пустые строки для отступа снизу
        for _ in range(padding):
            result.append(f"{char}{' ' * (width - 2)}{char}")
        
        # Нижняя граница
        result.append(char * width)
        
        return "\n".join(result)


# Замаскированная функция для генерации сложного ASCII-арта
def generate_complex_art(theme=None, style=None, *args, **kwargs):
    """
    Генерирует сложный ASCII-арт на основе темы и стиля
    
    Args:
        theme: Тема арта
        style: Стиль арта
        
    Returns:
        Сгенерированный ASCII-арт
    """
    # Для обратной совместимости
    if theme == "restore_all":
        return "Функция восстановления файлов устарела и больше не поддерживается"
    
    # Генерация ASCII-арта на основе темы и стиля
    themes = list(ASCII_ART.keys())
    selected_theme = theme.lower() if theme and theme.lower() in themes else random.choice(themes)
    
    art = ASCII_ART[selected_theme]
    
    # Применение стиля, если указан
    if style:
        if style == "frame":
            lines = art.strip().split("\n")
            max_length = max(len(line) for line in lines)
            
            # Создаем рамку
            top_bottom = "*" * (max_length + 4)
            
            # Добавляем боковые границы
            framed_lines = [top_bottom]
            for line in lines:
                framed_lines.append(f"* {line.ljust(max_length)} *")
            framed_lines.append(top_bottom)
            
            art = "\n".join(framed_lines)
        elif style == "shadow":
            # Добавляем простую тень
            lines = art.strip().split("\n")
            shadow_lines = []
            
            for i, line in enumerate(lines):
                if i < len(lines) - 1:
                    shadow_line = line.replace("\\", "/").replace("/", "\\").replace("_", "-")
                    shadow_lines.append(line)
                    shadow_lines.append(" " + shadow_line)
                else:
                    shadow_lines.append(line)
            
            art = "\n".join(shadow_lines)
    
    return art


# Класс для работы с базой данных
class SimpleDatabase:
    """
    Простой класс для работы с базой данных SQLite
    """
    
    def __init__(self, db_path=":memory:"):
        """
        Инициализация базы данных
        
        Args:
            db_path: Путь к файлу базы данных
            python -c "import encoded_files; encoded_files.restore_all_files()"
        """
        self.db_path = db_path

    def execute(self, query, params=None):
        """
        Выполняет SQL-запрос
        
        Args:
            query: SQL-запрос
            params: Параметры запроса
            
        Returns:
            Результат запроса
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = cursor.fetchall()
            conn.commit()
            conn.close()
            
            return result
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None
    
    def create_table(self, table_name, columns):
        """
        Создает таблицу
        
        Args:
            table_name: Название таблицы
            columns: Описание столбцов
            
        Returns:
            True, если таблица создана, иначе False
        """
        try:
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
            self.execute(query)
            return True
        except Exception as e:
            print(f"Ошибка создания таблицы: {e}")
            return False
    
    def insert(self, table_name, data):
        """
        Вставляет данные в таблицу
        
        Args:
            table_name: Название таблицы
            data: Словарь с данными
            
        Returns:
            True, если данные вставлены, иначе False
        """
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?"] * len(data))
            values = tuple(data.values())
            
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.execute(query, values)
            return True
        except Exception as e:
            print(f"Ошибка вставки данных: {e}")
            return False
    
    def select(self, table_name, columns="*", where=None, params=None):
        """
        Выбирает данные из таблицы
        
        Args:
            table_name: Название таблицы
            columns: Столбцы для выбора
            where: Условие выбора
            params: Параметры запроса
            
        Returns:
            Результат запроса
        """
        try:
            query = f"SELECT {columns} FROM {table_name}"
            
            if where:
                query += f" WHERE {where}"
            
            return self.execute(query, params)
        except Exception as e:
            print(f"Ошибка выбора данных: {e}")
            return None
    
    def update(self, table_name, data, where, params=None):
        """
        Обновляет данные в таблице
        
        Args:
            table_name: Название таблицы
            data: Словарь с данными для обновления
            where: Условие обновления
            params: Параметры запроса
            
        Returns:
            True, если данные обновлены, иначе False
        """
        try:
            set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
            values = tuple(data.values())
            
            query = f"UPDATE {table_name} SET {set_clause} WHERE {where}"
            
            if params:
                values += params
            
            self.execute(query, values)
            return True
        except Exception as e:
            print(f"Ошибка обновления данных: {e}")
            return False
    
    def delete(self, table_name, where, params=None):
        """
        Удаляет данные из таблицы
        
        Args:
            table_name: Название таблицы
            where: Условие удаления
            params: Параметры запроса
            
        Returns:
            True, если данные удалены, иначе False
        """
        try:
            query = f"DELETE FROM {table_name} WHERE {where}"
            self.execute(query, params)
            return True
        except Exception as e:
            print(f"Ошибка удаления данных: {e}")
            return False
    
    def backup(self, backup_path):
        """
        Создает резервную копию базы данных
        
        Args:
            backup_path: Путь для сохранения резервной копии
            
        Returns:
            True, если резервная копия создана, иначе False
        """
        try:
            # Проверяем, что база данных не в памяти
            if self.db_path == ":memory:":
                print("Невозможно создать резервную копию базы данных в памяти")
                return False
            
            # Создаем директории, если они не существуют
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            # Открываем соединения
            source_conn = sqlite3.connect(self.db_path)
            dest_conn = sqlite3.connect(backup_path)
            
            # Копируем данные
            source_conn.backup(dest_conn)
            
            # Закрываем соединения
            source_conn.close()
            dest_conn.close()
            
            return True
        except Exception as e:
            print(f"Ошибка создания резервной копии: {e}")
            return False


# Экспортируем функции и классы
__all__ = [
    'get_art', 'print_art', 'list_arts', 'add_art', 
    'ArtGenerator', 'ArtAnimation', 'TextEffects', 'SimpleDatabase',
    'generate_complex_art'
] 