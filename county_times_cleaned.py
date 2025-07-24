import csv
import os
from datetime import datetime

# Define file paths - update these to match your folder structure
input_folder = "/Users/joshmontgomery/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Swimming/Hart PowerBI Report/County Times 24:25"  # Change this to your input folder path
output_folder = "/Users/joshmontgomery/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Swimming/Hart PowerBI Report/Python Scripts/Clean Data"  # Change this to your desired output folder path

male_file_path = os.path.join(input_folder, 'Male County Times.csv')
female_file_path = os.path.join(input_folder, 'Female County Times.csv')

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Generate filename with current date
current_date = datetime.now().strftime('%Y-%m-%d')
output_filename = f'county_times_cleaned_{current_date}.csv'
output_path = os.path.join(output_folder, output_filename)

# Read male data
try:
    with open(male_file_path, mode='r') as file:
        reader = csv.reader(file)
        data = list(reader)
except FileNotFoundError:
    print(f"Error: Could not find {male_file_path}")
    print("Please update the 'input_folder' variable to point to the correct folder containing your CSV files.")
    exit(1)

male_list = []  # Create an empty list

for row in data[3:]:
    stroke = row[0]  # The stroke name (e.g., 'Backstroke')
    for i, time in enumerate(row[1:]):  # Loop through times with their index
        category = data[0][i + 1]  # Get the corresponding word from data[0]
        value1 = data[1][i + 1]  # Get corresponding value from line 1
        value2 = data[2][i + 1]  # Get corresponding value from line 2
        male_list.append([stroke, time, category, value1, value2])  # Append all

for line in male_list:
    line.append('Male')

header = ['Event','Time','Age Category','Course','Time Type','Gender']
male_list.insert(0, header)

# Read female data
try:
    with open(female_file_path, mode='r') as file:
        reader = csv.reader(file)
        data = list(reader)
except FileNotFoundError:
    print(f"Error: Could not find {female_file_path}")
    print("Please update the 'input_folder' variable to point to the correct folder containing your CSV files.")
    exit(1)

female_list = []  # Create an empty list

for row in data[3:]:
    stroke = row[0]  # The stroke name (e.g., 'Backstroke')
    for i, time in enumerate(row[1:]):  # Loop through times with their index
        category = data[0][i + 1]  # Get the corresponding word from data[0]
        value1 = data[1][i + 1]  # Get corresponding value from line 1
        value2 = data[2][i + 1]  # Get corresponding value from line 2
        female_list.append([stroke, time, category, value1, value2])  # Append all

for line in female_list:
    line.append('Female')

combined_list = male_list + female_list

def converted_time(time):
    if time == '':
        return ''
    else:
        if ':' not in time:
            return '00:00:' + time
        else:
            if time[1] == ':':
                return '00:0' + time
            else:
                return '00:' + time

for line in combined_list[1:]:
    line[1] = converted_time(line[1])

# Write to output file with date in filename
try:
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(combined_list)
    print(f"Successfully created: {output_path}")
except Exception as e:
    print(f"Error writing to file: {e}")

with open('county_times_cleaned.csv', mode = 'w') as file:
    writer = csv.writer(file)
    writer.writerows(combined_list)
