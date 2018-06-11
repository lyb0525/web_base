#!encoding=utf-8

# from fluent.sender import FluentSender
from flask_wtf.csrf import CsrfProtect
from flask.ext.sqlalchemy import SQLAlchemy

# from app.celery import celery

csrf = CsrfProtect()

db = SQLAlchemy(session_options={'autocommit': False, 'autoflush': False})

