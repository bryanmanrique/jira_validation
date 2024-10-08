from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import os
import json
from spark_jira_tools import Jira

app = Flask(__name__)
CORS(app)  # Permitir solicitudes CORS

@app.route('/run_check_hut', methods=['POST'])
def run_check_hut():
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
        return Response(f"La HUT {hut} existe.", mimetype='text/plain')
    else:
        return Response(f"La HUT {hut} no existe.", mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)