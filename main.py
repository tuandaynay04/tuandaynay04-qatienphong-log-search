import os
from flask import Flask, request
from google.cloud import firestore
from flask_cors import CORS # Dòng mới

app = Flask(__name__)
CORS(app) # Dòng mới - cho phép cross-origin requests

# Kết nối vào đúng DATABASE 'searchlog'
db = firestore.Client(database='searchlog')

@app.route("/", methods=["POST"])
def log_search_term():
    request_json = request.get_json(silent=True)
    term = request_json.get('term') if request_json else None

    if not term:
        return 'Missing term', 400

    db.collection('search_logs').add({
        'term': term,
        'timestamp': firestore.SERVER_TIMESTAMP
    })
    return 'OK', 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
