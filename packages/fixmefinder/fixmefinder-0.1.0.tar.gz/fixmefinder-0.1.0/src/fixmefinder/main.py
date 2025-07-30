import os
from pathlib import Path
from sys import argv

from fixmefinder.entry import Entry
from fixmefinder.finder import find_fixme_comments
from fixmefinder.issuemaker import make_issue
from fixmefinder.linear import create_issue, LINEAR_TEAM_ID
from fixmefinder.file_updater import update_comment_in_file

def main():
    directory = Path(os.getcwd())
    try:
        if Path(argv[1]).is_dir():
            directory = Path(argv[1])
    except Exception:
        pass

    entries = find_fixme_comments(directory)
    print(f"Found {len(entries)} FIXME or TODO comments in {directory}.")
    
    unhandled_entries = set(filter(lambda e: e.issue_tracker_id is None, entries))

    if not unhandled_entries:
        print("No unhandled FIXME or TODO comments found.")
        return
    
    for entry in unhandled_entries:
        title, body = make_issue(entry)
        print("~" * 50)
        print(f"Creating issue: {title}")
        print(body)

        response = create_issue(title, body, LINEAR_TEAM_ID)
        if not response.success:
            continue

        print(f"Issue created: {response.issue.title} (ID: {response.issue.identifier})")
        
        new_entry = Entry(type=entry.type, text=entry.text, location=entry.location, issue_tracker_id=response.issue.identifier)

        print(f"Updated entry: {new_entry.format()}")

        update_comment_in_file(entry, new_entry)
        

if __name__ == "__main__":
    main()
