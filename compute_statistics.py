"""
compute_statistics.py

This module contains a program that performs basic statistical calculations (mean, 
median, mode, standard deviation and variance) using a data file provided as a 
command line parameter and prints the results on the screen and in a file named 
'StatisticsResults.txt'.

Requirements:
- The program is invoked from the command line, taking a file as a parameter.
- Invalid data in the file is handled, and errors are displayed without interrupting execution.
- The execution time, including the calculation time, is displayed at the end.

Usage:
python compute_statistics.py fileWithData.txt
"""
import sys
import time
from collections import Counter


def read_file(file_name):
    """
    Reads the contents of a file and returns a list of values.

     :param file_name: Name of the file to read.
     :return: List of values in the file or an empty list if the file is not found.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read().splitlines()
    except FileNotFoundError as exception:
        print(f"Error: File not found - {exception.filename}")
        return []

def convert_to_numbers(data):
    """
    This function converts the records in a list to numbers by 
    validating that the value is a valid number
    """
    numbers = []

    for value in data:
        try:
            number = float(value)
            numbers.append(number)
        except ValueError as exception:
            print(f"Warning: The record with the value: '{value}' is "
                  f"not a valid number - {exception}")

    return numbers

def calculate_statistics(data):
    """
    Calculates the basic descriptive statistics (mean, median, mode, standard 
    deviation and variance) for a list of numbers.
    
    :param data: List of numbers.
    :return: A dictionary with the statistics data.    
    """
    # Get the total number of records
    total_valid_records = len(data)

    # Compute the mean.
    mean = sum(data) / len(data)

    # Compute the median.
    data.sort()
    if len(data) % 2 == 0:
        median = (data[len(data) // 2] + data[len(data) // 2 - 1]) / 2
    else:
        median = data[len(data) // 2]

    # Compute the mode.
    # Calcular la frecuencia de cada elemento
    counter = Counter(data)

    # Find the maximum frequency
    max_frequency = max(counter.values())

    # Get all elements that have the maximum frequency
    mode = [value for value, frequency in counter.items() if frequency == max_frequency]
    #If the result is multimodal we take the maximum value
    mode = max(mode)

    # Compute the standard deviation.
    standard_deviation = (sum((x - mean) ** 2 for x in data) / len(data)) ** 0.5

    # Calculate variance.
    variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1.0)

    # Print the results to the screen.
    print("Total valid records:", total_valid_records)
    print("Mean:", mean)
    print("Median:", median)
    print("Mode(s):", mode)
    print("Standard deviation:", standard_deviation)
    print("Variance:", variance)

    statistics_data = {
        'total_records': 0,
        'total_valid_records': total_valid_records,
        'mean': mean,
        'median': median,
        'mode': mode,
        'standard_deviation': standard_deviation,
        'variance': variance
    }

    return statistics_data

def write_to_file(file_name, statistic_data):
    """
    Writes the statistics to a file.

     :param file_name: Name of the file to write to.
     :param total_records: Total number of records in the file.
     :param total_valid_records: Total number of valid records in the file.
     :param mean: Mean of the data.
     :param median: Median of the data.
     :param mode: Mode of the data.
     :param standard_deviation: Standard deviation of the data.
     :param variance: Variance of the data.
    """
    # Print the results to a file.
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(f"Count: {statistic_data['total_records']}\n")
        file.write(f"Count valid records: {statistic_data['total_valid_records']}\n")
        file.write(f"Mean: {statistic_data['mean']}\n")
        file.write(f"Median: {statistic_data['median']}\n")
        file.write(f"Mode: {statistic_data['mode']}\n")
        file.write(f"Standard deviation: {statistic_data['standard_deviation']}\n")
        file.write(f"Variance: {statistic_data['variance']}\n")

# Main function
def compute_statistics(file_name):
    """
    This function calculates the basic descriptive statistics (mean, 
    median, mode, standard deviation and variance) for the data 
    contained in the specified file.

     :param file_name: Name of the file containing the data.
    """
    start_time = time.time()

    try:
        # Read the file contents.
        data = read_file(file_name)

        # Check if the data list is not empty.
        if not data:
            print("Error: Empty data in the file.")
            return

        total_records = len(data)
        # Print the results to the screen.
        print("Total records to analyze:", total_records)

        # Convert the data to numbers.
        data = convert_to_numbers(data)
        # Calculate the statistics.
        statistic_data =  calculate_statistics(data)
        statistic_data['total_records'] = total_records

        # Write the results to a file.
        write_to_file("StatisticsResults.txt", statistic_data)

        # Get the time elapsed for the execution.
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Print the time elapsed to the screen.
        print("Elapsed time:", elapsed_time)

        # Print the time elapsed to the file.
        with open("StatisticsResults.txt", "a", encoding="utf-8") as file:
            file.write(f"Elapsed time: {elapsed_time}\n")

    except FileNotFoundError as exception :
        print(f"Error: File not found - {exception .filename}")
    except ValueError as exception:
        print(f"Error: Invalid data in the file - {exception}")
    except PermissionError as exception:
        print(f"Error: Permission error - {exception}")
    except IOError as exception:
        print(f"Error: I/O error - {exception}")
    except TypeError as exception:
        print(f"Error: Type error - {exception}")
    except ZeroDivisionError as exception:
        print(f"Error: Division by zero - {exception}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compute_statistics.py fileWithData.txt")
    else:
        compute_statistics(sys.argv[1])
