import requests
import pandas as pd
from bs4 import BeautifulSoup

genders = ['M', 'F']
ages = ['09', 10, 11, 12, 13, 14, 15, 16, 17]

events = [
    ("50m Freestyle", 1), ("100m Freestyle", 2), ("200m Freestyle", 3),
    ("400m Freestyle", 4), ("800m Freestyle", 5), ("1500m Freestyle", 6),
    ("50m Backstroke", 13), ("100m Backstroke", 14), ("200m Backstroke", 15),
    ("50m Breaststroke", 7), ("100m Breaststroke", 8), ("200m Breaststroke", 9),
    ("50m Butterfly", 10), ("100m Butterfly", 11), ("200m Butterfly", 12),
    ("100m Individual Medley", 18), ("200m Individual Medley", 16), ("400m Individual Medley", 17)
]


# Function to convert time format
def converted_time(time):
    if ':' not in time:
        return '00:00:' + time
    else:
        if time[1] == ':':
            return '00:0' + time
        else:
            return '00:' + time


# Create a list of all events with gender and age
full_event_list = [(gender, age, event_name, event_id) for gender in genders for age in ages for event_name, event_id in
                   events]

# Generate URLs
urls = [(gender, age, event_name, event_id,
         f"https://www.swimmingresults.org/12months/last12.php?Pool=S&Stroke={event_id}&Sex={gender}&AgeGroup={age}&date=31%2F12%2F2025&StartNumber=1&RecordsToView=100&TargetNationality=P&TargetRegion=P&Level=C&TargetCounty=HNTS&TargetClub=XXXX")
        for gender, age, event_name, event_id in full_event_list]

all_data = []

for gender, age, event_name, event_id, web_link in urls:
    response = requests.get(web_link)

    if response.status_code != 200:
        print(f"Failed to retrieve data for {event_name} ({gender}, {age}) - Skipping")
        continue  # Skip this entry if the request fails

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the table
    table = soup.find("table")

    if table is None:
        print(f"No table found for {event_name} ({gender}, {age}) - Skipping")
        continue  # Skip if no table is found

    # Extract table rows (skip headers)
    row_count = 0
    for row in table.find_all("tr")[1:]:  # Skip the header row
        cells = [td.text.strip() for td in row.find_all("td")]
        if cells:
            cells.extend([gender, age, event_name])  # Append gender, age, event
            all_data.append(cells)
            row_count += 1

    # Print success message with row count
    print(f"Successfully processed {event_name} ({gender}, {age}) - {row_count} records added")

# Define column names
column_names = ["Ranking", "Name", "Club", "YOB", "Meet", "Venue", "Level", "Date", "Time", "FINA", "Gender", "Age",
                "Event"]

# Create a final DataFrame with headers
df_final = pd.DataFrame(all_data, columns=column_names)

# Apply the time formatting function to the "Time" column
df_final["Time"] = df_final["Time"].apply(converted_time)

# Export DataFrame to Excel
csv_filename = "/Users/joshmontgomery/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Swimming/Hart PowerBI Report/Python Scripts/Clean Data/county_rankings.csv"
df_final.to_csv(csv_filename, index=False)

print(f"Data successfully saved to {csv_filename}")

