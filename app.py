from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

history = {}

@app.route("/web")
def web():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():

    data = request.json
    url = data["url"]
    user = str(data["user"])

    video = None

    if "tiktok" in url:
        res = requests.get(f"https://tikwm.com/api/?url={url}").json()
        video = res["data"]["play"]

    if "instagram" in url:
        res = requests.get("https://igram.world/api/convert", params={"url": url}).json()
        video = res["url"]

    if video:
        history.setdefault(user, []).append(video)
        return jsonify({"video": video})

    return jsonify({"error": "failed"})


@app.route("/history/<uid>")
def get_history(uid):
    return jsonify(history.get(uid, []))


app.run(host="0.0.0.0", port=5000)
