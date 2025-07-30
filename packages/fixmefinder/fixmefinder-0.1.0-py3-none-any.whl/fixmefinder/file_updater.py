from pathlib import Path

from fixmefinder.entry import Entry

def update_comment_in_file(old_entry: Entry, new_entry: Entry) -> None:
    file_path = Path(old_entry.location.file)
    try:
        with file_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        line_idx = old_entry.location.start.line - 1  # zero-based
        if line_idx >= len(lines):
            raise IndexError(f"Line index {line_idx} out of range in {file_path}")

        original_line = lines[line_idx]
        formatted_entry = new_entry.format()

        col = old_entry.location.start.column - 1
        if 0 <= col < len(original_line):
            updated_line = original_line[:col] + formatted_entry + "\n"
        else:
            updated_line = formatted_entry + "\n"

        lines[line_idx] = updated_line

        with file_path.open("w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"Patched file: {file_path}")
    except Exception as e:
        print(f"Failed to update file {file_path}: {e}")
