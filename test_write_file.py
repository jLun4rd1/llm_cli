from functions.write_file import write_file


def run_write_file(working_dir, target_file, content):
    print(f"Content to write:\n {content}")
    print(f"Result for '{target_file}' file:")
    print(write_file(working_dir, target_file, content))

def main():
    run_write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print("-----")
    run_write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print("-----")
    run_write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

if __name__ == "__main__":
    main()
