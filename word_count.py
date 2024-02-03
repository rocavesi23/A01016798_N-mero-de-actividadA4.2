""" 
word_count.py - A Python program that takes a file as a command line parameter, processes the file 
to identify distinct words and their frequencies, handles invalid data in the file, and outputs 
the results both on the screen and in a file named WordCountResults.txt. The program also calculates 
and displays the elapsed time for execution and data calculation. It is compliant with PEP 8 style
conventions and can handle files with hundreds to thousands of items.

Requirements:
- The program is invoked from the command line, taking a file as a parameter.
- Invalid data in the file is handled, and errors are displayed without interrupting execution.
- The execution time, including the calculation time, is displayed at the end.

Usage:
python convertNumbers.py fileWithData.txt
"""
import time
import sys

def process_file(file_path):
    """
    Process the file and get word frequencies

    :param file_path: Path to the file to process
    :return: Dictionary of word frequencies
    """
    # Dictionary to store word frequencies
    word_count_dictionary = {}

    try:
        # Open file and iterate through lines
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Split line into words
                words = line.split()
                for dirty_word in words:
                    # Clean up word (remove punctuation and convert to lowercase)
                    clean_word = dirty_word.strip('.,!?()[]{}":;')
                    clean_word = clean_word.lower()

                    # Update word count
                    word_count_dictionary[clean_word] = word_count_dictionary.get(clean_word, 0) + 1

    except FileNotFoundError:
        # Handle file not found error
        print(f"Error: File '{file_path}' not found.")
        return None

    return word_count_dictionary

def save_results(word_count_dictionary, elpsed_time):
    """
    Save the word frequencies to a file and print elapsed time

    :param word_count: Dictionary of word frequencies
    :param elapsed_time: Elapsed time for execution
    """
    result_file_path = 'WordCountResults.txt'

    # Open result file and write word frequencies
    with open(result_file_path, 'w', encoding='utf-8') as result_file:
        for final_word, final_count in word_count_dictionary.items():
            result_file.write(f"{final_word}: {final_count}\n")

        # Write elapsed time to the result file
        result_file.write(f"\nElapsed Time: {elpsed_time:.5f} seconds")

    # Print message about results file
    print(f"Results saved to {result_file_path}")

if __name__ == "__main__":
    # Check for the correct number of command line arguments
    if len(sys.argv) != 2:
        print("Usage: python wordCount.py fileWithData.txt")
        sys.exit(1)

    # Record start time for execution duration
    start_time = time.time()
    INPUT_FILE = sys.argv[1]

    # Process the file and get word frequencies
    word_count = process_file(INPUT_FILE)

    if word_count is not None:
        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        # Print results on the screen
        for word, count in word_count.items():
            print(f"{word}: {count}")

        # Save results to a file
        save_results(word_count, elapsed_time)
        print(f"\nElapsed Time: {elapsed_time:.5f} seconds")
