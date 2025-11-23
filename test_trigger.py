import requests
import os
from dotenv import load_dotenv

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")
github_username = os.getenv("GITHUB_USERNAME")
repo_name = os.getenv("GITHUB_REPO_NAME")

url = f"https://api.github.com/repos/{github_username}/{repo_name}/dispatches"
headers = {
    'Authorization': f'token {github_token}',
    'Accept': 'application/vnd.github.v3+json'
}

payload = {
    "event_type": "test-trigger"
}

response = requests.post(url, headers=headers, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 204:
    print("✅ Test workflow triggered successfully!")
else:
    print("❌ Failed to trigger workflow")