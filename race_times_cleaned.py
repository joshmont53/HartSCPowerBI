import csv
import os
from datetime import datetime

# Define file paths - update these to match your folder structure
input_folder = "/Users/joshmontgomery/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Swimming/Hart PowerBI Report/Python Scripts/Swim Manager Downloads"  # Change this to your input folder path
output_folder = "/Users/joshmontgomery/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Swimming/Hart PowerBI Report/Python Scripts/Clean Data"  # Change this to your desired output folder path

file_path = os.path.join(input_folder, 'swim_manager_times.csv')

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Generate filename with current date
current_date = datetime.now().strftime('%Y-%m-%d')
output_filename = f'race_times_cleaned_{current_date}.csv'
output_path = os.path.join(output_folder, output_filename)

# Read data
try:
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        data = list(reader)
except FileNotFoundError:
    print(f"Error: Could not find {file_path}")
    print("Please update the 'input_folder' variable to point to the correct folder containing your CSV files.")
    exit(1)


def converted_time(time):
    if ':' not in time:
        return '00:00:' + time
    else:
        if time[1] == ':':
            return '00:0' + time
        else:
            return '00:' + time


for line in data[1:]:
    line[7] = converted_time(line[7])
    line[9] = converted_time(line[9])
    line[10] = converted_time(line[10])

for line in data:
    print(line)

# Write to output file with date in filename
try:
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"Successfully created: {output_path}")
except Exception as e:
    print(f"Error writing to file: {e}")
