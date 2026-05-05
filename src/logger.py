from helpers import caminho_log, data_arquivo, data_registro
import os

LOG_DIR = caminho_log()

# Arquivo único por execução
log_filename = f"{data_arquivo()}.log"
log_path = LOG_DIR / log_filename


def log(level, message, module):
    timestamp = data_registro()

    formatted_message = (
        f"{timestamp} | {level.upper():<7} | {module:<10} | {message}\n"
    )

    with open(log_path, "a", encoding="utf-8") as file:
        file.write(formatted_message)


# print(data_arquivo())
# print(data_registro())



