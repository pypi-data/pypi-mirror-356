import click
import json
from jsonpeek.core import parse_json, evaluate_query, JsonQueryError

@click.command()
@click.argument("query")
@click.option("--file", "filename", type=click.File("r"), default="-", help="Input JSON file or stdin by default.")
@click.option("--raw", is_flag=True, help="Output raw value instead of JSON.")
@click.option("--compact", is_flag=True, help="Output compact JSON (no pretty printing).")
def main(query, filename, raw, compact):
    """Query JSON data using Python expressions. Example: 'x["user"]["name"]'"""
    data = parse_json(filename)
    result = evaluate_query(data, query)

    if raw:
        click.echo(result)
    else:
        indent = None if compact else 2
        click.echo(json.dumps(result, indent=indent))

