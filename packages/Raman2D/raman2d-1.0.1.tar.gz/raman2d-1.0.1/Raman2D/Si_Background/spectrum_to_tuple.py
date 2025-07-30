"""
Convert a text file containing spectrum data into a Python file
with the data as a list of tuples. Can be used for background sub.
"""
import string


def convert_spectrum_to_python(input_file, output_file):
    """
    Convert a text file containing spectrum data into a Python file
    with the data as a list of tuples.

    Parameters:
        input_file (str): Path to the input text file
         containing the spectrum data.
        output_file (str): Path to the output Python file
         where the data will be saved.
    """
    # Initialize a list to store tuples of data
    data_tuples = []

    try:
        # Read the input file and process lines
        with open(input_file, 'r') as file:
            for line in file:
                # Strip unwanted whitespace and skip empty lines
                line = line.strip(string.whitespace)
                if line:
                    # Split the line by semicolon and convert values to float
                    x, y = map(float, line.split(';'))
                    data_tuples.append((x, y))
    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
        return
    except ValueError as err:
        print(f"Error: Invalid data format in the file. {err}")
        return

    try:
        # Write the processed data into a Python file
        with open(output_file, 'w') as file:
            file.write('"""\nIntegrated reference spectrum '
                       'for background calibration\n"""\n\n')
            file.write("REFERENCE_SPECTRUM = [\n")
            for x, y in data_tuples:
                file.write(f"    ({x:.15g}, {y:.15g}),\n")
            file.write("]\n")
        print(f"The data has been successfully "
              f"processed and saved in {output_file}.")
    except IOError as err:
        print(f"Error: Could not write to the file {output_file}. {err}")


# Example usage
INPUT = r"C:\Users\TM273821\Desktop\Raman\Ref_Si\0.0_0.0_smoothed.txt"
OUTPUT = r"C:\Users\TM273821\Desktop\Raman\Ref_Si\Si_background.py"
convert_spectrum_to_python(INPUT, OUTPUT)
