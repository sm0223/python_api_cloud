import functions_framework
from flask import Flask, request, jsonify
import json
import logging
import xsdata
from xsdata.formats.dataclass.parsers import XmlParser, JsonParser
import dataclasses
import traceback
import requests

from mpp import Mpp
from rules import runRule

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# In-memory storage for demo purposes
data_store = []

@app.route('/', methods=['GET'])
def hello():
    """Basic GET endpoint"""
    return jsonify({
        'message': 'Hello from Flask on Google Cloud Functions!',
        'status': 'success',
        'endpoints': {
            'GET /': 'This endpoint',
            'POST /bre033': 'Mortgage Pricing',
        }
    })


@app.route('/bre033', methods=['POST'])
def bre033():
    """POST endpoint to create a new item"""
    try:
        logger.info(type(request.data))
        

        #----------------------------------------PARSE REQUEST-------------------------------------
        parser = JsonParser()
        if not request.is_json:
            mpp = parser.from_string(request.data.decode("utf-8"), Mpp)
        else :            
            mpp = parser.from_string(request.data.decode("utf-8"), Mpp)

        # ----------------------------------------RUN RULES----------------------------------------
        mpp.result = runRule(mpp)     
        # ----------------------------------------CALL DIFFERENT SERVICE---------------------------
        # TODO: CALL TEST2

        # ----------------------------------------RETURN RESPONSE----------------------------------
        return jsonify({
            'status': 'success',
            'message': 'Item created successfully',
            'data': dataclasses.asdict(mpp)
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating item: {str(e)}")
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

# Register the Flask app with Functions Framework
@functions_framework.http
def main(request):
    """Main entry point for Google Cloud Functions"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()