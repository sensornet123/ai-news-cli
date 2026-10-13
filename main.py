import requests
import json

def fetch_hot_repos():
    url = "https://api.github.com/search/repositories"
    params = {"q": "topic:ai", "sort": "stars", "order": "desc", "per_page": 5}
    headers = {"Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, params=params, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json().get("items", [])

def generate_digest(repos):
    lines = []
    for repo in repos:
        name = repo["name"]
        desc = (repo.get("description") or "").strip() or "No description"
        line = f"- {name}: {desc}"
        lines.append(line)
    return "\n".join(lines)

def main():
    try:
        repos = fetch_hot_repos()
        if not repos:
            print("No repos found.")
            return
        digest = f"Today's Hot AI Repos (by stars):\n\n{generate_digest(repos)}"
        print(digest)
        with open("daily_digest.txt", "w", encoding="utf-8") as f:
            f.write(digest)
        print("\nDigest saved to daily_digest.txt")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
