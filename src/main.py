from datetime import datetime
import json
import os
import subprocess

static_folder = "..\\static"

with open(f"{static_folder}\\characters.json", "r") as file:
    chars_json = json.loads(file.read())

days_of_the_week = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]


def char_to_dates(letter: str, year: int) -> list:
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
        # Commit changes
        subprocess.run(commit_command, check=True)

        # Push the changes to the specified branch on the remote repository
        subprocess.run(["git", "push", "origin", branch], check=True)

        print("Changes committed and pushed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print("It is possible that there is no repo at given dir.")
        exit(0)


if __name__ == "__main__":
    repo_dir = input("Directory of repo: ")
    commit_message = input("Commit message: ")

    text = input("Text: ")
    text_size = input("What size should the text be (big/small): ")

    if text_size != "big" and text_size != "small":
        print("Please enter either big or small.")
        exit(0)
    year = int(input("What year should your commits be in: "))

    # Get week day of first day of given year and turn it into index
    first_day_of_year = days_of_the_week.index(datetime(year, 1, 1).strftime("%A"))

    dates = []
    # Might have to change this to 7/8 IDK why though
    day = 7
    icon_name = ""

    n = len(text)

    for i in range(n):
        if i >= len(text):
            break

        # +14 is 3 weeks because it will also add 1 week after each text[i] (the text[i] before the space)
        if text[i] == " ":
            day += 14
            continue
        elif text[i] == "`":
            icon_name = ""

            for char in text:
                if "`" in icon_name and char == "`":
                    icon_name += char
                    break

                if char == "`" or icon_name:
                    icon_name += char

            dates.append(char_to_dates(chars_json["icons"][icon_name], year))

            # Need to replace it with another char (can't be `) cause otherwise it will skip a letter
            text = text.replace(icon_name, "_")

        elif text[i] in chars_json["punctuation"].keys():
            dates.append(char_to_dates(chars_json["punctuation"][text[i]], year))
        elif text[i].isnumeric():
            dates.append(char_to_dates(chars_json["numbers"][text[i]], year))
        else:
            dates.append(char_to_dates(chars_json["letters"][text_size][text[i].upper()], year))

        # Add some space between each character
        day += 7

    for row in dates:
        for date in row:
            git_commit_push(repo_dir, commit_message, date=date)
