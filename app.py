from flask import Flask, jsonify, render_template, request, redirect
import random
import json
import os

app = Flask(__name__)

# JSON file path
QUOTES_FILE = "quotes.json"

# Load quotes from JSON file
def load_quotes():
    if os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Save quotes to JSON file
def save_quotes(quotes):
    with open(QUOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(quotes, f, indent=2, ensure_ascii=False)

# Load initial quotes
quotes = load_quotes()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quote", methods=["GET", "POST"])
def quote():
    if request.method == "POST":
        new_quote = {
            "quote": request.form["quote"],
            "character": request.form["character"],
            "anime": request.form["anime"]
        }

        quotes = load_quotes()  # always load latest
        quotes.append(new_quote)
        save_quotes(quotes)
        return redirect("/")

    quotes = load_quotes()  # always load latest
    if not quotes:
        return jsonify({"quote": "No quotes available", "character": "", "anime": ""})
    return jsonify(random.choice(quotes))


if __name__ == "__main__":
    app.run(debug=True)
