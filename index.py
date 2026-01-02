from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# List of backup engines
ENGINES = [
    "https://terabox-dl.qtcloud.workers.dev/api/get-info?url={}",
    "https://api.vkrdown.com/server/?vkr={}",
    "https://terabox.recloud.workers.dev/api/get-info?url={}"
]

@app.route("/")
def home():
    return jsonify({"status": 1, "msg": "Zion Multi-Engine API is Live!"})

@app.route("/api/terabox")
def terabox():
    link = request.args.get("link")
    if not link:
        return jsonify({"status": 0, "error": "Bhai link toh dalo!"})

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    # Baari-baari saare engines try karo
    for engine_url in ENGINES:
        try:
            target = engine_url.format(link)
            print(f"📡 Trying: {target}")
            res = requests.get(target, headers=headers, timeout=10)
            
            # Check if response is actually JSON
            if res.status_code == 200:
                data = res.json()
                # Agar data mein download links hain, toh return kar do
                return jsonify({
                    "status": 1,
                    "engine": "Zion-Auto-Fallback",
                    "data": data
                })
        except Exception as e:
            print(f"❌ Engine Failed: {str(e)}")
            continue

    return jsonify({
        "status": 0,
        "error": "ALL_ENGINES_DOWN",
        "msg": "Bhai, saare providers abhi busy hain. 5 min baad try karo."
    })

def handler(event, context):
    return app(event, context)
