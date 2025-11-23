import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")
github_username = os.getenv("GITHUB_USERNAME")
repo_name = os.getenv("GITHUB_REPO_NAME")

# Test with simple payload
url = f"https://api.github.com/repos/{github_username}/{repo_name}/dispatches"
headers = {
    'Authorization': f'token {github_token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Test with real repository from organization
payload = {
    "event_type": "build-matrix",
    "client_payload": {
        "repos_json": [
            {
                "repo_name": "yash-ai-interviewer-frontend",
                "version": "1.0",
                "has_release": False,
                "branch": "dev"
            }
        ],
        "max_parallel": 5
    }
}

print("Sending payload:")
print(json.dumps(payload, indent=2))

response = requests.post(url, headers=headers, json=payload)
print(f"\nStatus: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 204:
    print("✅ Build matrix workflow triggered!")
    print("Check: https://github.com/yash-viral/pipeline-test/actions")
else:
    print("❌ Failed to trigger workflow")