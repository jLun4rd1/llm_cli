from functions.run_python_file import run_python_file


def test_run_python_file(working_dir, target_file, args=None):
    print(f"Result after running '{target_file}' inside '{working_dir}':")
    if args:
        print(f"Args passed:\n{args}")
    print(run_python_file(working_dir, target_file, args))

def main():
    test_run_python_file("calculator", "main.py")
    test_run_python_file("calculator", "main.py", ["3 + 5"])
    test_run_python_file("calculator", "tests.py")
    test_run_python_file("calculator", "../main.py")
    test_run_python_file("calculator", "nonexistent.py")
    test_run_python_file("calculator", "lorem.txt")

if __name__ == "__main__":
    main()
