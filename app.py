from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
history = {}  # in-memory user download history


# ===== WEB PAGE =====
@app.route("/web")
def web():
    return render_template("index.html")


# ===== DOWNLOAD API =====
@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    user = str(data.get("user"))
    if not url or not user:
        return jsonify({"error": "Missing URL or user"}), 400

    video_url = None

    # --- TikTok ---
    if "tiktok.com" in url:
        try:
            res = requests.get(f"https://tikwm.com/api/?url={url}", timeout=20).json()
            video_url = res.get("data", {}).get("play")
        except:
            pass

    # --- Instagram ---
    if "instagram.com" in url:
        try:
            # Simple API fallback (replace with real API if needed)
            res = requests.get("https://igram.world/api/convert", params={"url": url}, timeout=20).json()
            video_url = res.get("url")
        except:
            pass

    if not video_url:
        return jsonify({"error": "Failed to get video"}), 400

    # Save history
    history.setdefault(user, []).append(video_url)
    return jsonify({"video": video_url})


# ===== HISTORY API =====
@app.route("/history/<uid>")
def get_history(uid):
    return jsonify(history.get(uid, []))


# ===== RUN FLASK =====
if __name__ == "__main__":
    # For development only
    app.run(host="0.0.0.0", port=5000, debug=True)
