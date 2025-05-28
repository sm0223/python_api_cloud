import functions_framework
from flask import Flask, request, jsonify
import json
import logging
import xsdata
from xsdata.formats.dataclass.parsers import XmlParser
from mpp import Mpp

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
            'POST /bre034': 'Mortgage Processing',
            'PUT /bre/addFunction': 'Add new Function',
            'DELETE /bre/deleteFunction': 'Delete Function'
        }
    })


@app.route('/bre033', methods=['POST'])
def bre033():
    """POST endpoint to create a new item"""
    try:
        parser = XmlParser()
    
        mpp_ob = {}
        # Get JSON data from request
        if not request.is_json:
            mpp_ob = parser.from_string(request.data, Mpp)
        else :            
            mpp_ob = request.get_json()
        
        logger.info(mpp_ob)
        logger.info(type(mpp_ob))
        logger.info(mpp_ob['Mpp'])

        logger.info(mpp_ob['Mpp']['Application'])
        logger.info(mpp_ob['Mpp']['Application']['Array_of_Applicant'])
        logger.info(mpp_ob['Mpp']['Application']['Array_of_Applicant'][0]['Applicant']['Name'])

        # TODO: CALL THE RESPECTIVE BRE 



        return jsonify({
            'status': 'success',
            'message': 'Item created successfully',
            'data': json.dumps(mpp),
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating item: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500



@app.route('/bre034', methods=['POST'])
def bre034():
    """POST endpoint to create a new item"""
    try:
        data = ""
        # Get JSON data from request
        if not request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'Request must be JSON'
            }), 400
        else :            
            data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Name field is required',
                'data':data
            }), 400
        data.name = "afadsf";



        # TODO: CALL THE RESPECTIVE BRE
        logger.info(f"BRE PROCESSING DONE")
        
        return jsonify({
            'status': 'success',
            'message': 'Item created successfully',
            'data': data
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating item: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
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