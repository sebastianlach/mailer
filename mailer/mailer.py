#!/usr/bin/env python
from flask import Flask, Blueprint
from flask_restful import Api

from .models.database import db
from .resources.mail import MailResource, MailsResource
from .resources.mail import RecipientsResource


# configure blueprint
blueprint = Blueprint('api', __name__, url_prefix='/api')

# configure api
api = Api(blueprint)
api.add_resource(MailsResource, '/mail')
api.add_resource(MailResource, '/mail/<int:mail_id>')
api.add_resource(RecipientsResource, '/mail/<int:mail_id>/recipient')


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('MAILER_SETTINGS')

    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()

    app.register_blueprint(blueprint)
    return app
