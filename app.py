from wikipedia_search import search_wikipedia
import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/github")
def github_form():
    return render_template('github_form.html')


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
        return render_template(
            "index.html",
            error="No Wikipedia page found for this prompt. Please try again."
        )


@app.route("/github/submit", methods=["POST"])
def lookup():
    username = request.form.get('username')
    response = requests.get(f"https://api.github.com/users/{username}/repos")

    if response.status_code == 200:
        repos = response.json()
        repo_data = []

        for repo in repos:
            commits_response = requests.get(
                repo["commits_url"].replace('{/sha}', '')
            )

            latest_commit = None
            if commits_response.status_code == 200:
                commits = commits_response.json()
                if commits:
                    latest_commit = commits[0]

            latest_commit_info = {
                "hash": latest_commit["sha"] if latest_commit else "No commits found",
                "author": latest_commit["commit"]["author"]["name"] if latest_commit else "N/A",
                "date": latest_commit["commit"]["author"]["date"] if latest_commit else "N/A",
                "message": latest_commit["commit"]["message"] if latest_commit else "N/A",
            }

            repo_data.append({
                "name": repo["name"],
                "last_updated": repo["updated_at"],
                "latest_commit": latest_commit_info,
                "url": repo["html_url"],
                "clone_url": repo["clone_url"],
                "ssh_url": repo["ssh_url"]
            })

        return render_template("github_results.html", username=username, repo_data=repo_data)
    else:
        return render_template("github_form.html", error=f"User {username} not found.")


def process_query(query):
    if query == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    elif query == "What is your name?":
        return "Mac"
    elif query.startswith("Which of the following numbers is the largest"):
        return str(sorted(list(map(int, query[-11:-1].split(","))))[-1])
    elif "plus" in query:
        return str(int(query.split()[2]) + int(query.split()[4].rstrip('?')))
    elif "minus" in query:
        return str(int(query.split()[2]) - int(query.split()[4].rstrip('?')))
    elif "multiplied" in query:
        return str(int(query.split()[2]) * int(query.split()[-1].rstrip("?")))
    elif "prime" in query:
        output = ""
        list_of_numbers_with_commas = query.split()[-5:]
        for number in list_of_numbers_with_commas:
            number = int(number.rstrip(",?"))
            if is_prime(number):
                output += str(number) + ", "
        return output.rstrip(", ")
    elif "both a square and a cube" in query:
        list_of_numbers_with_commas = query.split()[-7:]
        for num in list_of_numbers_with_commas:
            num = int(num.rstrip(',?'))
            if is_square_and_cube(num):
                return str(num)
    else:
        return "Unknown"


def is_square_and_cube(num):
    root_square = int(num**0.5)
    root_cube = int(num**(1/3))
    return root_square**2 == num and root_cube**3 == num


def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

