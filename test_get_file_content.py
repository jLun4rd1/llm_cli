from config import MAX_CHARS
from functions.get_file_content import get_file_content

def run_get_file_content(working_dir, target_file):
    print(f"Result for '{target_file}' file:")

    file_content = get_file_content(working_dir, target_file)

    if "[..." in file_content and "characters]" in file_content:
        print(f"File should be over {MAX_CHARS} characters long")

    if len(file_content) > MAX_CHARS:
        print(f"Total file length: {len(file_content)}")
    else:
        print(file_content)

def main():
    run_get_file_content("calculator", "lorem.txt")
    print("-----")
    run_get_file_content("calculator", "main.py")
    print("-----")
    run_get_file_content("calculator", "pkg/calculator.py")
    print("-----")
    run_get_file_content("calculator", "/bin/cat")
    print("-----")
    run_get_file_content("calculator", "pkg/does_not_exist.py")

if __name__ == "__main__":
    main()
