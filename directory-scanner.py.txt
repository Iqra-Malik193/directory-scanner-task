import os
from datetime import datetime

folder_path = input("Enter folder path: ")

output_file = "output.txt"

with open(output_file, "w") as file:
    file.write("DIRECTORY SCANNER REPORT\n")
    file.write("=" * 50 + "\n\n")

    for root, dirs, files in os.walk(folder_path):
        file.write(f"\nFolder: {root}\n")
        file.write("-" * 50 + "\n")

        for name in files:
            file_path = os.path.join(root, name)

            size = os.path.getsize(file_path)
            extension = os.path.splitext(name)[1]
            modified = datetime.fromtimestamp(
                os.path.getmtime(file_path)
            ).strftime("%d-%m-%Y %I:%M:%S %p")

            info = (
                f"File Name: {name}\n"
                f"Size: {size} bytes\n"
                f"Extension: {extension}\n"
                f"Last Modified: {modified}\n"
                + "-" * 40 + "\n"
            )

            print(info)
            file.write(info)

print("Report saved successfully in output.txt")