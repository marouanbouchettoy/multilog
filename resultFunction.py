import os


def saveResult(result):
    file_foder = "results"
    file_path = file_foder + "/results.txt"  # Specify the path to your text file

    if not os.path.exists(file_path):
        os.mkdir(file_foder)
        with open(file_path, 'w') as file:
            pass  # File created

    # Open the file in append mode ('a')
    with open(file_path, 'a') as file:
        # Write the result to the file
        file.write(result + "\n")  # Add a newline for readability
