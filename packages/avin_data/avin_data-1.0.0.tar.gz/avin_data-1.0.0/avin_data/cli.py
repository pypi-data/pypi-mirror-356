import click


@click.command()
def start_cli():
    """Prints a greeting."""
    click.echo("Hello, World!")
