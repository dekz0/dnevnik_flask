from flask import render_template
from app import app

@app.errorhandler(404)
def not_found_error(error):
    # Обработка ошибки 404 (страница не найдена)
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    # Обработка ошибки 500 (внутренняя ошибка сервера)
    # Здесь можно добавить логику логирования, если это требуется
    return render_template('500.html'), 500
