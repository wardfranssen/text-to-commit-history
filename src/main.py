import json
from git import Repo
from git import Actor

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


dir = input("Dir of repo: ")
make_commit(dir)
