import sys
import requests

API_URL = "https://api.github.com/repos/entity12208/GeoLoader/releases"

def get_release_notes(tag):
    response = requests.get(API_URL)
    releases = response.json()
    for release in releases:
        if release['tag_name'] == tag:
            return release['body']
    return "No release notes found."

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_release_notes.py <tag>")
        sys.exit(1)
    
    tag = sys.argv[1]
    notes = get_release_notes(tag)
    print(notes)
