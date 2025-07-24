import csv

with open('Male County Times.csv', mode='r') as file:
    reader = csv.reader(file)
    data = list(reader)

'''for line in data:
    print(line)

times = []

for row in data[3:]:
    times.extend(row[1:])

for row in data[3:]:
    times.append(row[0])


for line in times:
    print(line)

new_list = []  # Create an empty list

for row in data[3:]:
    word = row[0]  # Extract the word (e.g., 'Backstroke')
    for time in row[1:]:  # Loop through each time in the row
        new_list.append([word, time])  # Add [word, time] to new_list

for line in new_list:
    print(line)

new_list = []  # Create an empty list

for row in data[3:]:
    stroke = row[0]  # The stroke name (e.g., 'Backstroke')
    for i, time in enumerate(row[1:]):  # Loop through times with their index
        category = data[0][i + 1]  # Get the corresponding word from data[0]
        new_list.append([stroke, time, category])  # Append with category

for line in new_list:
    print(line)'''


male_list = []  # Create an empty list

for row in data[3:]:
    stroke = row[0]  # The stroke name (e.g., 'Backstroke')
    for i, time in enumerate(row[1:]):  # Loop through times with their index
        category = data[0][i + 1]  # Get the corresponding word from data[0]
        value1 = data[1][i + 1]  # Get corresponding value from line 1
        value2 = data[2][i + 1]  # Get corresponding value from line 2
        male_list.append([stroke, time, category, value1, value2])  # Append all

#for line in new_list:
   # print(line)

for line in male_list:
    line.append('Male')

#for line in new_list:
  #  print(line)

header = ['Event','Time','Age Category','Course','Time Type','Gender']

male_list.insert(0,header)

#for line in male_list:
  #  print(line)

import csv

with open('Female County Times.csv', mode='r') as file:
    reader = csv.reader(file)
    data = list(reader)

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

for line in combined_list:
    print(line)

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


with open('county_times_cleaned.csv', mode = 'w') as file:
    writer = csv.writer(file)
    writer.writerows(combined_list)