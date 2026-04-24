# Installation and Start

## Local Installation

First create a virtual environment:

```bash
python3 -m venv .venv
```

Then activate the environment:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the application with:

```bash
python app.py
```

Then open this address in the browser:

```text
http://localhost:5000
```

## Installation with Docker

Docker is used for reproducible execution. This allows the professor to start the same environment without setting up Python packages manually on the local machine.

Build the image:

```bash
docker build -t eis-monte-carlo .
```

Start the container:

```bash
docker run --rm -p 5000:5000 eis-monte-carlo
```

Then open this address in the browser:

```text
http://localhost:5000
```

## Notes

The GUI is web-based and runs in the browser. Therefore, `tkinter` is not required.

Flask is the only external Python dependency. Libraries such as `pandas`, `numpy`, or `matplotlib` are not used.

No extra dependency is required for the CSV export. The export uses the Python standard library and writes CSV files into `simulation_exports/`.
