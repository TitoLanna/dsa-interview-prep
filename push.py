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
DOCS_PROGRESS_FILE = os.path.join("docs", "progress.json")

PROGRESS_START = "<!-- PROGRESS_START -->"
PROGRESS_END = "<!-- PROGRESS_END -->"

# Maps a progress.json problem number to the solution file that
# holds its code. Kept explicit (rather than fuzzy-matched) because
# a few problem names don't line up cleanly with their filenames.
SOLUTION_FILE_MAP = {
    "1": "arrays/Two Sum .py",
    "2": "arrays/Best Time to Buy and Sell Stock.py",
    "3": "arrays/Best Time to Buy and Sell Stock II.py",
    "4": "arrays/Remove Duplicates from Sorted Array.py",
    "5": "arrays/Product of Array Except Self.py",
    "6": "arrays/Maximum Subarray.py",
    "7": "arrays/Spiral Matrix.py",
    "8": "arrays/Subarray Sum Equals K.py",
    "9": "hashmaps/Contains Duplicate.py",
    "10": "hashmaps/Valid Anagram.py",
    "11": "hashmaps/Group Anagrams.py",
    "12": "hashmaps/Longest Consecutive Sequence.py",
    "13": "hashmaps/Insert Delete GetRandom O(1).py",
    "14": "two_pointers/Valid Palindrome.py",
    "15": "two_pointers/Valid Palindrome II.py",
    "16": "two_pointers/Two Sum II - Input Array Is Sorted.py",
    "17": "two_pointers/11. Container With Most Water.ipynb",
    "18": "two_pointers/3Sum.py",
    "19": "two_pointers/Trapping Rain Water.py",
    "20": "sliding_window/Maximum Average Subarray I.py",
    "21": "sliding_window/ Longest Substring Without Repeating Characters.py",
    "22": "sliding_window/Minimum Size Subarray Sum.py",
    "23": "sliding_window/Longest Repeating Character Replacement.py",
    "24": "sliding_window/ Permutation in String.py",
}

# Maps a progress.json problem number to its primary pattern-handbook
# topic id (docs/patterns.json) and LeetCode number, so the review app
# can show recognition signals / templates / common mistakes alongside
# the problem. Derived from the handbook's own LeetCode ladder tables.
PROBLEM_TOPIC_MAP = {
    "1": {"topic": "arrays-strings", "leetcode_number": 1},
    "2": {"topic": "arrays-strings", "leetcode_number": 121},
    "3": {"topic": "arrays-strings", "leetcode_number": 122},
    "4": {"topic": "arrays-strings", "leetcode_number": 26},
    "5": {"topic": "arrays-strings", "leetcode_number": 238},
    "6": {"topic": "arrays-strings", "leetcode_number": 53},
    "7": {"topic": "arrays-strings", "leetcode_number": 54},
    "8": {"topic": "arrays-strings", "leetcode_number": 560},
    "9": {"topic": "hash-maps-sets", "leetcode_number": 217},
    "10": {"topic": "hash-maps-sets", "leetcode_number": 242},
    "11": {"topic": "hash-maps-sets", "leetcode_number": 49},
    "12": {"topic": "hash-maps-sets", "leetcode_number": 128},
    "13": {"topic": "hash-maps-sets", "leetcode_number": 380},
    "14": {"topic": "two-pointers", "leetcode_number": 125},
    "15": {"topic": "two-pointers", "leetcode_number": 680},
    "16": {"topic": "two-pointers", "leetcode_number": 167},
    "17": {"topic": "two-pointers", "leetcode_number": 11},
    "18": {"topic": "two-pointers", "leetcode_number": 15},
    "19": {"topic": "two-pointers", "leetcode_number": 42},
    "20": {"topic": "sliding-window", "leetcode_number": 643},
    "21": {"topic": "sliding-window", "leetcode_number": 3},
    "22": {"topic": "sliding-window", "leetcode_number": 209},
    "23": {"topic": "sliding-window", "leetcode_number": 424},
    "24": {"topic": "sliding-window", "leetcode_number": 567},
}


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

from datetime import date, timedelta

def update_sm2(entry, quality):
    """
    Update spaced-repetition fields using
    an SM-2-style review schedule.
    """

    if quality < 0 or quality > 5:
        raise ValueError(
            "Quality must be between 0 and 5."
        )

    repetitions = entry.get(
        "repetitions",
        0
    )

    interval = entry.get(
        "interval",
        1
    )

    ease_factor = entry.get(
        "ease_factor",
        2.5
    )

    if quality < 3:

        repetitions = 0
        interval = 1

    else:

        if repetitions == 0:
            interval = 1

        elif repetitions == 1:
            interval = 6

        else:
            interval = round(
                interval * ease_factor
            )

        repetitions += 1

    ease_factor += (
        0.1
        - (5 - quality)
        * (
            0.08
            + (5 - quality) * 0.02
        )
    )

    ease_factor = max(
        1.3,
        ease_factor
    )

    entry["repetitions"] = repetitions
    entry["interval"] = interval

    entry["ease_factor"] = round(
        ease_factor,
        2
    )

    entry["next_review"] = (
        date.today()
        + timedelta(days=interval)
    ).isoformat()

    return entry

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

    def get_quality():
        while True:
            user_input = input(
                "Rate your recall 0-5 "
                "(0=blackout, 3=correct but hard, 5=perfect): "
            ).strip()

            try:
                quality = int(user_input)
            except ValueError:
                print("Please enter a number from 0 to 5.")
                continue

            if 0 <= quality <= 5:
                return quality

            print("Please enter a number from 0 to 5.")


    
    
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
                quality = get_quality()

                problem_info = {
                    "action": action.value,
                    "number": number,
                    "problem": entry["problem"],
                    "difficulty": entry["difficulty"],
                    "pattern": entry["pattern"],
                    "quality": quality,
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

        quality = info.get("quality")

        if quality is not None:
            update_sm2(entry, quality)

        if entry["reviews"] >= 3:

            entry["mastery"] = "Mastered"

        else:

            entry["mastery"] = "Reviewing"

        print(
            f" Review recorded for: "
            f"{entry['problem']}"
        )

        if quality is not None:
            print(
                f" Next review: {entry['next_review']} "
                f"(interval: {entry['interval']}d, "
                f"ease: {entry['ease_factor']})"
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
# Docs site data (GitHub Pages review app)
# =========================================================

def extract_code(path):
    """
    Read the solution source for a problem.

    Supports plain .py files and .ipynb notebooks
    (code cells are concatenated in order).

    Returns None if the file is missing or unreadable.
    """

    if not path or not os.path.exists(path):
        return None

    if path.endswith(".ipynb"):

        try:
            with open(path, "r", encoding="utf-8") as file:
                notebook = json.load(file)

        except (json.JSONDecodeError, OSError):
            return None

        code_parts = []

        for cell in notebook.get("cells", []):

            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))

                if source.strip():
                    code_parts.append(source)

        return "\n\n".join(code_parts) if code_parts else None

    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def generate_docs_progress():
    """
    Build docs/progress.json for the GitHub Pages review app:
    a copy of progress.json with each problem's solution code
    embedded, so the static site never needs to fetch outside
    of docs/.
    """

    progress = load_json(PROGRESS_FILE)

    docs_data = {}

    for number, entry in progress.items():

        file_path = SOLUTION_FILE_MAP.get(number)
        topic_info = PROBLEM_TOPIC_MAP.get(number, {})

        docs_entry = dict(entry)
        docs_entry["file"] = file_path
        docs_entry["code"] = extract_code(file_path)
        docs_entry["topic"] = topic_info.get("topic")
        docs_entry["leetcode_number"] = topic_info.get("leetcode_number")

        docs_data[number] = docs_entry

    os.makedirs("docs", exist_ok=True)

    save_json(DOCS_PROGRESS_FILE, docs_data)

    print(" docs/progress.json generated.")


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
    # Regenerate docs/progress.json for the review app
    # -----------------------------------------------------

    generate_docs_progress()

    # -----------------------------------------------------
    # Step 7:
    # Commit and push
    # -----------------------------------------------------

    commit_and_push()


# =========================================================
# Program entry point
# =========================================================

if __name__ == "__main__":
    main()