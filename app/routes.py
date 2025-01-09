from urllib.parse import urlsplit
from flask import abort, flash, redirect, render_template, request, url_for, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required

import sqlalchemy as sa
from app import app
from app.forms import LoginForm
from app import db
from app.forms import RegistrationForm
from app.models import User
from app.utils import READING_LISTS

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
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    grades = [
        {'student': user, 'subject': 'Test grade 4'},
        {'student': user, 'subject': 'Test post 5'}
    ]
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
