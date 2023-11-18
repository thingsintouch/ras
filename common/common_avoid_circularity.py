def insert_line_at_top(file_path, line_to_insert):
    file = None  # Initialize file variable outside the try-except block
    try:
        # Read the existing file content
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            lines = file.readlines()
        # Insert the new line at the top
        lines = [str(line_to_insert)] + lines

        # Ensure the file has less than 400 lines by deleting the last line if necessary
        if len(lines) > 500:
            lines.pop()

        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        # Create the file if it doesn't exist
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(line_to_insert)
            print(f"File {file_path} created with the inserted line")

    except Exception as e:
        print(f"could not write line at top of file - Exception: {e}")

    finally:
        if file and not file.closed:
            file.close()  # Ensure the file is closed even if an exception occurred