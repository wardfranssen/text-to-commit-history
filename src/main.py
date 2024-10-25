from datetime import datetime
import json
import os
import subprocess
import time

static_folder = "..\\static"

with open(f"{static_folder}\\letters.json", "r") as file:
    letters_json = json.loads(file.read())

days_of_the_week = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]


def letter_to_dates(letter: str, year: int) -> list:
    global day

    dates = []
    for column in zip(*letter):
        for box in column:
            if box == "X":
                if day-first_day_of_year >= 0:
                    try:
                        # Turn day number into date of given year
                        dates.append(datetime.strptime(f"{year}-{day-first_day_of_year+1}", "%Y-%j").strftime("%Y-%m-%d"))
                    except ValueError:
                        print("Text is too long, it does not fit in 1 year")
                        raise exit(0)
            day += 1

    return dates


def git_commit_push(repo_path: str, message: str, date="", branch="main") -> None:
    if not os.path.isdir(repo_path):
        print(f"Error: The specified repository path '{repo_path}' does not exist.")
        return

    # Change to the specified repository directory
    os.chdir(repo_path)

    try:
        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)

        commit_command = ["git", "commit", "-m", message, "--allow-empty"]

        if date:
            commit_command.append(f"--date={date}")
        # Commit changes with the provided message
        subprocess.run(commit_command, check=True)

        # Push the changes to the specified branch on the remote repository
        subprocess.run(["git", "push", "origin", branch], check=True)

        print("Changes committed and pushed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    repo_dir = input("Directory of repo: ")
    commit_message = input("Commit message: ")

    text = input("Text: ")
    text_size = input("What size should the text be (big/small): ")
    year = int(input("What year should your commits be in: "))

    # Get week day of first day of given year and turn it into index
    first_day_of_year = days_of_the_week.index(datetime(year, 1, 1).strftime("%A"))

    dates = []
    day = 0

    for letter in text.strip().upper():
        # +14 is 3 weeks because it will also add 1 week after each letter (the letter before the space)
        if letter == " ":
            day += 14
            continue
        else:
            dates.append(letter_to_dates(letters_json["letters"][text_size][letter], year))

        # Add some space between each letter
        day += 7

    for row in dates:
        for date in row:
            git_commit_push(repo_dir, commit_message, date=date)
            time.sleep(1)
