import csv

with open('race_times.csv', mode='r') as file:
    reader = csv.reader(file)
    data = list(reader)

#for line in data:
    #print(line)

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

with open('race_times_cleaned.csv', mode = 'w') as file:
    writer = csv.writer(file)
    writer.writerows(data)
