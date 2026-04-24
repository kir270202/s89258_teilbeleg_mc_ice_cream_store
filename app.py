"""
Monte Carlo simulation of a small ice cream shop.

The web application uses Flask for a simple browser GUI. The simulation itself
uses only basic Python functions, loops, dictionaries, and random numbers.
"""

import csv
import os
import random
import statistics
from datetime import datetime

from flask import Flask, render_template, request, send_from_directory


app = Flask(__name__)


# Temperature ranges per month: month -> (minimum, maximum)
MONTHLY_TEMPERATURES = {
    1: (0, 8),
    2: (1, 10),
    3: (5, 15),
    4: (9, 20),
    5: (13, 24),
    6: (17, 30),
    7: (19, 34),
    8: (18, 32),
    9: (14, 25),
    10: (8, 18),
    11: (3, 12),
    12: (0, 8),
}

# Number of days per month in a normal year.
DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Flavor weights. The numbers represent the assumed popularity.
FLAVOR_WEIGHTS = {
    "Vanille": 22,
    "Schokolade": 20,
    "Erdbeere": 18,
    "Zitrone": 14,
    "Stracciatella": 14,
    "Pistazie": 12,
}

DEFAULT_PARAMS = {
    "runs": 1000,
    "price_per_scoop": 1.50,
    "cost_per_scoop": 0.45,
    "fixed_cost_per_day": 80.0,
    "seed": "",
}

EXPORT_FOLDER = "simulation_exports"


def get_month_from_day(day):
    """Return the month for a day of the year from 1 to 365."""
    days_counted = 0
    for month, days_in_month in enumerate(DAYS_PER_MONTH, start=1):
        days_counted += days_in_month
        if day <= days_counted:
            return month
    return 12


def random_temperature(month):
    """Generate a random temperature for the given month."""
    min_temp, max_temp = MONTHLY_TEMPERATURES[month]
    return random.uniform(min_temp, max_temp)


def simulate_customer_count(temperature):
    """Simulate the customer count for one day depending on temperature."""
    base_customers = 60

    if temperature < 10:
        factor = 0.4
    elif temperature < 20:
        factor = 0.8
    elif temperature < 30:
        factor = 1.3
    else:
        factor = 1.6

    fluctuation = random.uniform(0.8, 1.2)
    customers = int(base_customers * factor * fluctuation)
    return max(customers, 0)


def simulate_portion_size(temperature):
    """Randomly choose 1, 2, or 3 scoops for one customer."""
    random_value = random.random()

    if temperature < 15:
        if random_value < 0.75:
            return 1
        if random_value < 0.95:
            return 2
        return 3

    if temperature < 30:
        if random_value < 0.45:
            return 1
        if random_value < 0.85:
            return 2
        return 3

    if random_value < 0.25:
        return 1
    if random_value < 0.75:
        return 2
    return 3


def choose_flavor():
    """Choose one flavor using a weighted random choice."""
    flavors = list(FLAVOR_WEIGHTS.keys())
    weights = list(FLAVOR_WEIGHTS.values())
    return random.choices(flavors, weights=weights, k=1)[0]


def simulate_year(params):
    """Simulate one complete year and return the yearly results."""
    yearly_revenue = 0
    yearly_profit = 0
    yearly_customers = 0
    yearly_scoops = 0
    flavor_counts = {flavor: 0 for flavor in FLAVOR_WEIGHTS}

    for day in range(1, 366):
        month = get_month_from_day(day)
        temperature = random_temperature(month)
        customers = simulate_customer_count(temperature)

        daily_scoops = 0
        for _ in range(customers):
            portion_size = simulate_portion_size(temperature)
            daily_scoops += portion_size

            for _ in range(portion_size):
                flavor = choose_flavor()
                flavor_counts[flavor] += 1

        daily_revenue = daily_scoops * params["price_per_scoop"]
        variable_costs = daily_scoops * params["cost_per_scoop"]
        daily_profit = daily_revenue - variable_costs - params["fixed_cost_per_day"]

        yearly_revenue += daily_revenue
        yearly_profit += daily_profit
        yearly_customers += customers
        yearly_scoops += daily_scoops

    return {
        "profit": yearly_profit,
        "revenue": yearly_revenue,
        "customers": yearly_customers,
        "scoops": yearly_scoops,
        "flavors": flavor_counts,
    }


def save_run_results_to_csv(run_results, params):
    """Save all individual Monte Carlo runs to an Excel-compatible CSV file."""
    os.makedirs(EXPORT_FOLDER, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(EXPORT_FOLDER, f"simulation_results_{timestamp}.csv")

    columns = [
        "run_number",
        "yearly_profit",
        "yearly_revenue",
        "yearly_customers",
        "yearly_scoops",
        "Vanille",
        "Schokolade",
        "Erdbeere",
        "Zitrone",
        "Stracciatella",
        "Pistazie",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow([f"# runs={params['runs']}"])
        writer.writerow([f"# price_per_scoop={params['price_per_scoop']}"])
        writer.writerow([f"# cost_per_scoop={params['cost_per_scoop']}"])
        writer.writerow([f"# fixed_cost_per_day={params['fixed_cost_per_day']}"])
        writer.writerow([f"# seed={params['seed']}"])
        writer.writerow(columns)

        for row in run_results:
            writer.writerow([row[column] for column in columns])

    return filename


def run_monte_carlo(params):
    """Run many yearly simulations and calculate average result values."""
    if params["seed"] != "":
        random.seed(params["seed"])
    else:
        random.seed()

    profits = []
    revenues = []
    customers = []
    scoops = []
    total_flavors = {flavor: 0 for flavor in FLAVOR_WEIGHTS}
    all_run_results = []

    for run_number in range(1, params["runs"] + 1):
        result = simulate_year(params)
        profits.append(result["profit"])
        revenues.append(result["revenue"])
        customers.append(result["customers"])
        scoops.append(result["scoops"])
        all_run_results.append({
            "run_number": run_number,
            "yearly_profit": result["profit"],
            "yearly_revenue": result["revenue"],
            "yearly_customers": result["customers"],
            "yearly_scoops": result["scoops"],
            "Vanille": result["flavors"]["Vanille"],
            "Schokolade": result["flavors"]["Schokolade"],
            "Erdbeere": result["flavors"]["Erdbeere"],
            "Zitrone": result["flavors"]["Zitrone"],
            "Stracciatella": result["flavors"]["Stracciatella"],
            "Pistazie": result["flavors"]["Pistazie"],
        })

        for flavor, count in result["flavors"].items():
            total_flavors[flavor] += count

    average_flavors = {}
    for flavor, count in total_flavors.items():
        average_flavors[flavor] = count / params["runs"]

    most_popular_flavor = max(total_flavors, key=total_flavors.get)
    csv_file = save_run_results_to_csv(all_run_results, params)

    return {
        "average_profit": statistics.mean(profits),
        "average_revenue": statistics.mean(revenues),
        "average_customers": statistics.mean(customers),
        "average_scoops": statistics.mean(scoops),
        "most_popular_flavor": most_popular_flavor,
        "min_profit": min(profits),
        "max_profit": max(profits),
        "average_flavors": average_flavors,
        "csv_filename": os.path.basename(csv_file),
    }


def format_money(value):
    """Format a number as a German-style Euro value."""
    return f"{value:,.2f} EUR".replace(",", "X").replace(".", ",").replace("X", ".")


def create_interpretation(result):
    """Create a short interpretation text for the result page."""
    if result["average_profit"] >= 0:
        profit_text = "Der durchschnittliche Jahresgewinn ist positiv."
    else:
        profit_text = "Der durchschnittliche Jahresgewinn ist negativ."

    return (
        f"{profit_text} Die warmen Monate sind im Modell besonders wichtig, "
        "weil dann mehr Kunden kommen und groessere Portionen gekauft werden. "
        f"Die beliebteste Eissorte ist {result['most_popular_flavor']}. "
        "Die Zielfunktion lautet: maximaler durchschnittlicher Jahresgewinn."
    )


def parse_form_values(form):
    """Read and validate form values from the web page."""
    params = DEFAULT_PARAMS.copy()

    try:
        params["runs"] = int(form.get("runs", DEFAULT_PARAMS["runs"]))
        params["price_per_scoop"] = float(str(form.get("price_per_scoop", DEFAULT_PARAMS["price_per_scoop"])).replace(",", "."))
        params["cost_per_scoop"] = float(str(form.get("cost_per_scoop", DEFAULT_PARAMS["cost_per_scoop"])).replace(",", "."))
        params["fixed_cost_per_day"] = float(str(form.get("fixed_cost_per_day", DEFAULT_PARAMS["fixed_cost_per_day"])).replace(",", "."))
        params["seed"] = form.get("seed", "").strip()
    except ValueError:
        return None, "Bitte nur gueltige Zahlen eingeben."

    if params["runs"] <= 0:
        return None, "Die Anzahl der Monte-Carlo-Laeufe muss groesser als 0 sein."
    if params["runs"] > 20000:
        return None, "Bitte hoechstens 20000 Monte-Carlo-Laeufe eingeben."
    if params["price_per_scoop"] < 0 or params["cost_per_scoop"] < 0 or params["fixed_cost_per_day"] < 0:
        return None, "Preise und Kosten duerfen nicht negativ sein."

    return params, ""


@app.route("/", methods=["GET", "POST"])
def index():
    """Show the form and, after submit, the simulation results."""
    params = DEFAULT_PARAMS.copy()
    result = None
    error = ""
    interpretation = ""
    flavor_rows = []

    if request.method == "POST":
        params, error = parse_form_values(request.form)
        if error == "":
            result = run_monte_carlo(params)
            interpretation = create_interpretation(result)

            max_flavor_value = max(result["average_flavors"].values())
            sorted_flavors = sorted(result["average_flavors"].items(), key=lambda item: item[1], reverse=True)
            for flavor, average_count in sorted_flavors:
                bar_width = 0
                if max_flavor_value > 0:
                    bar_width = average_count / max_flavor_value * 100
                flavor_rows.append({
                    "name": flavor,
                    "average_count": average_count,
                    "bar_width": bar_width,
                })
        else:
            params = DEFAULT_PARAMS.copy()

    return render_template(
        "index.html",
        params=params,
        result=result,
        error=error,
        interpretation=interpretation,
        flavor_rows=flavor_rows,
        format_money=format_money,
    )


@app.route("/download/<filename>")
def download_file(filename):
    """Download a generated CSV export file."""
    return send_from_directory(EXPORT_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
