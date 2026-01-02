from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Zion Ultimate Engine is Online!"

@app.route("/api/terabox")
def terabox():
    link = request.args.get("link")
    if not link:
        return jsonify({"status": 0, "error": "Link missing!"})

    # Publer Engine - Ye Cloudflare ko bypass karne mein king hai
    api_url = "https://publer.io/api/v1/tools/media-download"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://publer.io",
        "Referer": "https://publer.io/terabox-video-downloader"
    }

    try:
        # Step 1: Request metadata from Publer
        payload = {"url": link}
        res = requests.post(api_url, json=payload, headers=headers, timeout=15)
        
        if res.status_code == 200:
            data = res.json()
            return jsonify({
                "status": 1,
                "engine": "Publer-Bypass",
                "title": data.get("title"),
                "thumbnail": data.get("thumbnail"),
                "links": data.get("payload", []) # Publer 'payload' mein links deta hai
            })
        else:
            # Fallback to the simplest worker if Publer fails
            fallback_res = requests.get(f"https://terabox-dl.qtcloud.workers.dev/api/get-info?url={link}", timeout=10)
            return jsonify(fallback_res.json())

    except Exception as e:
        return jsonify({"status": 0, "error": "All bypasses failed", "msg": str(e)})

def handler(event, context):
    return app(event, context)
