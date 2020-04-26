from datetime import datetime

from colander import Invalid
from flask import request
from flask_mail import Message
from flask_restful import Resource, abort, marshal_with
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from ..models.mail import Mail, MailStates, Recipient
from ..models.database import db
from ..schemas.mail import (
    MailCreateSchema,
    MailUpdateSchema,
    RecipientCreateSchema,
)
from ..services.mail import mail


class MailResource(Resource):

    @marshal_with(Mail.marshal_fields)
    def get(self, mail_id):
        try:
            mail = Mail.query.filter(Mail.id == mail_id).one()
        except NoResultFound as e:
            abort(404, message='Mail not found')

        return mail

    @marshal_with(Mail.marshal_fields)
    def post(self, mail_id):
        try:
            mail = Mail.query.filter(Mail.id == mail_id).one()
        except NoResultFound as e:
            abort(404, message='Mail not found')

        if not request.is_json:
            abort(400, message='Provide valid JSON')

        document = request.get_json()
        schema = MailUpdateSchema()
        try:
            data = schema.deserialize(document)
        except Invalid as e:
            abort(400, errors=e.asdict())

        mail.content = data.get('content', mail.content)
        mail.address = data.get('address', mail.address)
        mail.name = data.get('name', mail.name)
        db.session.add(mail)
        db.session.commit()
        return mail


class MailsResource(Resource):

    @marshal_with(Mail.marshal_fields)
    def get(self):
        return Mail.query.all()

    @marshal_with(Mail.marshal_fields)
    def post(self):
        if not request.is_json:
            abort(400, message='Provide valid JSON')

        document = request.get_json()
        schema = MailCreateSchema()
        try:
            data = schema.deserialize(document)
        except Invalid as e:
            abort(400, errors=e.asdict())

        mail = Mail(
            content=data['content'],
            address=data.get('address', None),
            name=data.get('name', None),
        )
        db.session.add(mail)
        db.session.commit()
        return mail


class RecipientsResource(Resource):

    @marshal_with(Recipient.marshal_fields)
    def post(self, mail_id):
        try:
            mail = Mail.query.filter(Mail.id == mail_id).one()
        except NoResultFound as e:
            abort(404, message='Mail not found')

        if not request.is_json:
            abort(400, message='Provide valid JSON')

        document = request.get_json()
        schema = RecipientCreateSchema()
        try:
            data = schema.deserialize(document)
        except Invalid as e:
            abort(400, errors=e.asdict())

        try:
            recipient = Recipient(
                mail_id=mail.id,
                address=data['address'],
                name=data.get('name', None),
            )
            db.session.add(recipient)
            db.session.commit()
        except IntegrityError as e:
            abort(409, message='Recipient already exists')

        return recipient


class SendMailsResource(Resource):

    @marshal_with(Mail.marshal_fields)
    def post(self):
        mails = Mail.query.filter(Mail.state == MailStates.PENDING).all()
        for entity in mails:
            if entity.recipients:
                message = Message(
                    subject=None,
                    body=entity.content,
                    sender=(
                        (entity.name, entity.address) if entity.name else\
                        entity.address
                    ),
                    recipients=[
                        (item.name, item.address) if item.name else\
                        item.address
                        for item in entity.recipients
                    ]
                )
                mail.send(message)
                entity.state = MailStates.SENT
                db.session.add(entity)

        db.session.commit()
        return mails
