from app import app
from app.models import User, Post
from app import db


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Post=Post)
