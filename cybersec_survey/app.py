from cybersec_survey.db import init_db, get_session
from cybersec_survey.db.models import NewsItem, ClassificationResult
from flask import Flask, render_template, request, jsonify, redirect, session, url_for, Response
import os
import json
from sqlalchemy.sql import func
from cybersec_survey.config import Config

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")

init_db()


@app.route("/api/news_items")
def get_news_items():
    db = get_session()
    if "news_item_ids" not in session:
        # Subquery: count how many times each news_item_id appears in classifications
        classification_counts = (
            db.query(ClassificationResult.news_item_id, func.count(ClassificationResult.id).label("class_count"))
            .group_by(ClassificationResult.news_item_id)
            .subquery()
        )

        # Left join with NewsItem and order by classification count (nulls = 0)
        items = (
            db.query(NewsItem)
            .outerjoin(classification_counts, NewsItem.id == classification_counts.c.news_item_id)
            .order_by(classification_counts.c.class_count.asc().nullsfirst(), func.random())
            .limit(Config.NEWS_ITEMS_PER_SESSION)
            .all()
        )

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
    if not data:
        return jsonify({"status": "error"})
    username = session.get("username", "")
    news_item_id = data.get("id", "")
    label = data.get("label", "")
    comment = data.get("comment", "")

    db = get_session()
    result = ClassificationResult(username=username, news_item_id=news_item_id, cybersecurity=label, comment=comment)
    db.add(result)
    db.commit()
    db.close()

    return jsonify({"status": "ok"})


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            session["username"] = username
            return redirect(url_for("welcome"))
        else:
            return render_template("login.html", error="Please enter a name.")

    if "username" in session:
        return redirect(url_for("classify"))
    return render_template(
        "login.html",
        num_news_items=Config.NEWS_ITEMS_PER_SESSION,
        time_limit_min=Config.NEWS_ITEMS_PER_SESSION // 2,
        time_limit_max=Config.NEWS_ITEMS_PER_SESSION,
    )


@app.route("/classify")
def classify():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("classify.html", username=session["username"])


@app.route("/welcome")
def welcome():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("welcome.html", username=session["username"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/export", methods=["GET"])
def export():
    return render_template("export.html")


@app.route("/export-users", methods=["POST"])
def export_users():
    password = request.form.get("password")
    if password != Config.ADMIN_PW:
        return render_template("export.html", error="Wrong password")

    db = get_session()

    from cybersec_survey.db.models import ClassificationResult

    all_rows = db.query(ClassificationResult).all()
    user_id_dict = {}
    for row in all_rows:
        row_data = {"id": row.news_item_id, "cybersecurity": row.cybersecurity, "comment": row.comment}
        if row.username in user_id_dict:
            user_id_dict[row.username].append(row_data)
        else:
            user_id_dict[row.username] = [row_data]
    db.close()

    json_data = json.dumps(user_id_dict, ensure_ascii=False, indent=2)

    return Response(json_data, mimetype="application/json", headers={"Content-Disposition": "attachment;filename=users.json"})


@app.route("/export-all", methods=["POST"])
def export_all():
    password = request.form.get("password")
    if password != Config.ADMIN_PW:
        return render_template("export.html", error="Wrong password")

    db = get_session()

    from cybersec_survey.db.models import NewsItem, ClassificationResult

    all_news_items = db.query(NewsItem).all()
    export_data = []

    for news_item in all_news_items:
        classifications = db.query(ClassificationResult).filter_by(news_item_id=news_item.id).all()
        result = {
            "content": news_item.content.encode("unicode_escape").decode("utf-8"),
            "language": news_item.language,
            "classifications": [{"user": c.username, "cybersecurity": c.cybersecurity} for c in classifications],
            "comments": [{"user": c.username, "comment": c.comment} for c in classifications],
        }
        export_data.append(result)

    db.close()

    json_data = json.dumps(export_data, ensure_ascii=False, indent=2)

    return Response(json_data, mimetype="application/json", headers={"Content-Disposition": "attachment;filename=data.json"})
