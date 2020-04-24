from datetime import datetime

from flask import request
from flask_restful import Resource, abort, marshal_with
from sqlalchemy.orm.exc import NoResultFound

from ..models.mail import Mail, Recipient
from ..models.database import db


class MailResource(Resource):

    @marshal_with(Mail.marshal_fields)
    def get(self, mail_id):
        try:
            mail = Mail.query.filter(Mail.id == mail_id).one()
        except NoResultFound as e:
            abort(404, message='Mail not found')

        return mail


class MailsResource(Resource):

    @marshal_with(Mail.marshal_fields)
    def get(self):
        return Mail.query.all()

    @marshal_with(Mail.marshal_fields)
    def post(self):
        if not request.is_json:
            abort(400, message='Provide valid JSON')

        data = request.get_json()

        mail = Mail(
            content=data['content'],
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

        data = request.get_json()

        recipient = Recipient(
            mail_id=mail.id,
            address=data['address'],
        )
        db.session.add(recipient)
        db.session.commit()
        return recipient
