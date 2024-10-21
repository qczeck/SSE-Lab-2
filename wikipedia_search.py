import requests


def search_wikipedia(prompt):
    # Format the prompt for the Wikipedia search URL
    search_url = f"https://en.wikipedia.org/wiki/{prompt.replace(' ', '_')}"

    # Make a request to the Wikipedia page
    response = requests.get(search_url)

    # Check if the page exists by inspecting the response
    if response.status_code == 200:
        return search_url
    else:
        return None
