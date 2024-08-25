from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from spark_jira_tools import Jira

app = Flask(__name__)
CORS(app)  # Permitir solicitudes CORS

@app.route('/validate', methods=['POST'])
def validate():
    username = request.json.get("username")
    token = request.json.get("token")
    hut = request.json.get("hut")

    jira = Jira(username=username, token=token)

    data = {
        "jql": f"key in ({hut})"
    }

    payload = json.dumps(data)

    url = request.json.get("url_jira") + "/rest/api/2/search"

    r = jira._session.post(url, data=payload)

    response = r.json()
    issues = response.get("issues")

    if issues:
        return jsonify({f"La HUT {hut} existe."})
    else:
        return jsonify({f"La HUT {hut} no existe."})

if __name__ == '__main__':
    app.run(debug=True)