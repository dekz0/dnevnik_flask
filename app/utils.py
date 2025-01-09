import json
import os


READING_LISTS = {
    5: [
        {"title": "Руслан и Людмила", "author": "А.С. Пушкин"},
        {"title": "Кавказский пленник", "author": "Л.Н. Толстой"},
        {"title": "Дети капитана Гранта", "author": "Жюль Верн"},
        {"title": "Белый клык", "author": "Джек Лондон"},
        {"title": "Приключения Гекльберри Финна", "author": "Марк Твен"}
    ],
    6: [
        {"title": "Легенды и мифы древней Греции", "author": "Н.А. Кун"},
        {"title": "Метель", "author": "А.С. Пушкин"},
        {"title": "Левша", "author": "Н.С. Лесков"},
        {"title": "Ночь перед Рождеством", "author": "Н.В. Гоголь"},
        {"title": "Хоббит, или Туда и Обратно", "author": "Д.Р.Р. Толкиен"}
    ],
    7: [
        {"title": "Дубровский", "author": "А.С. Пушкин"},
        {"title": "Тарас Бульба", "author": "Н.В. Гоголь"},
        {"title": "Детство", "author": "Л.Н. Толстой"},
        {"title": "Алые паруса", "author": "А. Грин"},
        {"title": "Властелин колец", "author": "Д.Р.Р. Толкиен"}
    ],
    8: [
        {"title": "Капитанская дочка", "author": "А.С. Пушкин"},
        {"title": "Ревизор", "author": "Н.В. Гоголь"},
        {"title": "После бала", "author": "Л.Н. Толстой"},
        {"title": "Василий Теркин", "author": "А.Т. Твардовский"},
        {"title": "Война миров", "author": "Г. Уэллс"}
    ],
    9: [
        {"title": "Евгений Онегин", "author": "А.С. Пушкин"},
        {"title": "Мертвые души", "author": "Н.В. Гоголь"},
        {"title": "Герой нашего времени", "author": "М.Ю. Лермонтов"},
        {"title": "Отцы и дети", "author": "И.С. Тургенев"},
        {"title": "Преступление и наказание", "author": "Ф.М. Достоевский"}
    ],
    10: [
        {"title": "Война и мир", "author": "Л.Н. Толстой"},
        {"title": "Гроза", "author": "А.Н. Островский"},
        {"title": "Обломов", "author": "И.А. Гончаров"},
        {"title": "Вишневый сад", "author": "А.П. Чехов"},
        {"title": "Мастер и Маргарита", "author": "М.А. Булгаков"}
    ],
    11: [
        {"title": "Тихий Дон", "author": "М.А. Шолохов"},
        {"title": "Доктор Живаго", "author": "Б.Л. Пастернак"},
        {"title": "Один день Ивана Денисовича", "author": "А.И. Солженицын"},
        {"title": "Архипелаг ГУЛАГ", "author": "А.И. Солженицын"},
        {"title": "Колымские рассказы", "author": "В.Т. Шаламов"}
    ]
}


DATA_FILE = 'data.json'

def read_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_user_by_username(username):
    data = read_data()
    return next((u for u in data.get('users', []) if u['username'] == username), None)

def add_user(user):
    data = read_data()
    if 'users' not in data:
        data['users'] = []
    data['users'].append(user)
    write_data(data)

def get_grades_for_user(username):
    data = read_data()
    return [g for g in data.get('grades', []) if g['student'] == username]
