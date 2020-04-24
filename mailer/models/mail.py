from datetime import datetime

from flask_restful import fields
from sqlalchemy import UniqueConstraint

from .database import db


class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    marshal_fields = dict(
        id=fields.Integer,
        content=fields.String,
        created_at=fields.DateTime,
        recipients=fields.List(fields.String),
    )


class Recipient(db.Model):
    __table_args__ = (
        db.UniqueConstraint('mail_id', 'address', name='unique_address'),
    )

    id = db.Column(db.Integer, primary_key=True)
    mail_id = db.Column(db.Integer, db.ForeignKey('mail.id'), nullable=False)
    mail = db.relationship('Mail', backref=db.backref('recipients', lazy=True))
    address = db.Column(db.String(255), nullable=False)

    marshal_fields = dict(
        id=fields.Integer,
        mail_id=fields.Integer,
        address=fields.String,
    )

    def __str__(self):
        return "{}".format(self.address)
