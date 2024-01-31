from flask import Flask, jsonify, request
from core_client import Client  # Import the datarhei Core PyClient

app = Flask(__name__)
base_url = "http://127.0.0.1:8080"
username = "admin"
password = "groovy"

# Initialize the datarhei Core PyClient
core_client = Client(base_url=base_url, username=username, password=password)

# Get token data
@app.route('/get_token_data', methods=['GET'])
def get_token_data():
    token = core_client.login()
    return jsonify({'token': token})

# Get processes
@app.route('/get_processes', methods=['GET'])
def get_processes():
    process_list = core_client.v3_process_get_list()
    processes = [process.id for process in process_list]
    return jsonify({'processes': processes})

# Get a single processes
@app.route('/get_process/<process_id>', methods=['GET'])
def get_process(process_id):
    try:
        process = core_client.v3_process_get(id=process_id)
        return jsonify({'process': process})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return an error response with status code 500

# Create a new process
@app.route('/create_process', methods=['POST'])
def create_process():
    try:
        process_config = request.json  # Access the JSON payload from the request
        post_process = core_client.v3_process_post(config=process_config)
        return jsonify({'result': 'Process created successfully -- '} + post_process)
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Return an error response with status code 400

# Delete a process
@app.route('/delete_process/<process_id>', methods=['DELETE'])
def delete_process(process_id):
    try:
        delete_response = core_client.v3_process_delete(id=process_id)
        return jsonify({'result': 'Process deleted successfully -- '} + delete_response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Return an error response with status code 400

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Make the API accessible over the internet