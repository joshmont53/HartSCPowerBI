import pandas as pd
import requests

# URL
url = "https://www.swimmingresults.org/12months/last12.php?Pool=S&Stroke=1&Sex=M&AgeGroup=10&date=31%2F12%2F2025&StartNumber=1&RecordsToView=100&TargetNationality=P&TargetRegion=P&Level=C&TargetCounty=HNTS&TargetClub=XXXX"

# Fake a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Get page content
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    tables = pd.read_html(response.text)  # Use the HTML content
    df = tables[0]  # Store the first table in a variable
    print(df)  # Display the table

    # Export to CSV
    df.to_csv("swimming_rankings.csv", index=False)
    print("Data successfully saved to swimming_rankings.csv")
else:
    print(f"Failed to fetch data: {response.status_code}")





