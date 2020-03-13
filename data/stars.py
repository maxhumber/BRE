import json
import os
import time
from dotenv import load_dotenv
from tqdm import tqdm
import requests

load_dotenv(dotenv_path='data/.env')

# https://github.com/user/settings/tokens

token = os.getenv("GITHUB_ACCESS_TOKEN")
username = os.getenv("GITHUB_USERNAME")

session = requests.Session()
session.auth = (username, token)

# STARGAZERS - GET /repos/:owner/:repo/stargazers

def get_repo_stargazers(owner, repo):
    page = 1
    url = f"http://api.github.com/repos/{owner}/{repo}/stargazers?page={page}"
    response = session.get(url)
    pages = int(response.links["last"]["url"].split("=")[-1])
    stargazers = []
    for page in range(1, pages + 1):
        url = f"http://api.github.com/repos/{owner}/{repo}/stargazers?page={page}"
        response = session.get(url)
        data = response.json()
        sg = [s["login"] for s in data]
        stargazers.extend(sg)
        time.sleep(0.1)
    return stargazers


# STARRED REPOS

def parse_repo(repo, user):
    return {
        "user": user,
        "repo": repo["full_name"],
        "description": repo["description"],
        "language": repo["language"],
        "stargazers": repo["stargazers_count"],
    }


def get_user_stars(user):
    page = 1
    url = f"https://api.github.com/users/{user}/starred?page={page}"
    response = session.get(url)
    try:
        pages = int(response.links["last"]["url"].split("=")[-1])
        pages = min(pages, 10)
    except KeyError:
        pages = 1
    stars = []
    for page in range(1, pages + 1):
        url = f"https://api.github.com/users/{user}/starred?page={page}"
        response = session.get(url)
        data = response.json()
        s = [parse_repo(r, user) for r in data]
        stars.extend(s)
        time.sleep(0.1)
    return stars


if __name__ == "__main__":

    gazpacho_stargazers = get_repo_stargazers("maxhumber", "gazpacho")
    gif_stargazers = get_repo_stargazers("maxhumber", "gif")
    stargazers = list(set(gazpacho_stargazers).union(gif_stargazers))

    all_stars = []
    for user in tqdm(stargazers):
        all_stars.extend(get_user_stars(user))

    import pandas as pd
    df = pd.DataFrame(all_stars)
    df.to_csv("data/stars.csv", encoding="utf-8", index=False)
