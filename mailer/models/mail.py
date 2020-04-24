from datetime import datetime

from flask_restful import fields

from .database import db


class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    marshal_fields = dict(
        id=fields.Integer,
        content=fields.String,
        created_at=fields.DateTime,
    )
