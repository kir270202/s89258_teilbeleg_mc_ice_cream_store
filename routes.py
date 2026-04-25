"""Flask routes and UI-specific helpers for the ice cream simulation app."""

from flask import Blueprint, render_template, request, send_from_directory

from simulation import DEFAULT_PARAMS, EXPORT_FOLDER, run_monte_carlo


ui = Blueprint("ui", __name__)


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


@ui.route("/", methods=["GET", "POST"])
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


@ui.route("/download/<filename>")
def download_file(filename):
    """Download a generated CSV export file."""
    return send_from_directory(EXPORT_FOLDER, filename, as_attachment=True)
