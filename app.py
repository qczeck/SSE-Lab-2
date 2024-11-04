from flask import Flask, render_template, request
from wikipedia_search import search_wikipedia


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
        return render_template("index.html", error="No Wikipedia page found"
                               "for this prompt. Please try again.")

@app.route("/github/submit", methods = ["POST"])
def lookup():
    username = request.form.get('username')
    response = request.get(f" https://api.github.com/users/ss5921/repos")


    # Check if the response is successful
    if response.status_code == 200:
        repos = response.json()  # GitHub API returns a list of 'repository' entities
        for repo in repos:
            print(repo["full_name"])  # Corrected to use straight quotes
        return "Repositories fetched successfully. Check console for output."
    else:
        return f"User {username} not found", 404


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
