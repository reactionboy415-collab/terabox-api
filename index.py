from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/api/terabox")
def terabox():
    link = request.args.get("link")
    if not link:
        return jsonify({"status": 0, "error": "Link missing"})
    
    # Ye tunnel bypass API hai jo Vercel par makkhan chalti hai
    api_url = f"https://terabox-dl.qtcloud.workers.dev/api/get-info?url={link}"
    
    try:
        res = requests.get(api_url, timeout=15)
        return jsonify(res.json())
    except:
        return jsonify({"status": 0, "error": "Service Down"})

# Vercel ke liye zaruri hai
def handler(event, context):
    return app(event, context)
