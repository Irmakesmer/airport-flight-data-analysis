"""
****************************************************************************
Additional info
 1. I declare that my work contains no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: w20449452
 4. Date: 24/11/2025
****************************************************************************
"""

from graphics import *
import csv
import math

# global data list
data_list = []

def load_csv(CSV_chosen):
    """
    Loads a CSV file into the global list data_list.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    """
    global data_list
    data_list.clear()
    with open(CSV_chosen, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data_list.append(row)


# Valid airports
VALID_AIRPORTS = {
    "LHR": "London Heathrow",
    "MAD": "Madrid Adolfo Suárez-Barajas",
    "CDG": "Charles De Gaulle International",
    "IST": "Istanbul Airport International",
    "AMS": "Amsterdam Schiphol",
    "LIS": "Lisbon Portela",
    "FRA": "Frankfurt Main",
    "FCO": "Rome Fiumicino",
    "MUC": "Munich International",
    "BCN": "Barcelona International"
}

# Valid airlines
VALID_AIRLINES = {
    "BA": "British Airways",
    "AF": "Air France",
    "AY": "Finnair",
    "KL": "KLM",
    "SK": "Scandinavian Airlines",
    "TP": "TAP Air Portugal",
    "TK": "Turkish Airlines",
    "W6": "Wizz Air",
    "U2": "easyJet",
    "FR": "Ryanair",
    "A3": "Aegean Airlines",
    "SN": "Brussels Airlines",
    "EK": "Emirates",
    "QR": "Qatar Airways",
    "IB": "Iberia",
    "LH": "Lufthansa"
}



# =========================
# TASK A – VALIDATION
# =========================
def get_airport_and_year():
    """Prompt user for airport code and year, validate both."""
    while True:
        code = input("Please enter a three-letter city code: ").strip().upper()
        if len(code) != 3:
            print("Wrong code length – please enter a three-letter city code.")
            continue
        if code not in VALID_AIRPORTS:
            print("Unavailable city code – please enter a valid city code.")
            continue
        break

    while True:
        year_input = input("Please enter the year required in the format YYYY: ").strip()
        if not year_input.isdigit() or len(year_input) != 4:
            print("Wrong data type – please enter a four-digit year value.")
            continue
        year = int(year_input)
        if year < 2000 or year > 2025:
            print("Out of range – please enter a value from 2000 to 2025.")
            continue
        break

    filename = f"{code}{year}.csv"

    print("****************************************************************************")
    print(f"{filename} selected - Planes departing {VALID_AIRPORTS[code]} {year}")
    print("****************************************************************************")

    return filename, code, year



# =========================
# TASK B – OUTCOMES
# =========================
def process_outcomes(airport_code):
    """Analyse loaded data and return dictionary of outcomes."""
    total_flights = len(data_list)
    terminal_2 = sum(1 for row in data_list if row[8] == '2')
    under_600 = sum(1 for row in data_list if int(row[5]) < 600)
    air_france = sum(1 for row in data_list if row[1].startswith("AF"))

    # Flights departing in temperatures below 15°C
    temp_below_15 = 0
    for row in data_list:
        weather = row[10]
        if '°C' in weather:
            try:
                temp = int(weather.split('°C')[0])
                if temp < 15:
                    temp_below_15 += 1
            except:
                pass

    # British Airways stats
    ba_flights = [row for row in data_list if row[1].startswith("BA")]
    avg_ba_per_hour = round(len(ba_flights) / 12, 2)
    perc_ba_total = round((len(ba_flights) / total_flights) * 100, 2) if total_flights else 0

    # Air France delay percentage
    af_flights = [row for row in data_list if row[1].startswith("AF")]
    delayed_af = sum(1 for row in af_flights if row[3] != row[2])
    perc_af_delayed = round((delayed_af / len(af_flights)) * 100, 2) if af_flights else 0

    # Rain hours
    rain_hours = len({row[10] for row in data_list if 'rain' in row[10].lower()})

    # Least common destination(s)
    dest_counts = {}
    for row in data_list:
        dest = row[4]
        dest_counts[dest] = dest_counts.get(dest, 0) + 1

    min_count = min(dest_counts.values())
    least_common = [VALID_AIRPORTS.get(code, code) for code, count in dest_counts.items() if count == min_count]

    return {
        "total_flights": total_flights,
        "terminal_2": terminal_2,
        "under_600": under_600,
        "air_france": air_france,
        "temp_below_15": temp_below_15,
        "avg_ba_per_hour": avg_ba_per_hour,
        "perc_ba_total": perc_ba_total,
        "perc_af_delayed": perc_af_delayed,
        "rain_hours": rain_hours,
        "least_common": least_common
    }


def display_outcomes(filename, airport_code, year, results):
    print("\n*********************************************************************************")
    print(f"File {filename} selected - Planes departing {VALID_AIRPORTS[airport_code]} {year}")
    print("*********************************************************************************")
    print(f"The total number of flights from this airport was {results['total_flights']}")
    print(f"The total number of flights departing Terminal Two was {results['terminal_2']}")
    print(f"The total number of departures on flights under 600 miles was {results['under_600']}")
    print(f"There were {results['air_france']} Air France flights from this airport}")
    print(f"There were {results['temp_below_15']} flights departing in temperatures below 15 degrees")
    print(f"There was an average of {results['avg_ba_per_hour']} British Airways flights per hour")
    print(f"British Airways planes made up {results['perc_ba_total']}% of all departures")
    print(f"{results['perc_af_delayed']}% of Air France departures were delayed")
    print(f"There were {results['rain_hours']} hours in which rain fell")
    print(f"The least common destinations are {results['least_common']}")
    print("*********************************************************************************\n")



# =========================
# TASK C – SAVE RESULTS
# =========================
def save_results(filename, airport_code, year, results):
    with open("results.txt", "a") as f:
        f.write(f"File {filename} - {VALID_AIRPORTS[airport_code]} {year}\n")
        for key, val in results.items():
            f.write(f"{key}: {val}\n")
        f.write("-----------------------------------------------------------\n")



# =========================
# TASK D – HISTOGRAM
# =========================
def get_airline_code():
    """Prompt for and validate airline code."""
    while True:
        code = input("Enter a two-character Airline code to plot a histogram: ").strip().upper()
        if code not in VALID_AIRLINES:
            print("Unavailable Airline code please try again.")
            continue
        return code


def draw_histogram(airline_code, airport_code, year):
    airline_name = VALID_AIRLINES[airline_code]
    airport_name = VALID_AIRPORTS[airport_code]

    hours = [f"{h:02d}" for h in range(12)]
    hour_counts = {h: 0 for h in hours}

    # Count flights per hour
    for row in data_list:
        if row[1].startswith(airline_code):
            hour = row[2].split(":")[0]
            if hour in hour_counts:
                hour_counts[hour] += 1

    max_val = max(hour_counts.values()) if hour_counts else 1

    win = GraphWin(f"{airline_name} Departures - {airport_name} {year}", 800, 500)
    win.setBackground("white")

    # Axes
    Line(Point(80, 400), Point(700, 400)).draw(win)
    Line(Point(80, 400), Point(80, 100)).draw(win)

    Text(Point(400, 40), f"{airline_name} Departures from {airport_name} {year}").draw(win)
    Text(Point(400, 480), "Hour of Departure").draw(win)
    Text(Point(40, 250), "Flights").draw(win)

    bar_width = 40
    gap = 20

    for i, h in enumerate(hours):
        count = hour_counts[h]
        bar_height = (count / max_val) * 250

        x1 = 100 + i * (bar_width + gap)
        y1 = 400 - bar_height

        rect = Rectangle(Point(x1, y1), Point(x1 + bar_width, 400))
        rect.setFill("skyblue")
        rect.draw(win)

        Text(Point(x1 + bar_width / 2, 410), h).draw(win)
        Text(Point(x1 + bar_width / 2, y1 - 10), str(count)).draw(win)

    Text(Point(400, 460), "Click anywhere to close").draw(win)
    win.getMouse()
    win.close()


# =========================
# TASK E – LOOP
# =========================
def main():
    while True:
        filename, airport_code, year = get_airport_and_year()
        load_csv(filename)
        results = process_outcomes(airport_code)
        display_outcomes(filename, airport_code, year, results)
        save_results(filename, airport_code, year, results)

        airline_code = get_airline_code()
        draw_histogram(airline_code, airport_code, year)

        again = input("Do you want to select a new data file? Y/N: ").strip().upper()
        if again != "Y":
            print("Thank you. End of run.")
            break


if __name__ == "__main__":
    main()



  






