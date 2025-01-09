import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Schedule, Grade, Library, TutorVideo

@app.shell_context_processor
def make_shell_context():
  return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Grade': Grade, 'Shedule': Schedule, 'Library': Library, 'TutorVideo': TutorVideo}