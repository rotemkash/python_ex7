"""
======================================================================
ex7
======================================================================
Writen by: Rotem kashani, ID = 209073352,   login = rotemkash
	       David Koplev, ID = 208870279 ,    login = davidkop

The purpose of the program is to read an SQL file, extract table names and fields from it, and convert each table's
data into a separate CSV file. The program aims to automate the process of converting SQL data into a more widely
supported CSV format.

The input for the program is the file path of an SQL file. This file should contain SQL statements, including
 table creation (`CREATE TABLE`) and data insertion (`INSERT INTO`) statements. The program reads this SQL file and
  extracts the table names and fields to convert them into CSV files.


  The output of the program is one or more CSV files. Each CSV file corresponds to a table in the input SQL file.
  The program converts the table data into CSV format and writes it to separate CSV files. The filename of each CSV
  file is derived from the table name in the SQL file. The resulting CSV files contain the table data in a structured,
   comma-separated format that can be easily opened and processed by various applications or used for data analysis
   purposes.
"""

import re
import csv


def read_sql_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()  # Read file and split lines

        # Rest of the code remains unchanged

        table_start_pattern = re.compile(r'^CREATE TABLE `(\w+)`')
        insert_pattern = re.compile(r'^INSERT INTO `(\w+)` VALUES (.+)')

        table_name = None
        table_fields = []
        table_count = 0

        for line in lines:
            line = line.strip()

            if table_start_pattern.match(line):
                table_name = table_start_pattern.match(line).group(1)
                table_fields = []
            elif insert_pattern.match(line):
                if table_name is not None:
                    values = insert_pattern.match(line).group(2)

                    # Split multiline INSERT INTO statements into separate lines
                    values = re.sub(r'\),\(', '),\n(', values)
                    values = values.splitlines()

                    table_fields.extend(values)

            if table_fields and all(isinstance(field, str) for field in table_fields):
                yield table_name, table_fields
                table_count += 1
                table_name = None
                table_fields = []

        print(f"Total tables processed: {table_count}")

    except IOError:
        raise IOError("Error reading the SQL file.")



def convert_to_csv(table_name, table_fields):  # Converts a table's fields into a CSV file.
    csv_filename = table_name + '.csv'
    try:
        with open(csv_filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(table_fields[0].split(','))  # Write attributes as the first row

            for values in table_fields[1:]:
                writer.writerow(values.split(','))  # Write values as subsequent rows
    except IOError:
        raise IOError("Error writing to the CSV file.")


def main(file_path):  # Orchestrates the overall execution of the program, calling the above
    # functions to read SQL file, convert tables to CSV, and handle exceptions.
    try:
        for table_name, table_fields in read_sql_file(file_path):
            try:
                convert_to_csv(table_name, table_fields)
            except Exception as e:
                raise RuntimeError(f"Error converting table {table_name} to CSV:", str(e))
        print("Conversion to CSV completed successfully.")
    except IOError as e:
        raise IOError("An error occurred while reading the SQL file:", str(e))
    except RuntimeError as e:
        raise RuntimeError("An error occurred during the conversion:", str(e))
    finally:
        print("Program execution complete.")


if __name__ == '__main__':
    file_path = 'demo.sql'  # Replace with the actual file path
    try:
        main(file_path)
    except (IOError, RuntimeError) as e:
        print(e)
