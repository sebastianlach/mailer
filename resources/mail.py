from datetime import datetime
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from models.mail import Mail
from models.database import db


class MailResource(Resource):

    def get(self, mail_id):
        try:
            mail = Mail.query.filter(id==mail_id).one()
        except NoResultFound as e:
            abort(404, message='Mail not found')

        return {
            'content': '{}'.format(mail.content),
        }


class MailsResource(Resource):

    def get(self):
        mails = Mail.query.all()
        return [
            {
                'content': '{}'.format(mail.content),
            }
            for mail in mails
        ]
