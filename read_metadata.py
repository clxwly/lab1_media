"""
Скрипт для чтения метаданных аудиофайлов (MP3, WAV).
Вариант 1: исполнитель, альбом, год (+ длительность, битрейт, частота).
Использование: python read_metadata.py <файл>
"""

import os
import sys

from mutagen.mp3 import MP3
from mutagen.wave import WAVE

SUPPORTED_EXTENSIONS = ('.mp3', '.wav')
NOT_FOUND = "не указано"


def get_text_tag(tags, *keys):
    """Возвращает текст первого найденного ID3-тега из списка keys."""
    if tags is None:
        return NOT_FOUND
    for key in keys:
        if key in tags and tags[key].text:
            return str(tags[key].text[0])
    return NOT_FOUND


def read_audio_metadata(file_path):
    """
    Читает метаданные аудиофайла (MP3, WAV).

    :param file_path: путь к файлу
    :return: словарь с метаданными
    :raises ValueError: если файл повреждён или не соответствует формату
    """
    ext = os.path.splitext(file_path)[1].lower()

    # Открываем файл подходящим классом mutagen
    try:
        audio = MP3(file_path) if ext == '.mp3' else WAVE(file_path)
    except Exception as e:
        raise ValueError(
            f"файл повреждён или не соответствует формату {ext}: {e}"
        )

    # Год: в ID3v2.4 тег TDRC, в ID3v2.3 тег TYER
    year = get_text_tag(audio.tags, 'TDRC', 'TYER')
    if year != NOT_FOUND:
        year = year[:4]

    metadata = {
        "Исполнитель": get_text_tag(audio.tags, 'TPE1'),
        "Альбом": get_text_tag(audio.tags, 'TALB'),
        "Год": year,
        "Длительность": f"{audio.info.length:.2f} сек",
        # mutagen отдаёт битрейт в бит/с, переводим в кбит/с
        "Битрейт": f"{audio.info.bitrate // 1000} кбит/с",
        "Частота дискретизации": f"{audio.info.sample_rate} Гц",
    }
    return metadata


def main():
    """Основная функция."""
    if len(sys.argv) < 2:
        print("Использование: python read_metadata.py <файл>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Проверка 1: файл существует
    if not os.path.isfile(file_path):
        print(f"Ошибка: файл не найден: {file_path}")
        sys.exit(1)

    # Проверка 2: поддерживаемый формат
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        print(f"Ошибка: неверный формат '{ext}'. Поддерживаются: MP3, WAV")
        sys.exit(1)

    # Проверка 3: файл читается (не повреждён)
    try:
        metadata = read_audio_metadata(file_path)
    except ValueError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

    print(f"Метаданные для {file_path}:")
    for key, value in metadata.items():
        print(f"  {key}: {value}")


if __name__ == '__main__':
    main()