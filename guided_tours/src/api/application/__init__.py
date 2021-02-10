import logging
from http import HTTPStatus

from flask import Flask
from flask_restful import Api

from guided_tours_lib.validation.exceptions import ValidationException

from .models import db


def _add_api_resources(api):
    """Adds resources to REST api."""

    from .resources import (
        Ping,
        Root,
        Tours,
        TourAudio,
        TourImages,
        Users,
        UserLogin,
        UserLogout,
    )

    api.add_resource(Root, "/")
    api.add_resource(Users, "/users", "/users/", "/users/<string:username>")
    api.add_resource(Tours, "/tours", "/tours/", "/tours/<int:tour_id>")
    api.add_resource(TourAudio, "/tours/<int:tour_id>/audio")
    api.add_resource(TourImages, "/tours/<int:tour_id>/images/<int:image_number>")

    # The following endpoints are not strictly RESTful.
    # These endpoints involve commands and would be better suited to a RPC API, for example JSON-RPC
    api.add_resource(UserLogin, "/login")
    api.add_resource(UserLogout, "/logout")
    api.add_resource(Ping, "/ping")


def make_app():
    """Make the application."""

    # create the Flask app
    app = Flask(__name__)

    # parse the config file
    app.config.from_pyfile("../config/settings.conf")

    # set the api version from config
    version = app.config["API_VERSION"]

    # create api prefix for all routes
    prefix = f"/api/v{version}"

    # create the restful api object
    api = Api(app=app, prefix=prefix)

    # initialize the db for the app
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        """Create all db tables"""
        db.create_all()

    @app.errorhandler(ValidationException)
    def validation_error(error):
        """Response when ValidationException is raised."""
        return str(error), HTTPStatus.BAD_REQUEST

    @app.errorhandler(500)
    def internal_server_error(e):
        logging.error(str(e))
        return ("Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR)

    # add the api resources
    _add_api_resources(api)

    return app
