from flask import abort, current_app, request
import os
import middleware.ip_limiter

# Copy a temporary file to the permanent location, return the permanent location
class FileAdapter:
    @current_app.route("/store-file", methods=["POST"])
    @middleware.ip_limiter.limit_ip_access
    def store_file():
        file = request.files["file"]
        try:
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], file.filename))
        except:
            abort(500)
        return file.filename

    @current_app.route("/get-file/<filename>", methods=["GET"])
    @middleware.ip_limiter.limit_ip_access
    def get_file(filename):
        try:
            file = open(
                os.path.join(current_app.config["UPLOAD_FOLDER"], filename), "rb"
            )
        except FileNotFoundError:
            abort(404)
        try:
            content = file.read()
        except:
            abort(500)
        file.close()
        return content
