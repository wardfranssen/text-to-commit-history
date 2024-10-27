![Example image](https://github.com/wardfranssen/gitCommitHistory/blob/main/static/images/Example.png?raw=true)

# text-to-commit-history


This project allows you to create a series of git commits that form a specified text pattern over a year. The text pattern is defined using a JSON file that maps letters, numbers, punctuatiion and icons to a grid of dates. This JSON file can easily be edited to costumize everything.

## Prerequisites

- Python 3.x
- Git
- GitHub CLI ([Setup Instructions](https://docs.github.com/en/get-started/getting-started-with-git/set-up-git#setting-up-git))

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/wardfranssen/text-to-commit-history.git
    cd text-to-commit-history
    ```

## Usage

1. Make your own public repo and publish it to github. This repo will be used to make the commits to, if you delete this repo all the commits will also be gone.

1. Run the script:
    ```sh
    python src/main.py
    ```

2. Follow the prompts to input:
    - Directory of the repository you just made
    - Commit message
    - Text to be displayed
    - Text size (big/small)
    - Year for the commits

## Example

```sh
Directory of repo: C:\Users\user\Test
Commit message: Test
Text: Hello, World
What size should the text be (big/small): small
What year should your commits be in: 2000
```

## Files

- `src/main.py`: Main script to run the project.
- `static/characters.json`: JSON file containing the characters mappings, you can fully customize the characters in this file, but make sure that each letter has 7 columns.
- `static/...vincent-van-git.config.json`: These can be imported to https://vincent-van-git.netlify.app/ to visualize the letters in a commit history.
