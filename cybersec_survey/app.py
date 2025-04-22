from db import init_db, get_session
from db.models import NewsItem, ClassificationResult
from flask import Flask, render_template, request, jsonify, redirect, session, url_for, Response
import os
import yaml
from sqlalchemy.sql import func

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")

init_db()


@app.route("/api/news_items")
def get_news_items():
    db = get_session()

    if "news_item_ids" not in session:
        items = db.query(NewsItem).order_by(func.random()).limit(10).all()
        session["news_item_ids"] = [item.id for item in items]
        session["current_index"] = 0
    else:
        items = db.query(NewsItem).filter(NewsItem.id.in_(session["news_item_ids"])).all()

    db.close()
    return jsonify({"news_items": [{"id": i.id, "content": i.content} for i in items], "index": session.get("current_index", 0)})


@app.route("/api/label", methods=["POST"])
def save_label():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.json
    username = session["username"]
    news_item_id = data["id"]
    label = data["label"]

    db = get_session()
    result = ClassificationResult(username=username, news_item_id=news_item_id, cybersecurity=label)
    db.add(result)
    db.commit()
    db.close()

    session["current_index"] = session.get("current_index", 0) + 1

    return jsonify({"status": "ok"})


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            session["username"] = username
            return redirect(url_for("classify"))
        else:
            return render_template("login.html", error="Please enter a name.")

    if "username" in session:
        return redirect(url_for("classify"))

    return render_template("login.html")


@app.route("/classify")
def classify():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", username=session["username"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/export", methods=["GET", "POST"])
def export():
    if request.method == "POST":
        password = request.form.get("password")
        if password != "dimmuborg1r":
            return render_template("export.html", error="Wrong password")

        session["is_admin"] = True
        return redirect(url_for("admin_dashboard"))
    return render_template("export.html")


@app.route("/export/dashboard")
def admin_dashboard():
    if not session.get("is_admin"):
        return redirect(url_for("export"))

    db = get_session()

    from db.models import NewsItem, ClassificationResult

    all_news_items = db.query(NewsItem).all()
    export_data = []

    for news_item in all_news_items:
        classifications = db.query(ClassificationResult).filter_by(news_item_id=news_item.id).all()
        result = {
            "content": news_item.content.encode("unicode_escape").decode("utf-8"),
            "language": news_item.language,
            "classifications": [{"user": c.username, "cybersecurity": c.cybersecurity} for c in classifications],
        }
        export_data.append(result)

    db.close()

    yaml_data = yaml.dump(export_data, sort_keys=False, allow_unicode=True, default_style="")

    return Response(yaml_data, mimetype="text/yaml", headers={"Content-Disposition": "attachment;filename=classified_news_items.yaml"})


if __name__ == "__main__":
    app.run(debug=True, port=5004)
