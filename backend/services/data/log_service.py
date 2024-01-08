import utils.ip_limiter
from datetime import datetime
from flask import Blueprint, Flask, current_app
from flask_restx import Api, Resource, fields, Namespace
import os

log_namespace = Namespace("log", description="Log operations")


def write_file(file, message):
    message = f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {message}'

    with open(
        os.path.join(
            current_app.config["ROOT_FOLDER"], current_app.config["LOG_FOLDER"], file
        ),
        "a",
    ) as f:
        f.write(message + "\n")


def write_error(message):
    write_file("error.log", message)


def write_database(query):
    write_file("database.log", query)


def write_external_api(message):
    write_file("external_api.log", message)


message = log_namespace.model(
    "Message",
    {
        "message": fields.String(required=True, description="The message to log"),
    },
)


@log_namespace.route("/error")
@log_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Log an error",
    params={"message": "The error message"},
)
class Error(Resource):
    @log_namespace.expect(message)
    @log_namespace.marshal_with(message)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        write_error(log_namespace.payload["message"])
        return "OK", 200


@log_namespace.route("/database")
@log_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Log a database query",
    params={"query": "The database query"},
)
class Database(Resource):
    @log_namespace.expect(message)
    @log_namespace.marshal_with(message)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        write_database(log_namespace.payload["message"])
        return "OK", 200


@log_namespace.route("/external_api")
@log_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Log an external API call",
    params={"message": "The external API call"},
)
class ExternalAPI(Resource):
    @log_namespace.expect(message)
    @log_namespace.marshal_with(message)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        write_external_api(log_namespace.payload["message"])
        return "OK", 200
