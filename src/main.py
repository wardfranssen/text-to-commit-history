import json
from git import Repo
from git import Actor
import requests
import subprocess
import os

static_folder = "..\\static"

with open(f"{static_folder}\\letters.json", "r") as file:
    letters_json = json.loads(file.read())


def text_to_blocks(text: str):
    print(letters_json["letters"]["A"])
    for letter in text.upper():
        print()


def make_commit(repo_dir):
    with open(f"{static_folder}\\commit_message.txt") as file:
        commit_message = file.read()

    repo = Repo(repo_dir)
    repo.index.add(f"C:\\Users\\wardf\\PycharmProjects\\gitCommitHistory\\static\\commit.txt")
    repo.index.commit(commit_message, author=Actor("Python", ""))
    # repo.index.


def get_header(owner: str, repo_name: str, branch_name: str):
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/git/ref/heads/{branch_name}")

    print(response.json())

    url = response.json()["object"]["url"]
    response = requests.get(url)

    commit_sha = response.json()["sha"]
    tree_sha = response.json()["tree"]["sha"]
    tree_url = response.json()["tree"]["url"]

    print(commit_sha, tree_sha, tree_url)

    payload = {
        "content": "SGVsbG8sIFdvcmxkIQ==",
        "encoding": "base64"
    }

    response = requests.post(f"https://api.github.com/repos/{owner}/{repo_name}/git/blobs", data=payload)
    print(response.json())


# username = input("Github username: ")
# repo_name = input("Repo name: ")
# branch_name = input("Branch name: ")
# get_header(username, repo_name, branch_name)




def git_commit_push(repo_path, message, branch="main"):
    # Check if the repository path exists
    if not os.path.isdir(repo_path):
        print(f"Error: The specified repository path '{repo_path}' does not exist.")
        return

    # Change to the specified repository directory
    os.chdir(repo_path)

    try:
        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)

        # Commit changes with the provided message
        subprocess.run(["git", "commit", "-m", message, "--allow-empty"], check=True)

        # Push the changes to the specified branch on the remote repository
        subprocess.run(["git", "push", "origin", branch], check=True)

        print("Changes committed and pushed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


# Usage example
repo_path = input("Enter the path to your repository: ")
commit_message = input("Enter your commit message: ")
git_commit_push(repo_path, commit_message)


# make_commit("C:\\Users\\wardf\\PycharmProjects\\gitCommitHistory")
