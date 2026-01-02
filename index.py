from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Zion API is Running!"

@app.route("/api/terabox")
def terabox():
    link = request.args.get("link")
    if not link:
        return jsonify({"status": 0, "error": "Link missing"})
    
    api_url = f"https://terabox-dl.qtcloud.workers.dev/api/get-info?url={link}"
    
    try:
        # User-Agent add kiya taaki target server block na kare
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(api_url, headers=headers, timeout=15)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"status": 0, "error": str(e)})

# Ye niche wali line hata dena (Vercel automatically handle karega)
# if __name__ == "__main__":
#     app.run()
