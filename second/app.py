from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

app = Flask(__name__)

client = MongoClient(MONGO_URI)
db = client["testdb"]
collection = db["users"]
todo_collection = db["todos"]


@app.route("/", methods=["GET", "POST"])
def form():
    error = None
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            collection.insert_one({"name": name, "email": email})
            return redirect(url_for("success"))
        except Exception as e:
            error = str(e)
    return render_template("form.html", error=error)

@app.route("/success")
def success():
    return render_template("success.html")
@app.route("/api")
def api():
    with open("second/api_data.json") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/todo")
def todo():
    return render_template("todo.html")

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    todo_collection.insert_one({
        "itemName": item_name,
        "itemDescription": item_description
    })

    return "To-Do Item Saved Successfully"


if __name__ == "__main__":
    app.run(debug=True)
