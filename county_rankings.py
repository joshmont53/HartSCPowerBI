import requests
import pandas as pd
from bs4 import BeautifulSoup
from decimal import Decimal, ROUND_HALF_EVEN

# ----------------------------------
# CONFIG
# ----------------------------------
genders = ['M', 'F']
ages = ['09', 10, 11, 12, 13, 14, 15, 16, 17]
pools = ['S', 'L']  # Short & Long course

events = [
    ("50m Freestyle", 1), ("100m Freestyle", 2), ("200m Freestyle", 3),
    ("400m Freestyle", 4), ("800m Freestyle", 5), ("1500m Freestyle", 6),
    ("50m Backstroke", 13), ("100m Backstroke", 14), ("200m Backstroke", 15),
    ("50m Breaststroke", 7), ("100m Breaststroke", 8), ("200m Breaststroke", 9),
    ("50m Butterfly", 10), ("100m Butterfly", 11), ("200m Butterfly", 12),
    ("100m Individual Medley", 18), ("200m Individual Medley", 16), ("400m Individual Medley", 17)
]

# Map full event names to ASA/BS codes used by the macro tables
event_code_map = {
    "50m Freestyle": "50FR", "100m Freestyle": "100FR", "200m Freestyle": "200FR",
    "400m Freestyle": "400FR", "800m Freestyle": "800FR", "1500m Freestyle": "1500FR",
    "50m Backstroke": "50BA", "100m Backstroke": "100BA", "200m Backstroke": "200BA",
    "50m Breaststroke": "50BR", "100m Breaststroke": "100BR", "200m Breaststroke": "200BR",
    "50m Butterfly": "50FL", "100m Butterfly": "100FL", "200m Butterfly": "200FL",
    "200m Individual Medley": "200IM", "400m Individual Medley": "400IM",
    # 100 IM is SC-only for conversion; we still keep it for formatting
    "100m Individual Medley": "100IM"
}

# TurnFactor list from your VBA macro (mapped to the codes above)
turn_factor_by_code = {
    "50FR": 42.245, "100FR": 42.245, "200FR": 43.786, "400FR": 44.233,
    "800FR": 45.525, "1500FR": 46.221,
    "50BR": 63.616, "100BR": 63.616, "200BR": 66.598,
    "50FL": 38.269, "100FL": 38.269, "200FL": 39.760,
    "50BA": 40.500, "100BA": 40.500, "200BA": 41.980,
    "200IM": 49.700, "400IM": 55.366,
    # 100IM intentionally omitted for LC->SC conversion
}

# ----------------------------------
# HELPERS
# ----------------------------------

def time_to_seconds(t_str: str) -> float:
    """Accepts 'M:SS.ss' or 'SS.ss'. Returns total seconds."""
    s = t_str.strip()
    parts = s.split(":")
    if len(parts) == 1:
        return float(parts[0])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    elif len(parts) == 3:  # hh:mm:ss.xx (unlikely here)
        return int(parts[-2]) * 60 + float(parts[-1])
    else:
        return 0.0

def vba_round_to_tenth(x: float) -> float:
    """VBA/Excel Round(x,1): banker's rounding (HALF_EVEN)."""
    return float(Decimal(x).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN))

def lc_to_sc_macro(lc_time_str: str, event_name: str) -> float | str:
    """
    Convert LC -> SC using the official macro:
    SC = LC - (TurnFactor / LC) * ((distance/100)^2) * 2
    Rounded to 0.1s using VBA HALF_EVEN. Returns seconds (float) if convertible,
    otherwise returns the original string unchanged.
    """
    code = event_code_map.get(event_name)
    tf = turn_factor_by_code.get(code)
    if tf is None:
        return lc_time_str  # no conversion available for this event

    lc_seconds = time_to_seconds(lc_time_str)
    if lc_seconds <= 0:
        return lc_time_str

    try:
        distance = int(event_name.split("m")[0])  # e.g., "400m Freestyle" -> 400
    except Exception:
        return lc_time_str

    num_turn_factor = ((distance / 100.0) ** 2) * 2.0
    sc_unrounded = lc_seconds - (tf / lc_seconds) * num_turn_factor
    sc_seconds = vba_round_to_tenth(sc_unrounded)
    return sc_seconds

def seconds_to_m_ss_2dp(sec: float) -> str:
    """Convert numeric seconds to 'M:SS.ss' (handles rollover correctly)."""
    m = int(sec // 60)
    s = sec - m * 60
    return f"{m}:{s:05.2f}"  # e.g., 61.8 -> '1:01.80'

# Your original display normaliser: ensures '00:MM:SS.ss'
def converted_time(time_str: str) -> str:
    if ':' not in time_str:
        return '00:00:' + time_str
    else:
        if time_str[1] == ':':
            return '00:0' + time_str
        else:
            return '00:' + time_str

# ----------------------------------
# SCRAPE
# ----------------------------------
all_data = []

# Pre-build all URLs (including pool)
urls = [
    (
        gender, age, pool, event_name, event_id,
        f"https://www.swimmingresults.org/12months/last12.php?Pool={pool}"
        f"&Stroke={event_id}&Sex={gender}&AgeGroup={age}&date=31%2F12%2F2025"
        f"&StartNumber=1&RecordsToView=100&TargetNationality=P&TargetRegion=P"
        f"&Level=C&TargetCounty=HNTS&TargetClub=XXXX"
    )
    for gender in genders for age in ages for pool in pools for event_name, event_id in events
]

for gender, age, pool, event_name, event_id, url in urls:
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {event_name} ({gender}, {age}, {pool}) - Skipping")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if table is None:
        print(f"No table found for {event_name} ({gender}, {age}, {pool}) - Skipping")
        continue

    row_count = 0
    for row in table.find_all("tr")[1:]:  # skip header
        cells = [td.text.strip() for td in row.find_all("td")]
        if not cells:
            continue

        # Original scraped time string
        raw_time = cells[8]

        if pool == 'L':
            # Convert LC -> SC using macro, then convert seconds to 'M:SS.ss', then normalise
            sc_val = lc_to_sc_macro(raw_time, event_name)
            if isinstance(sc_val, float):
                time_for_display = converted_time(seconds_to_m_ss_2dp(sc_val))
            else:
                time_for_display = converted_time(raw_time)
        else:
            # SC row: use original time, just normalise
            time_for_display = converted_time(raw_time)

        # Replace Time col with our display value
        cells[8] = time_for_display

        # Append extra columns
        cells.extend([gender, age, event_name, pool])
        all_data.append(cells)
        row_count += 1

    print(f"Successfully processed {event_name} ({gender}, {age}, {pool}) - {row_count} records added")

# ----------------------------------
# OUTPUT
# ----------------------------------
column_names = [
    "Ranking", "Name", "Club", "YOB", "Meet", "Venue", "Level", "Date",
    "Time", "FINA", "Gender", "Age", "Event", "Course"
]
df_final = pd.DataFrame(all_data, columns=column_names)

# Export to CSV
csv_filename = "/Users/joshmontgomery/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Swimming/Hart PowerBI Report/Python Scripts/Clean Data/swim_rankings.csv"
df_final.to_csv(csv_filename, index=False)
print(f"Data successfully saved to {csv_filename}")


print(f"Data successfully saved to {csv_filename}")

