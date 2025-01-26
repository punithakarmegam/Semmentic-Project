from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Importer flask_cors
import requests

app = Flask(__name__)

# ✅ Activer CORS pour toutes les routes
CORS(app)

FUSEKI_URL = "http://localhost:3030/entertainment/sparql"

@app.route("/proxy", methods=["POST"])
def proxy():
    query = request.form.get("query")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    response = requests.post(FUSEKI_URL, data={"query": query}, headers=headers)
    return response.json()

if __name__ == "__main__":
    app.run(port=5000)
