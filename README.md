# Как запустить проект?

1. Установите git и python
2. Если скачали zip файл, то расспаковываем его и заходим в папку распакованную.
3. Если хотите скачать с git то в командой строке вводим по очереди каждую строку:
```bash
   git clone https://github.com/dekz0/dnevnik_flask
   cd dnevnik_flask
```
4. Настройка питона, то есть виртуальной среды:
```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```
5. Установка библиотек:
```bash
pip install -r requirements.txt
```
6. Запуск сервера:
```bash
flask run
```
Откройте приложение в своем браузере по адресу http://127.0.0.1:5000
