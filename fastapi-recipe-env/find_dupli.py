import os
import re
from collections import Counter

def find_duplicate_classes(directory):
    class_pattern = re.compile(r'^\s*class\s+(\w+)')
    class_names = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = class_pattern.match(line)
                        if match:
                            class_name = match.group(1)
                            if class_name in class_names:
                                class_names[class_name].append(file_path)
                            else:
                                class_names[class_name] = [file_path]

    duplicates = {cls: paths for cls, paths in class_names.items() if len(paths) > 1}

    if duplicates:
        print("\n🚨 Duplicate class names found! 🚨")
        for cls, paths in duplicates.items():
            print(f"\nClass '{cls}' appears in:")
            for path in paths:
                print(f"  - {path}")
    else:
        print("✅ No duplicate class names found!")

# Run the function in the current directory
if __name__ == "__main__":
    find_duplicate_classes(".")
