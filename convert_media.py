"""
Скрипт для конвертации аудио WAV -> MP3 с помощью FFmpeg.
Вариант 1.
Использование: python convert_media.py <входной.wav> <выходной.mp3>
"""

import os
import shutil
import subprocess
import sys


def check_ffmpeg():
    """Проверяет наличие FFmpeg в системе. Если не найден, завершает работу."""
    if shutil.which('ffmpeg') is None:
        print("Ошибка: FFmpeg не найден в PATH. Установите его: brew install ffmpeg")
        sys.exit(1)


def convert_file(input_path, output_path):
    """
    Конвертирует WAV в MP3 с помощью FFmpeg.

    :param input_path: путь к исходному файлу (.wav)
    :param output_path: путь к выходному файлу (.mp3)
    :return: True при успехе, False при ошибке
    """
    # -y: перезаписать выходной файл, libmp3lame: MP3-кодек, 192k: битрейт
    cmd = ['ffmpeg', '-i', input_path,
           '-codec:a', 'libmp3lame', '-b:a', '192k',
           '-y', output_path]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        # Последняя строка stderr обычно содержит причину ошибки
        lines = result.stderr.strip().splitlines()
        reason = lines[-1] if lines else "неизвестная ошибка"
        print(f"Ошибка FFmpeg: {reason}")
        # Удаляем недописанный выходной файл, если он остался
        if os.path.exists(output_path):
            os.remove(output_path)
        return False
    return True


def main():
    """Основная функция."""
    if len(sys.argv) < 3:
        print("Использование: python convert_media.py <входной.wav> <выходной.mp3>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Проверка 1: FFmpeg установлен
    check_ffmpeg()

    # Проверка 2: входной файл существует
    if not os.path.isfile(input_path):
        print(f"Ошибка: файл не найден: {input_path}")
        sys.exit(1)

    # Проверка 3: форматы соответствуют варианту (WAV -> MP3)
    if os.path.splitext(input_path)[1].lower() != '.wav':
        print("Ошибка: входной файл должен быть в формате WAV")
        sys.exit(1)
    if os.path.splitext(output_path)[1].lower() != '.mp3':
        print("Ошибка: выходной файл должен иметь расширение .mp3")
        sys.exit(1)

    # Конвертация
    if convert_file(input_path, output_path):
        size_kb = os.path.getsize(output_path) / 1024
        print(f"Конвертация завершена: {output_path} ({size_kb:.1f} КБ)")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()