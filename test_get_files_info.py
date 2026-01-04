from functions.get_files_info import get_files_info


def run_get_files_info(working_dir, target_dir):
    result_text = f"Result for '{target_dir}' directory:"
    if target_dir == ".":
        result_text = result_text.replace(f"'{target_dir}'", "current")

    print(result_text)
    print(get_files_info(working_dir, target_dir))

def main():
    run_get_files_info("calculator", ".")
    run_get_files_info("calculator", "pkg")
    run_get_files_info("calculator", "/bin")
    run_get_files_info("calculator", "../")

if __name__ == "__main__":
    main()
