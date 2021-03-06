from datetime import datetime
from enum import Enum

from flask_restful import fields
from sqlalchemy import UniqueConstraint

from .database import db


class MailStates(Enum):
    PENDING = 'pending'
    SENT = 'sent'


class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=False)
    state = db.Column(db.Enum(MailStates), default=MailStates.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    address = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)

    marshal_fields = dict(
        id=fields.Integer,
        content=fields.String,
        state=fields.String,
        address=fields.String,
        name=fields.String,
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
    name = db.Column(db.String(255), nullable=True)

    marshal_fields = dict(
        id=fields.Integer,
        mail_id=fields.Integer,
        address=fields.String,
        name=fields.String,
    )

    def __str__(self):
        return "{}".format(self.address)
