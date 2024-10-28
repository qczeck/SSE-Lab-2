from flask import Flask, render_template, request
from wikipedia_search import search_wikipedia


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/query")
def process_response():
    q = request.args.get('q')
    return process_query(q)


@app.route("/submit", methods=["POST"])
def submit():
    prompt = request.form.get("prompt")
    url = search_wikipedia(prompt)

    if url:
        return render_template("hello.html", url=url, prompt=prompt)
    else:
        return render_template("index.html", error="No Wikipedia page found"
                               "for this prompt. Please try again.")


def process_query(query):
    if query == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    elif query == "What is your name?":
        return "Mac"
    elif query.startswith("Which of the following numbers is the largest"):
        return = str(sorted(list(map(int, test[-11:-1].split(","))))[-1])

    else:
        return "Unknown"
