import logging

import requests
import typer


app = typer.Typer()


@app.command()
def goodbye(name: str, formal: bool = False):
    while True:
        try:
            response = requests.get("https://ifconfig.me")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            break


if __name__ == "__main__":
    app()