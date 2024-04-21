import argparse
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from task_manager.api.db import get_db_url
from task_manager.api.query import get_filtered_model_objects

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_url()
db = SQLAlchemy(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    model_name = request.args.get('modelName')
    filters = request.args.get('filters', {})
    fields = request.args.get('fields', '*')
    filters = json.loads(filters)
    results = get_filtered_model_objects(model_name, **filters)
    response_data = []
    for result in results:
        if fields == '*':
            response_data.append(result.__dict__)
        else:
            response_data.append({field: getattr(result, field) for field in fields})

    return jsonify(response_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Flask app: Video Search")
    parser.add_argument("--port", default=5001, type=int, help="port number")
    args = parser.parse_args()
    app.run(host="0.0.0.0", debug=True, port=args.port, use_reloader=True)