from urllib.parse import urlsplit
from flask import abort, flash, redirect, render_template, request, url_for, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required

from app import app
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import User
from app.utils import READING_LISTS, add_user, get_grades_for_user, get_user_by_username, read_data

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home page')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user_data = get_user_by_username(form.username.data)  # Получаем данные пользователя из JSON
        if user_data is None or user_data['password'] != form.password.data:  # Замените на хеширование!
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        # Преобразуем словарь в объект User
        user = User.from_dict(user_data)
        
        # Вход пользователя
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        data = read_data()
        if get_user_by_username(form.username.data):
            flash('Username already exists')
            return redirect(url_for('register'))
        user = {
            'username': form.username.data,
            'email': form.email.data,
            'password': form.password.data  # В реальном проекте используйте хеширование!
        }
        add_user(user)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = get_user_by_username(username)
    if not user:
        abort(404, description="User not found")
    
    grades = get_grades_for_user(username)
    return render_template('user.html', user=user, grades=grades)



@app.route('/protected/<page>')
@login_required
def protected_route(page):
    if not current_user.is_authenticated:
        flash('Пожалуйста, войдите для доступа к этой странице.')
        return redirect(url_for('login'))
    
    if page == 'library':
        return render_template('library.html')
    elif page == 'tutor':
        return render_template('tutor.html')
    elif page == 'leto':
        return render_template('leto.html', reading_lists=READING_LISTS)
    
    return redirect(url_for('index'))


@app.route('/library/class/<int:class_num>')
@login_required
def library_class(class_num):
    if class_num < 1 or class_num > 11:
        flash('Некорректный номер класса')
        return redirect(url_for('protected_route', page='library'))
    return render_template('library_class.html', class_num=class_num)

@app.route('/book/<path:filename>')
@login_required
def serve_book(filename):
    try:
        return send_from_directory(app.config['PDF_FOLDER'], filename)
    except FileNotFoundError:
        abort(404, description="Файл не найден")

@app.route('/tutor/<subject>')
@login_required
def tutor_subject(subject):
    return render_template('tutor.html', subject=subject)

@app.route('/leto/class/<int:class_num>')
@login_required
def leto_class(class_num):
    if class_num < 1 or class_num > 11:
        flash('Некорректный номер класса')
        return redirect(url_for('protected_route', page='leto'))
    
    reading_list = READING_LISTS.get(class_num, [])
    return render_template('leto.html', 
                         selected_class=class_num,
                         reading_list=reading_list)
