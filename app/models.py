from datetime import datetime, timezone
from typing import Optional, List
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from app import db
from app import login


# Модель пользователя
class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    # Связь с другими таблицами
    grades: so.WriteOnlyMapped[List["Grade"]] = so.relationship("Grade", back_populates="user")
    schedules: so.WriteOnlyMapped[List["Schedule"]] = so.relationship("Schedule", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def __repr__(self):
        return f'<User {self.username}>'


# Модель расписания
class Schedule(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)
    day_of_week: so.Mapped[str] = so.mapped_column(sa.String(16))  # Например, "Понедельник"
    lesson_name: so.Mapped[str] = so.mapped_column(sa.String(128))
    start_time: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8))  # "08:00"
    end_time: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8))
    user: so.Mapped["User"] = so.relationship("User", back_populates="schedules")

    def __repr__(self):
        return f'<Schedule {self.lesson_name} for User {self.user_id}>'


# Модель оценок
class Grade(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)
    subject: so.Mapped[str] = so.mapped_column(sa.String(64))
    grade: so.Mapped[int] = so.mapped_column()
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user: so.Mapped["User"] = so.relationship("User", back_populates="grades")

    def __repr__(self):
        return f'<Grade {self.grade} for User {self.user_id}>'


# Модель библиотеки
class Library(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    author: so.Mapped[str] = so.mapped_column(sa.String(128))
    grade_level: so.Mapped[int] = so.mapped_column(index=True)  # Для какого класса
    url: so.Mapped[str] = so.mapped_column(sa.String(256))  # Ссылка на онлайн книгу

    def __repr__(self):
        return f'<Library Book {self.title}>'


# Модель видеоуроков
class TutorVideo(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    subject: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    topic: so.Mapped[str] = so.mapped_column(sa.String(128))
    url: so.Mapped[str] = so.mapped_column(sa.String(256))  # Ссылка на видеоурок

    def __repr__(self):
        return f'<TutorVideo {self.topic} ({self.subject})>'

@login.user_loader
def load_user(id):
  return db.session.get(User, int(id))