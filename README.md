## Docker run
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

## Local run

Install the requirements:

```bash
pip install -r requirements.txt
```

Start the Flask app:

```bash
python3 app.py
```

Then open:

```text
http://localhost:5000
```
