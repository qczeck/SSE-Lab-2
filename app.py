from flask import Flask, render_template, request
from wikipedia_search import search_wikipedia

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    prompt = request.form.get("prompt")
    url = search_wikipedia(prompt)
    
    if url:
        return render_template("hello.html", url=url, prompt=prompt)
    else:
        return render_template("index.html", error="No Wikipedia page found for this prompt. Please try again.")