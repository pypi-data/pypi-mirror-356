import os

def mmap_read(file_path: str) -> str:
    """Чтение файла через memory-mapping (идеально для больших файлов)."""
    with open(file_path, 'rb') as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            return mm.read().decode('utf-8')

class RawFileReader:
    def __init__(self):
        self.BOM_UTF8 = b'\xef\xbb\xbf'
        self.BOM_UTF16_LE = b'\xff\xfe'
        self.BOM_UTF16_BE = b'\xfe\xff'
        self.BOM_UTF32_LE = b'\xff\xfe\x00\x00'
        self.BOM_UTF32_BE = b'\x00\x00\xfe\xff'

    def _detect_encoding(self, raw_data: bytes) -> str:
        """Определяет кодировку по BOM (для UTF-8/16/32)."""
        if raw_data.startswith(self.BOM_UTF8):
            return 'utf-8-sig'
        elif raw_data.startswith(self.BOM_UTF16_LE):
            return 'utf-16-le'
        elif raw_data.startswith(self.BOM_UTF16_BE):
            return 'utf-16-be'
        elif raw_data.startswith(self.BOM_UTF32_LE):
            return 'utf-32-le'
        elif raw_data.startswith(self.BOM_UTF32_BE):
            return 'utf-32-be'
        return 'utf-8'  # Дефолтная кодировка

    def _read_bytes(self, file_path: str) -> bytes:
        """Читает файл как сырые байты (без os.open)."""
        with open(file_path, 'rb') as f:
            return f.read()

    def read_txt(self, file_path: str) -> str:
        """Читает TXT-файл с автоопределением кодировки."""
        raw_data = self._read_bytes(file_path)
        encoding = self._detect_encoding(raw_data)
        try:
            return raw_data.decode(encoding)
        except UnicodeDecodeError:
            # Фоллбек на latin-1, если UTF-8 не сработал
            return raw_data.decode('latin-1')

    def read_csv(self, file_path: str, delimiter=',') -> list[list[str]]:
        """Парсит CSV без внешних библиотек."""
        text = self.read_txt(file_path)
        lines = text.splitlines()
        return [line.split(delimiter) for line in lines]

    def read_xls(self, file_path: str) -> list[list[str]]:
        """Читает XLS как CSV (без реального парсинга бинарных данных)."""
        return self.read_csv(file_path, delimiter='\t')

    def read_file(self, file_path: str) -> str | list[list[str]]:
        """Автоматически определяет тип файла по расширению."""
        if file_path.endswith('.csv'):
            return self.read_csv(file_path)
        elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
            return self.read_xls(file_path)
        return self.read_txt(file_path)
    
def easy_input(prompt: str, input_type=str) -> any:
    """Упрощённый input с автоматическим преобразованием типа."""
    while True:
        user_input = input(prompt)
        try:
            return input_type(user_input)
        except ValueError:
            print(f"Ошибка! Введите значение типа {input_type.__name__}.")

def print_list(lst: list, numbered: bool = False) -> None:
    """Красивый вывод списка (с нумерацией)."""
    if numbered:
        for i, item in enumerate(lst, 1):
            print(f"{i}. {item}")
    else:
        print(*lst, sep='\n')
def simple_write(file_path: str, text: str, mode: str = 'w') -> None:
    """Запись в файл с автозакрытием и обработкой ошибок."""
    try:
        with open(file_path, mode, encoding='utf-8') as f:
            f.write(text)
    except IOError as e:
        print(f"Ошибка записи: {e}")

def ask_yes_no(question: str) -> bool:
    """Вопрос с ответом Да/Нет (возвращает True/False)."""
    while True:
        answer = input(f"{question} (Да/Нет): ").strip().lower()
        if answer in ('да', 'д', 'yes', 'y'):
            return True
        elif answer in ('нет', 'н', 'no', 'n'):
            return False
        print("Ошибка! Введите 'Да' или 'Нет'.")

