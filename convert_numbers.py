"""
convertNumbers.py - A Python program that reads a file containing a list of numbers,
converts each number to binary and hexadecimal representations using basic algorithms
and prints the results on the screen and in a file named 'ConvertionResults.txt'.

Requirements:
- The program is invoked from the command line, taking a file as a parameter.
- Invalid data in the file is handled, and errors are displayed without interrupting execution.
- The execution time, including the calculation time, is displayed at the end.

Usage:
python convertNumbers.py fileWithData.txt
"""
import sys
import time

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
            number = int(value)
            numbers.append(number)
        except ValueError as exception:
            print(f"Warning: The record with the value: '{value}' is "
                  f"not a valid number - {exception}")

    return numbers

def decimal_a_binario_complemento_a_2(numero_decimal, numero_bits):
    """
    Convierte un número decimal a binario usando complemento a 2 con algoritmos básicos.

    Parámetros:
    numero_decimal: El número decimal a convertir.
    numero_bits: El número de bits a usar en la representación binaria.

    Retorno:
    Una cadena que representa el número decimal en binario usando complemento a 2.
    """

    if numero_decimal >= 0:
        # Conversión a binario estándar
        binario = ""
        while numero_decimal > 0:
            binario = str(numero_decimal % 2) + binario
            numero_decimal //= 2
        # Rellenar con ceros a la izquierda si es necesario
        binario = binario.zfill(numero_bits)
    else:
        # Conversión a complemento a 1
        binario_complemento_a_1 = ""
        numero_decimal = abs(numero_decimal)
        while numero_decimal > 0:
            binario_complemento_a_1 = str(numero_decimal % 2) + binario_complemento_a_1
            numero_decimal //= 2
        # Rellenar con ceros a la izquierda si es necesario
        binario_complemento_a_1 = binario_complemento_a_1.zfill(numero_bits)
        # Convertir a complemento a 2 sumando 1
        binario = ""
        llevar = 1
        for i in range(numero_bits):
            suma = int(binario_complemento_a_1[i]) + llevar
            llevar = suma // 2
            binario = str(suma % 2) + binario

    return binario

def sum_with_carry(bit1, bit2, carry):
    """
    Realizes the sum of bits considering the carry.

    Args:
        bit1 (int): The first bit.
        bit2 (int): The second bit.
        carry (int): The carry from the previous sum.

    Returns:
        tuple: A tuple containing the result of the sum and the new carry.
    """
    # Performs the sum of bits considering the carry
    result = bit1 ^ bit2 ^ carry

    # Calculates the new carry
    new_carry = (bit1 & bit2) | ((bit1 ^ bit2) & carry)

    return result, new_carry

def binary_addition(binary1, binary2):
    """
    Adds two binary numbers.

    Args:
        binary1 (str): The first binary number.
        binary2 (str): The second binary number.

    Returns:
        str: The result of the binary addition.
    """
    # Ensure both strings have the same length, padding with zeros on the left if necessary
    length = max(len(binary1), len(binary2))
    binary1 = binary1.zfill(length)
    binary2 = binary2.zfill(length)

    result = ''
    carry = 0

    # Iterate from the least significant bit to the most significant bit
    for i in range(length - 1, -1, -1):
        bit1 = int(binary1[i])
        bit2 = int(binary2[i])

        # Perform binary addition with carry
        sum_result, carry = sum_with_carry(bit1, bit2, carry)

        # Add the result to the beginning of the string
        result = str(sum_result) + result

    # If there is a final carry, add it to the result
    if carry:
        result = '1' + result

    return result

def convert_to_binary(number):
    """
    Converts a decimal number to binary.

    Args:
        number (int): The decimal number to be converted.

    Returns:
        str: The binary representation of the input number.
    """
    if number == 0:
        binary_result = '0'
    else:
        is_negative = False

        if number < 0:
            is_negative = True
            number = abs(number)

        # Convert to binary
        binary_result = ''
        while number > 0:
            binary_result = str(number % 2) + binary_result
            number //= 2

        # Pad with zeros to ensure 32 bits
        binary_result = '0' * (10 - len(binary_result)) + binary_result

        if is_negative:
            # Perform two's complement for 32 bits
            binary_result = ''.join('1' if bit == '0' else '0' for bit in binary_result)
            binary_result = binary_addition(binary_result, '0000000001')

        # Remove leading zeros
        binary_result = binary_result[binary_result.index('1'):] if '1' in binary_result else '0'

    return binary_result

def convert_to_hexadecimal(number):
    """
    Converts a decimal number to hexadecimal.

    Args:
        number (int): The decimal number to be converted.

    Returns:
        str: The hexadecimal representation of the input number.
    """
    number_original = number
    hexadecimal_result = ''

    if number == 0:
        hexadecimal_result = '0'
    else:
        if number < 0:
            number = abs(number)

            # Convert to binary
            binary_result = ''
            while number > 0:
                binary_result = str(number % 2) + binary_result
                number //= 2

            # Pad with zeros to ensure 40 bits
            binary_result = '0' * (40 - len(binary_result)) + binary_result

            # Perform two's complement for 32 bits
            binary_result = ''.join('1' if bit == '0' else '0' for bit in binary_result)
            binary_result = binary_addition(binary_result, '0' * 39 + '1')

            # Ensure multiple of 4
            binary_result = binary_result.zfill((len(binary_result) + 3) // 4 * 4)
            hex_chars = '0123456789ABCDEF'

            for i in range(0, len(binary_result), 4):
                chunk = binary_result[i:i+4]
                decimal_value = int(chunk, 2)
                hexadecimal_result += hex_chars[decimal_value]

        else:
            # Convert to hexadecimal
            temp_number = abs(number_original)
            while temp_number > 0:
                remainder = temp_number % 16
                if remainder < 10:
                    hexadecimal_result = str(remainder) + hexadecimal_result
                else:
                    hexadecimal_result = chr(ord('A') + remainder - 10) + hexadecimal_result
                temp_number //= 16

    return hexadecimal_result

def process_file(file_path):
    """
    Reads a file containing a list of numbers, converts each number to binary and hexadecimal,
    and returns the results.

    Args:
        file_path (str): The path to the input file.

    Returns:
        list or None: A list of tuples containing the original number, binary, and hexadecimal 
                      representations.
        Returns None if there is an error reading the file or converting the numbers.
    """
    try:
        data = read_file(file_path)

        # Check if the data list is not empty.
        if not data:
            print("Error: Empty data in the file.")
            return None

        total_records = len(data)
        # Print the results to the screen.
        print("Total records to analyze:", total_records)


        numbers = convert_to_numbers(data)

        results = []
        for number in numbers:
            binary = convert_to_binary(number)
            hexadecimal = convert_to_hexadecimal(number)
            results.append((number, binary, hexadecimal))

        return results

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except ValueError as exception:
        print(f"Error: {exception}")
        return None

def write_results_to_file(results):
    """
    Writes the conversion results to a file named 'ConvertionResults.txt'.

    Args:
        results (list): A list of tuples containing the original number, binary
                        and hexadecimal representations.
    """
    print(f"write huesos Total records analyzed: {len(results)}")

    with open("ConvertionResults.txt", 'w', encoding="utf-8") as result_file:
        for result in results:
            result_file.write(f"Number: {result[0]}, "
                              f"Binary: {result[1]}, "
                              f"Hexadecimal: {result[2]}\n")

def main():
    """
    The main function that orchestrates the execution of the program.

    Parses command line arguments, processes the input file, performs conversions,
    writes results to a file, and prints the results along with the elapsed time.
    """
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py fileWithData.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    conversion_results = process_file(input_file)

    if conversion_results is not None:
        write_results_to_file(conversion_results)
        for result in conversion_results:
            print(f"Number: {result[0]}, Binary: {result[1]}, Hexadecimal: {result[2]}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time elapsed: {elapsed_time} seconds")
    # Print the time elapsed to the file.
    with open("ConvertionResults.txt", "a", encoding="utf-8") as file:
        file.write(f"Elapsed time: {elapsed_time}\n")


if __name__ == "__main__":
    main()
