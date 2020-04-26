#!/usr/bin/env python
from flask import Flask, Blueprint
from flask_restful import Api

from .models.database import db
from .services.mail import mail
from .resources.mail import MailResource, MailsResource
from .resources.mail import RecipientsResource
from .resources.mail import SendMailsResource


# configure blueprint
blueprint = Blueprint('api', __name__, url_prefix='/api')

# configure api
api = Api(blueprint)
api.add_resource(MailsResource, '/mails')
api.add_resource(SendMailsResource, '/mails/send')
api.add_resource(MailResource, '/mails/<int:mail_id>')
api.add_resource(RecipientsResource, '/mails/<int:mail_id>/recipients')


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('MAILER_SETTINGS')

    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()

    mail.init_app(app)

    app.register_blueprint(blueprint)
    return app
