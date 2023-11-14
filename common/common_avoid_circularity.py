
def insert_line_at_top(file_path, line_to_insert):
    try:
        # Read the existing file content
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            lines = file.readlines()

        # Insert the new line at the top
        lines.insert(0, line_to_insert)

        # Ensure the file has less than 400 lines by deleting the last line if necessary
        if len(lines) > 500:
            lines.pop()

        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

        # print(f"Line inserted successfully in {file_path}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        # Create the file if it doesn't exist
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(line_to_insert)
            print(f"File {file_path} created with the inserted line")

def clean_non_utf8(text):
    cleaned_text = ""
    for char in text:
        try:
            char.encode('utf-8')
            cleaned_text += char
        except UnicodeEncodeError:
            cleaned_text += '?'  # Replace non-UTF-8 character with a placeholder

    return cleaned_text