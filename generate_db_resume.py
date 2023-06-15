import logging
from src.handler.save_db_resume.handler import handler

logging.basicConfig(
    level=logging.DEBUG,
    filename='save_db_resume.log',
    format='%(name)s - %(levelname)s - %(message)s',
)


if __name__ == '__main__':
    print(handler())
