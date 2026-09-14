import json
import os
import subprocess
import sys
from datetime import date
from enum import Enum


class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    
class Action(Enum):
    SOLVE = "solve"
    REVIEW = "review"
    SKIP = "skip"
class Confirmation(Enum):
    YES = "yes"
    NO = "no"

# =========================================================
# Configuration
# =========================================================

CONFIG_FILE = "git_config.json"
PROGRESS_FILE = "progress.json"
README_FILE = "README.md"

PROGRESS_START = "<!-- PROGRESS_START -->"
PROGRESS_END = "<!-- PROGRESS_END -->"


# =========================================================
# General command helper
# =========================================================

def run(command, capture=False):
    """
    Run a shell command.

    If capture=True, return stdout as a string.
    Stop the program if the command fails.
    """

    result = subprocess.run(
        command,
        capture_output=capture,
        text=True
    )

    if result.returncode != 0:
        if capture and result.stderr:
            print(result.stderr.strip())

        sys.exit(result.returncode)

    if capture:
        return result.stdout.strip()

    return result


# =========================================================
# Git initialization
# =========================================================

def is_git_repo():
    """
    Check whether the current directory
    is already inside a Git repository.
    """

    result = subprocess.run(
        [
            "git",
            "rev-parse",
            "--is-inside-work-tree"
        ],
        capture_output=True,
        text=True
    )

    return result.returncode == 0


def initialize_git():
    """
    Initialize Git if the current directory
    is not already a Git repository.
    """

    if is_git_repo():
        print("Git repository detected.")
        return

    print("Git repository not found.")
    print("Initializing Git...")

    run([
        "git",
        "init"
    ])

    run([
        "git",
        "branch",
        "-M",
        "main"
    ])

    print("Git repository initialized.")


# =========================================================
# JSON helpers
# =========================================================

def load_json(filename):
    """
    Load JSON data.

    If the file does not exist,
    create it with an empty dictionary.

    If the JSON is invalid,
    return an empty dictionary.
    """

    if not os.path.exists(filename):
        save_json(filename, {})
        return {}

    try:
        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except json.JSONDecodeError:

        print(
            f"{filename} contains invalid JSON."
        )

        return {}


def save_json(filename, data):
    """
    Save dictionary data to a JSON file.
    """

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# =========================================================
# Git remote handling
# =========================================================

def get_actual_remote():
    """
    Ask Git for the current origin URL.

    Return None if origin does not exist.
    """

    result = subprocess.run(
        [
            "git",
            "remote",
            "get-url",
            "origin"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return None

    return result.stdout.strip()


def setup_remote(config):
    """
    Make sure a GitHub remote exists.

    Priority:

    1. Use actual Git origin
    2. Restore origin from JSON
    3. Ask user for GitHub URL
    """

    actual_remote = get_actual_remote()

    # -----------------------------------------------------
    # Case 1:
    # Git already has an origin
    # -----------------------------------------------------

    if actual_remote:

        print(" Git remote found:")
        print(f"   {actual_remote}")

        config["remote_url"] = actual_remote
        config["remote_connected"] = True

        save_json(
            CONFIG_FILE,
            config
        )

        return actual_remote

    # -----------------------------------------------------
    # Case 2:
    # Git has no origin,
    # but JSON remembers one
    # -----------------------------------------------------

    saved_remote = config.get(
        "remote_url"
    )

    if saved_remote:

        print(
            " Remote exists in JSON "
            "but not in Git."
        )

        print(
            "Restoring remote:"
        )

        print(
            f"   {saved_remote}"
        )

        run([
            "git",
            "remote",
            "add",
            "origin",
            saved_remote
        ])

        print(
            " Git remote restored."
        )

        return saved_remote

    # -----------------------------------------------------
    # Case 3:
    # No remote anywhere
    # -----------------------------------------------------

    print(
        "\n No GitHub remote detected."
    )

    repo_url = input(
        "Enter your GitHub repository URL: "
    ).strip()

    if not repo_url:

        print(
            " Repository URL cannot be empty."
        )

        sys.exit(1)

    run([
        "git",
        "remote",
        "add",
        "origin",
        repo_url
    ])

    config["remote_url"] = repo_url
    config["remote_connected"] = True

    save_json(
        CONFIG_FILE,
        config
    )

    print(
        " GitHub remote added and saved."
    )

    return repo_url


# =========================================================
# Git branch helpers
# =========================================================
def remote_branch_exists(branch):
    """
    Check whether the branch already exists
    on the remote repository.
    """

    result = subprocess.run(
        [
            "git",
            "ls-remote",
            "--heads",
            "origin",
            branch
        ],
        capture_output=True,
        text=True
    )

    return bool(result.stdout.strip())

def sync_with_remote():
    """
    Synchronize the local branch with GitHub
    before attempting to push.

    This is especially important when the
    GitHub repository already contains commits.
    """

    branch = get_current_branch()

    if not remote_branch_exists(branch):
        print(
            f" Remote branch origin/{branch} "
            "does not exist yet."
        )

        return

    print(
        f" Synchronizing with origin/{branch}..."
    )

    result = subprocess.run(
        [
            "git",
            "pull",
            "origin",
            branch,
            "--allow-unrelated-histories",
            "--no-edit"
        ]
    )

    if result.returncode != 0:

        print(
            "\n Git could not automatically "
            "synchronize the repositories."
        )

        print(
            "There may be a merge conflict "
            "that requires manual resolution."
        )

        sys.exit(result.returncode)

    print(
        " Repository synchronized."
    )
def get_current_branch():
    """
    Get the current Git branch.
    """

    branch = run(
        [
            "git",
            "branch",
            "--show-current"
        ],
        capture=True
    )

    if not branch:
        return "main"

    return branch


def has_upstream():
    """
    Check whether the current Git branch
    already tracks a remote branch.
    """

    result = subprocess.run(
        [
            "git",
            "rev-parse",
            "--abbrev-ref",
            "--symbolic-full-name",
            "@{u}"
        ],
        capture_output=True,
        text=True
    )

    return result.returncode == 0
#Confirmation code 
def get_confirmation(message):
        while True:
             user_input =  input(f"{message} (yes/no): ").strip().lower()
             try:
                 return Confirmation(user_input)
             except ValueError:
                 print("Please enter yes or no.")

# =========================================================
# DSA progress tracking
# =========================================================


def ask_problem_information():
    """
    Ask whether the user solved,
    reviewed, or wants to skip
    recording a DSA problem.
    """

    
    
    #Helper functions
    def get_action():
        while True:
            user_input = input(
                "Did you solve or review a problem? "
                "(solve/review/skip): "
            ).strip().lower()

            try:
                return Action(user_input)

            except ValueError:
                print(
                    "Please enter solve, review, or skip."
                )
    def get_problem_number():
        while True :
            try:
                 return int(input("Problem number: ").strip())
                
            except ValueError:
                print("Please enter a valid problem number. example 24")
    
    def get_problem_name():       
        while True:
            problem: str = input(
                "Problem name: "
            ).strip()

            if problem:
                return problem

            print(
                "Problem name cannot be empty."
            )


    def get_problem_difficulty():       
        while True:
            user_input = input("Difficulty (Easy/Medium/Hard): ").strip().title()
            try:
                return Difficulty(user_input)
                
            except ValueError:
                print(" Please enter Easy, Medium, or Hard.")
                
    def get_problem_pattern():  
        while True:
            pattern = input( "Pattern/Topic: ").strip().title()
            
            if pattern:
                    return pattern
            print(
                "Pattern cannot be empty."
            )            


    
    
    def show_summary(data, title="DSA PROBLEM SUMMARY"):
            print("\n" + "=" * 40)
            print(title)
            print("=" * 40)

            for index, (key, value) in enumerate(
                data.items(),
                start=1
            ):
                print(
                    f"{index}. {key.title()}: {value}"
                )

            print("=" * 40)
                 
                 
    print("\n DSA Progress")
    action = get_action()
    
    if action == Action.SKIP:
        return None
    #-------------------------------------
    # Review 
    #_____________________________________
    
    
    if action == Action.REVIEW:

        progress = load_json(PROGRESS_FILE)

        while True:
            number = get_problem_number()
            number_key = str(number)

            if number_key not in progress:
                print(
                    f"Problem #{number} was not found."
                )

                try_again = get_confirmation(
                    "Would you like to try another "
                    "problem number?"
                )

                if try_again == Confirmation.NO:
                    return None

                continue

            entry = progress[number_key]

            review_info = {
                "Number": number,
                "Problem": entry["problem"],
                "Difficulty": entry["difficulty"],
                "Pattern": entry["pattern"],
                "Reviews": entry["reviews"],
                "Last Reviewed": entry["last_reviewed"],
                "Mastery": entry["mastery"],
            }

            print("\n" + "=" * 40)
            print("PROBLEM FOUND")
            print("=" * 40)

            for key, value in review_info.items():
                print(f"{key}: {value}")

            print("=" * 40)

            confirm = get_confirmation(
                "Is this the problem you reviewed?"
            )

            if confirm == Confirmation.YES:
                problem_info = {
                    "action": action.value,
                    "number": number,
                    "problem": entry["problem"],
                    "difficulty": entry["difficulty"],
                    "pattern": entry["pattern"],
                }

                return problem_info
    
    #_____________________________________
    #   Edit
    #_____________________________________
    number =get_problem_number()
    problem =get_problem_name()
    difficulty = get_problem_difficulty()
    pattern = get_problem_pattern()
    
    
    problem_info={
        "action":action.value,
        "number":number,
        "problem":problem,
        "difficulty":difficulty.value,
        "pattern":pattern
    }
    
    show_summary(problem_info)
    
    make_changes = get_confirmation(
        "Would you like to make any changes?"
    )
    if make_changes == Confirmation.NO:
        return problem_info

    edit_options = {
    "1": ("action", get_action),
    "2": ("number", get_problem_number),
    "3": ("problem", get_problem_name),
    "4": ("difficulty", get_problem_difficulty),
    "5": ("pattern", get_problem_pattern),
}
    changes = {}
    
    while make_changes==Confirmation.YES:
        
        print(
            "\nWhat would you like to change?"
        )
        
        for index, key in enumerate(
            problem_info.keys(),
            start=1
        ):
            print(
                f"{index}. {key.title()}"
            )

        print("6. Done")

      

        choice = input(
            "Enter choice (1-6): "
            ).strip()
        
        # User selected Done
        if choice=="6":
            done = get_confirmation(
                "Are you done making changes?"
            )

            if done == Confirmation.YES:
                make_changes = Confirmation.NO
                break

            continue
        
        # Invalid option
        if choice not in edit_options:
            print(
                "Please choose a number from 1 to 6."
                )
            continue
       
       
        # Retrieve function from hashmap
        key,function =edit_options[choice]
        new_value =function()
        
        
         # Special case: Action.SKIP
        if new_value== Action.SKIP:
            
            cancel = get_confirmation(
                "Do you want to cancel "
                "this progress entry?"
            )

            if cancel == Confirmation.YES:
                return None

            continue
        
        # Enum -> string
        if isinstance(new_value,Enum):
            new_value =new_value.value
            
            
            #update Information
        problem_info[key] = new_value

        changes[key] = new_value

        print(
            f"\nUpdated "
            f"{key.title()} -> {new_value}"
        )

        show_summary(
            problem_info,
            "UPDATED DSA PROBLEM SUMMARY"
        )
        
        
    if changes:

        print("\nChanges made:")

        for key, value in changes.items():
            print(
                f"- {key.title()}: {value}"
            )
        show_summary(
            problem_info,"FINAL DSA PROBLEM SUMMARY"
        )
    return problem_info



def update_progress(info):
    """
    Update progress.json.

    Supports:
    - solve
    - review
    """

    if info is None:
        return

    progress = load_json(
        PROGRESS_FILE
    )

    number = str(info["number"])
    action = info["action"]

    today = date.today().isoformat()

    # -----------------------------------------------------
    # Create problem if it does not exist
    # -----------------------------------------------------

    if number not in progress:

        progress[number] = {
            "problem": info["problem"],
            "difficulty": info["difficulty"],
            "pattern": info["pattern"],
            "solved": None,
            "reviews": 0,
            "last_reviewed": None,
            "mastery": "Learning"
        }

    entry = progress[number]

    # -----------------------------------------------------
    # Solve
    # -----------------------------------------------------

    if action == "solve":

        entry["problem"] = info["problem"]
        entry["difficulty"] = info["difficulty"]
        entry["pattern"] = info["pattern"]

        if entry["solved"] is None:
            entry["solved"] = today

        print(
            f" Recorded solved problem: "
            f"{entry['problem']}"
        )

    # -----------------------------------------------------
    # Review
    # -----------------------------------------------------

    elif action == "review":

        entry["reviews"] += 1

        entry["last_reviewed"] = today

        if entry["reviews"] >= 3:

            entry["mastery"] = "Mastered"

        else:

            entry["mastery"] = "Reviewing"

        print(
            f" Review recorded for: "
            f"{entry['problem']}"
        )

    save_json(
        PROGRESS_FILE,
        progress
    )


# =========================================================
# README statistics
# =========================================================

def calculate_stats(progress):
    """
    Calculate DSA statistics.
    """

    total = len(progress)

    easy = 0
    medium = 0
    hard = 0

    mastered = 0

    total_reviews = 0

    for entry in progress.values():

        difficulty = entry.get(
            "difficulty",
            ""
        ).lower()

        if difficulty == "easy":
            easy += 1

        elif difficulty == "medium":
            medium += 1

        elif difficulty == "hard":
            hard += 1

        if (
            entry.get("mastery")
            == "Mastered"
        ):

            mastered += 1

        total_reviews += entry.get(
            "reviews",
            0
        )

    return {
        "total": total,
        "easy": easy,
        "medium": medium,
        "hard": hard,
        "mastered": mastered,
        "reviews": total_reviews
    }


# =========================================================
# README generation
# =========================================================

def generate_progress_markdown(progress):
    """
    Generate the dynamic README progress section.
    """

    if not progress:
        return "No problems solved yet."

    stats = calculate_stats(
        progress
    )

    lines = []

    # -----------------------------------------------------
    # Statistics
    # -----------------------------------------------------

    lines.append(
        "### Statistics"
    )

    lines.append("")

    lines.append(
        f"- Problems completed: "
        f"**{stats['total']}**"
    )

    lines.append(
        f"- Easy: **{stats['easy']}**"
    )

    lines.append(
        f"- Medium: **{stats['medium']}**"
    )

    lines.append(
        f"- Hard: **{stats['hard']}**"
    )

    lines.append(
        f"- Total reviews: "
        f"**{stats['reviews']}**"
    )

    lines.append(
        f"- Mastered: "
        f"**{stats['mastered']}**"
    )

    lines.append("")

    # -----------------------------------------------------
    # Problem table
    # -----------------------------------------------------

    lines.append(
        "### Problem Log"
    )

    lines.append("")

    lines.append(
        "| # | Problem | Difficulty | "
        "Pattern | Solved | Reviews | "
        "Last Review | Mastery |"
    )

    lines.append(
        "|---|---|---|---|---|---:|---|---|"
    )

    # -----------------------------------------------------
    # Sort problems by number
    # -----------------------------------------------------

    def sort_key(item):

        key = item[0]

        try:
            return int(key)

        except ValueError:
            return 999999

    sorted_progress = sorted(
        progress.items(),
        key=sort_key
    )

    # -----------------------------------------------------
    # Generate rows
    # -----------------------------------------------------

    for number, entry in sorted_progress:

        solved = (
            entry.get("solved")
            or "-"
        )

        last_reviewed = (
            entry.get("last_reviewed")
            or "-"
        )

        mastery = entry.get(
            "mastery",
            "Learning"
        )

        if mastery == "Mastered":

            mastery_display = (
                " Mastered"
            )

        elif mastery == "Reviewing":

            mastery_display = (
                " Reviewing"
            )

        else:

            mastery_display = (
                " Learning"
            )

        row = (
            f"| {number} "
            f"| {entry.get('problem', '')} "
            f"| {entry.get('difficulty', '')} "
            f"| {entry.get('pattern', '')} "
            f"| {solved} "
            f"| {entry.get('reviews', 0)} "
            f"| {last_reviewed} "
            f"| {mastery_display} |"
        )

        lines.append(row)

    return "\n".join(lines)


def create_default_readme():
    """
    Create README.md automatically
    if it does not exist.
    """

    content = """# DSA Interview Preparation

Data Structures and Algorithms interview preparation using Python.

## Goals

- Build strong pattern recognition
- Practice LeetCode consistently
- Review previously solved problems
- Improve problem-solving speed
- Prepare for technical interviews

## Progress

<!-- PROGRESS_START -->

No problems solved yet.

<!-- PROGRESS_END -->

## Topics

- Arrays
- HashMaps
- Two Pointers
- Sliding Window
- Stacks
- Queues
- Linked Lists
- Binary Search
- Trees
- Heaps
- Graphs
- Backtracking
- Tries
- Union Find
- Greedy
- Dynamic Programming
"""

    with open(
        README_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)

    print(
        " README.md created."
    )


def update_readme():
    """
    Replace everything between:

    <!-- PROGRESS_START -->

    and

    <!-- PROGRESS_END -->

    with generated progress data.
    """

    progress = load_json(
        PROGRESS_FILE
    )

    if not os.path.exists(
        README_FILE
    ):

        create_default_readme()

    with open(
        README_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        content = file.read()

    if (
        PROGRESS_START not in content
        or PROGRESS_END not in content
    ):

        print(
            " README progress markers "
            "not found."
        )

        return

    generated = (
        generate_progress_markdown(
            progress
        )
    )

    before = content.split(
        PROGRESS_START,
        1
    )[0]

    after = content.split(
        PROGRESS_END,
        1
    )[1]

    new_content = (
        before
        + PROGRESS_START
        + "\n\n"
        + generated
        + "\n\n"
        + PROGRESS_END
        + after
    )

    with open(
        README_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            new_content
        )

    print(
        " README.md updated."
    )


# =========================================================
# Git commit / push
# =========================================================

def has_staged_changes():
    """
    Return True if there are staged
    changes waiting to be committed.
    """

    result = subprocess.run(
        [
            "git",
            "diff",
            "--cached",
            "--quiet"
        ]
    )

    return result.returncode == 1


def commit_and_push():
    """
    Ask for a commit message,
    stage files,
    commit,
    and push.
    """

    print(
        "\n Git Commit"
    )

    commit_message = input(
        "Enter commit message: "
    ).strip()

    if not commit_message:

        print(
            " Commit message "
            "cannot be empty."
        )

        return

    # -----------------------------------------------------
    # Stage files
    # -----------------------------------------------------

    print(
        "\n Adding changes..."
    )

    run([
        "git",
        "add",
        "."
    ])

    # -----------------------------------------------------
    # Check staged files
    # -----------------------------------------------------

    if not has_staged_changes():

        print(
            " Nothing new to commit."
        )

        return

    # -----------------------------------------------------
    # Commit locally
    # -----------------------------------------------------

    print(
        f'\n Committing: '
        f'"{commit_message}"'
    )

    run([
        "git",
        "commit",
        "-m",
        commit_message
    ])
    # -----------------------------------------
    # Synchronize with GitHub
    # -----------------------------------------

    sync_with_remote()


    branch = get_current_branch()

    # -----------------------------------------------------
    # Push
    # -----------------------------------------------------

    print(
        "\n Pushing to GitHub..."
    )

    if has_upstream():

        run([
            "git",
            "push"
        ])

    else:

        print(
            f"Setting origin/{branch} "
            f"as the upstream branch..."
        )

        run([
            "git",
            "push",
            "-u",
            "origin",
            branch
        ])

    print(
        "\n Commit pushed successfully!"
    )


# =========================================================
# Main program
# =========================================================

def main():

    print(
        "\n"
        "====================================\n"
        "         DSA Git Assistant\n"
        "===================================="
    )

    # -----------------------------------------------------
    # Step 1:
    # Verify Git repository
    # -----------------------------------------------------

    initialize_git()

    # -----------------------------------------------------
    # Step 2:
    # Load Git configuration
    # -----------------------------------------------------

    config = load_json(
        CONFIG_FILE
    )

    # -----------------------------------------------------
    # Step 3:
    # Verify GitHub remote
    # -----------------------------------------------------

    setup_remote(
        config
    )
   
    

    # -----------------------------------------------------
    # Step 4:
    # Record DSA activity
    # Record multiple DSA activities
    # -----------------------------------------------------
    while True:
        problem_info = (
            ask_problem_information()
        )
        if problem_info is not None:
             # Update progress.json
            update_progress(
                problem_info
            )
        add_another = get_confirmation(
            "Would you like to record another problem?"
        )
        if add_another==Confirmation.NO:
            break


    # -----------------------------------------------------
    # Step 5:
    # Regenerate README
    # -----------------------------------------------------

    update_readme()

    # -----------------------------------------------------
    # Step 6:
    # Commit and push
    # -----------------------------------------------------

    commit_and_push()


# =========================================================
# Program entry point
# =========================================================

if __name__ == "__main__":
    main()