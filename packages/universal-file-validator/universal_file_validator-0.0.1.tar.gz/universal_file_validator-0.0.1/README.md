# File Validator

[![PyPI version](https://img.shields.io/pypi/v/universal-file-validator.svg)](https://pypi.org/project/universal-file-validator/)
[![Build Status](https://github.com/DenisShahbazyan/File_Validator/actions/workflows/publish.yml/badge.svg)](https://github.com/DenisShahbazyan/File_Validator/actions)
[![Python Versions](https://img.shields.io/pypi/pyversions/universal-file-validator.svg)](https://pypi.org/project/universal-file-validator/)
[![License](https://img.shields.io/pypi/l/universal-file-validator.svg)](https://github.com/DenisShahbazyan/File_Validator/blob/master/LICENSE)

# Библиотека для валидации файлов

Библиотека предоставляет упрощенный интерфейс для валидации файлов.

## Основные возможности:
- Валидация по размеру
- Валидация по расширению
- Валидация по Mime типу

## Установка:
```sh
pip install universal-file-validator
```
После установки валидатора файлов необходимо установить libmagic, для чего вам нужно выполнить следующую команду:
- Windows:
```sh
pip install python-magic-bin
```
- Debian/Ubuntu:
```sh
sudo apt-get install libmagic1
```
- MacOS:
```sh
brew install libmagic
```

## Использование:

### Перед началом нужно создать экземпляр класса:
Словарь `image_types` можно не передавать только для валидации по размеру, для всех остальных валидаций он необходим.
```py
image_types = {
    'image/jpeg': ['jpg', 'jpeg'],
    'image/jpg': ['jpg', 'jpeg'],
    'image/png': ['png'],
}

vc = FileValidator(
    max_size=1000,
    size_unit='килобайт',
    allowed_types=image_types,
    is_validate_extension=True,
    is_validate_mime_type=True,
    is_cross_validation=True,
)
```
Подробнее об аргументах:

- `max_size (int)`: Максимальный размер файла в указанных единицах измерения.
    При значении 0 валидация размера отключена. По умолчанию 0.
- `size_unit (SizeUnit | str)`: Единица измерения для max_size.
    Может быть SizeUnit enum или строкой ('B', 'KB', 'MB', 'GB', 'bytes',
    'kilobytes', 'megabytes', 'gigabytes'). Поддерживает русские названия
    ('байт', 'килобайт', 'мегабайт', 'гигабайт'). По умолчанию
    SizeUnit.BYTES.
- `allowed_types (dict[str, list[str]])`: Словарь разрешенных
    MIME типов и соответствующих им расширений файлов. Ключ - MIME тип
    (например, 'image/jpeg'), значение - список разрешенных расширений
    (например, ['jpg', 'jpeg']). При значении None валидация MIME типов,
    расширений и перекрестная валидация отключена. По умолчанию None.
    Пример:
    ```
    {
        'image/jpeg': ['jpg', 'jpeg'],
        'image/png': ['png'],
    }
    ```
- `is_validate_extension (bool)`: Включить валидацию расширений файлов.
    Работает только при предоставленном allowed_types. Проверяет, что у файла
    есть расширение и оно находится в списке разрешенных. По умолчанию True.
- `is_validate_mime_type (bool)`: Включить валидацию MIME типов файлов.
    Работает только при предоставленном allowed_types. Проверяет, что у файла
    есть MIME тип и он находится в списке разрешенных. По умолчанию True.
- `is_cross_validation (bool)`: Включить перекрестную валидацию расширения файла
    с его MIME типом. Работает только при предоставленном allowed_types.
    Проверяет, что расширение файла соответствует указанному
    MIME типу. По умолчанию True.


### Можно валидировать по отдельности:
```py
from file_validator import FileValidator

image_types = {
    'image/jpeg': ['jpg', 'jpeg'],
    'image/jpg': ['jpg', 'jpeg'],
    'image/png': ['png'],
}

vc = FileValidator(
    max_size=1000,
    size_unit='килобайт',
    allowed_types=image_types,
)

file_name = 'image.jpeg'

with open(file_name, 'rb') as f:
    file_content = f.read()

vc.validate_size(file_content)

extension = vc.validate_extension_exists(file_name)
vc.validate_extension_allowed(extension)

mime_type = vc.detect_mime_type(file_content)  # Так же есть асинхронный метод adetect_mime_type()
vc.validate_mime_type_allowed(mime_type)

vc.validate_extension_mime_match(extension, mime_type)

print(f'{extension=}')
print(f'{mime_type=}')
```

- Если какая-то валидация будет провалена, вызовется исключение.

### Можно валидировать всё сразу:
```py
from file_validator import FileValidator

image_types = {
    'image/jpeg': ['jpg', 'jpeg'],
    'image/jpg': ['jpg', 'jpeg'],
    'image/png': ['png'],
}

vc = FileValidator(
    max_size=1000,
    size_unit='килобайт',
    allowed_types=image_types,
)

file_name = 'image.jpeg'

with open(file_name, 'rb') as f:
    file_content = f.read()

extension, mime_type = vc.validate_all(file_content, file_name)  # Так же есть асинхронный метод avalidate_all()
print(f'{extension=}')
print(f'{mime_type=}')
```


## Запуск локально (для разработки):
Установка зависимостей
```sh
pip install -r requirements.txt
```
После установки валидатора файлов необходимо установить libmagic, для чего вам нужно выполнить следующую команду:
- Windows:
```sh
pip install python-magic-bin
```
- Debian/Ubuntu:
```sh
sudo apt-get install libmagic1
```
- MacOS:
```sh
brew install libmagic
```


Запуск примеров:
```sh
python -m example.validator_steps
python -m example.validator_all
```

