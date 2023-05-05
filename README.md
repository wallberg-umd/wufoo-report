# wufoo-report

Extract report of Wufoo forms and users, using the [Wufoo API V3](https://wufoo.github.io/docs)

## Python Environment

Set up a Python environment.

```bash
# Setup the Python version
pyenv install --skip-existing $(cat .python-version)

# Setup the virtual environment
python -m venv .venv --prompt wufoo-py$(cat .python-version)
source .venv/bin/activate

# Install the requirements
pip install -r requirements.txt
```

## Running the report

```bash

# Set base_url and api_key
cp .env-template .env
# Edit .env

# Run the report (creates users.csv and forms.csv)
python3 ./report.py
```

## License

See the [LICENSE](LICENSE.txt) file for license rights and limitations.
