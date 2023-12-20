import io
from flask import Flask, request, current_app, make_response, send_file
from flask_restx import Api, Resource, abort, fields, Namespace
import requests 
import utils.ip_limiter

gptlogic_namespace = Namespace("gptlogic", description="GPT Logic operations")

"""
    Handles stuff related to gpt:
        - Summarize the text
        - Translated the text
        - Generate a text based on a prompt
        - Generate image
"""

text_model = gptlogic_namespace.model(
    "Text",
    {
        "text": fields.String(
            required=True, description="The text to be processed"
        ),
    },
)

generate_model = gptlogic_namespace.model(
    "Generate",
    {
        "prompt": fields.String(
            required=True, description="The prompt to be processed"
        ),
    },
)

@gptlogic_namespace.route("/summarize")
@gptlogic_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Summarize the text', params={'text': 'The text to be summarized'})
class Summarize(Resource):
    @gptlogic_namespace.expect(text_model)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        """
            Summarize the text
        """
        text = request.json["text"]
        if len(text) > 1000:
            abort(400, "Text too long")
        response = requests.post(f'{current_app.config["API_URL"]}/openai/text-generation', json={
                'pre_prompt': 'Summarize the text given',
                'prompt': text
            })
        if response.status_code != 200:
            return abort(response.status_code, response.json()['message'])
        return response.json()
    
@gptlogic_namespace.route("/translate")
@gptlogic_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Translate the text', params={'text': 'The text to be translated'})
class Translate(Resource):
    @gptlogic_namespace.expect(text_model)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        """
            Translate the text
        """
        text = request.json["text"]
        if len(text) > 1000:
            abort(400, "Text too long")
        response = requests.post(f'{current_app.config["API_URL"]}/openai/text-generation', json={
                'pre_prompt': 'Translate the text given in english',
                'prompt': text
            })
        if response.status_code != 200:
            return abort(response.status_code, response.json()['message'])
        return response.json()
    
@gptlogic_namespace.route("/generate")
@gptlogic_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Generate text from prompt', params={'prompt': 'The prompt for GPT', 'text': 'The text to be processed'})
class Generate(Resource):
    @gptlogic_namespace.expect(generate_model)
    @gptlogic_namespace.expect(text_model)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        """
            Generate text from prompt
        """
        prompt = request.json["prompt"]
        text = request.json["text"]
        
        if len(text) + len(prompt) > 2000:
            return abort(400, "Text too long")
        
        response = requests.post(f'{current_app.config["API_URL"]}/openai/text-generation', json={
                'prompt': text,
                'pre_prompt': prompt
            })
        if response.status_code != 200:
            return abort(response.status_code, response.json()['message'])
        return response.json()

@gptlogic_namespace.route("/image")
@gptlogic_namespace.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, description='Generate image from prompt', params={'text': 'The prompt to be processed'})
class Image(Resource):
    @gptlogic_namespace.expect(text_model)
    @utils.ip_limiter.limit_ip_access
    def post(self):
        """
            Generate image from prompt
        """
        text = request.json["text"]
        
        if len(text) > 1000:
            abort(400, "Text too long")
        
        response = requests.post(f'{current_app.config["API_URL"]}/openai/image-generation', json={
                'text': text
            })
        if response.status_code != 200:
            return abort(response.status_code, response.json()['message'])
        return response.json()