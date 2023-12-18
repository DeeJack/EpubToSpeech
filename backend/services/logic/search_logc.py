import io
from flask import Flask, request, current_app, make_response, send_file
from flask_restx import Api, Resource, abort, fields, Namespace
import requests 

search_namespace = Namespace("search", description="Search operations")

search_model = search_namespace.model(
    "Search",
    {
        "keywords": fields.String(
            required=True, description="The text to be searched"
        ),
    },
)


"""
    I don't even know what to do in this service
"""