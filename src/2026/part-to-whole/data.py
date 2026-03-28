import requests
import csv
import time
from collections import defaultdict


session = requests.Session()
session.headers.update({"Accept": "application/vnd.github+json"})


def get_repos(username):
    repos = []
    page = 1

    while True:
        url = f"https://api.github.com/users/{username}/repos"
        params = {"per_page": 100, "page": page}
        res = session.get(url, params=params)
        res.raise_for_status()

        data = res.json()
        if not data:
            break

        repos.extend(data)
        page += 1

    return repos


def get_languages(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    res = session.get(url)
    res.raise_for_status()
    return res.json()


def build_dataset(username):
    repos = get_repos(username)

    total_languages = defaultdict(int)
    repo_languages = {}

    for repo in repos:
        if repo["fork"]:
            continue

        name = repo["name"]
        langs = get_languages(username, name)

        repo_languages[name] = langs

        for lang, bytes_count in langs.items():
            total_languages[lang] += bytes_count

        time.sleep(0.2)

    return total_languages, repo_languages


def to_percentages(lang_dict):
    total = sum(lang_dict.values())
    return {lang: (value / total) * 100 for lang, value in lang_dict.items()}


def save_total_csv(total_langs, percent_langs):
    with open("src/2026/part-to-whole/languages_total.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["language", "bytes", "percentage"])

        for lang in total_langs:
            writer.writerow([lang, total_langs[lang], percent_langs[lang]])


if __name__ == "__main__":
    total_langs, repo_langs = build_dataset("y-sunflower")
    percent_langs = to_percentages(total_langs)
    save_total_csv(total_langs, percent_langs)
