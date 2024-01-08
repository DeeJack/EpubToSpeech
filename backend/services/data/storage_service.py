from flask import Blueprint, Flask, current_app, request, send_file, make_response
from flask_restx import Api, Resource, fields, abort, Namespace
import utils.ip_limiter
import os


def save_file(file, filename):
    if os.path.basename(filename) != filename:
        abort(400)
    file.save(
        os.path.join(
            current_app.config["ROOT_FOLDER"],
            current_app.config["UPLOAD_FOLDER"],
            filename,
        )
    )


def get_file(filename):
    if os.path.basename(filename) != filename:
        abort(400)
    try:
        filepath = os.path.join(
            current_app.config["ROOT_FOLDER"],
            current_app.config["UPLOAD_FOLDER"],
            filename,
        )
        return send_file(filepath, as_attachment=True)
    except UnicodeDecodeError as e:
        abort(500)
    except FileNotFoundError as e:
        print(e)
        abort(404)
    except:
        abort(500)


storage_namespace = Namespace("storage", description="Filesystem operations")

file = storage_namespace.model(
    "file",
    {
        "file": fields.String(required=True, description="The file to store"),
        "filename": fields.String(
            required=True, description="The name of the file to store"
        ),
    },
)

from werkzeug.datastructures import FileStorage

upload_parser = storage_namespace.parser()
upload_parser.add_argument("file", location="files", type=FileStorage, required=True)
upload_parser.add_argument("filename", location="form", type=str, required=True)


@storage_namespace.route("/store-file")
@storage_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Store a file",
    params={"file": "The file to store", "filename": "The name of the file to store"},
)
class StoreFile(Resource):
    # @storage_namespace.expect(file)
    # @storage_namespace.marshal_with(file)
    @storage_namespace.expect(upload_parser)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args["file"]
        if uploaded_file is None:
            print("No file")
            abort(400, "No file part")
        if "filename" not in request.form:
            print("NO FILENAME")
            abort(400, "No filename part")

        file = request.files["file"]
        filename = request.form["filename"]

        save_file(file, filename)
        return "OK", 200


@storage_namespace.route("/get-file/<string:filename>")
@storage_namespace.doc(
    responses={200: "OK", 400: "Invalid Argument", 500: "Mapping Key Error"},
    description="Get a file",
    params={"filename": "The path of the file to get"},
)
class GetFile(Resource):
    @utils.ip_limiter.limit_ip_access
    def get(self, filename):
        return get_file(filename)
