import requests
import os
from dotenv import load_dotenv

load_dotenv()

org_token = os.getenv("GITHUB_ORG_TOKEN")
org_name = "Yash-AI-Technologies"

headers = {
    'Authorization': f'token {org_token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Test organization access
url = f"https://api.github.com/orgs/{org_name}/repos"
response = requests.get(url, headers=headers)

print(f"Organization access status: {response.status_code}")
if response.status_code == 200:
    repos = response.json()
    print(f"✅ Can access {len(repos)} repositories")
    for repo in repos[:3]:  # Show first 3
        print(f"  - {repo['name']}")
else:
    print(f"❌ Cannot access organization: {response.text}")

# Test specific repo access
test_repo = "your-test-repo-name"  # Replace with actual repo name
url = f"https://api.github.com/repos/{org_name}/{test_repo}"
response = requests.get(url, headers=headers)
print(f"\nTest repo access status: {response.status_code}")
if response.status_code != 200:
    print(f"❌ Cannot access {test_repo}: {response.text}")