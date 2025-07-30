import click
from .connector import StarburstConnector
from .scheduler import QueryScheduler

@click.group()
def cli():
    """Starburst Scheduler CLI for running and scheduling queries."""
    pass

@cli.command()
@click.option("--host", required=True, help="Starburst cluster host (e.g., cluster.trino.galaxy.starburst.io)")
@click.option("--port", type=int, default=443, help="Starburst cluster port (default: 443)")
@click.option("--user", required=True, help="Starburst username (e.g., user@domain.com/deny_pii)")
@click.option("--password", required=True, envvar="STARBURST_PASSWORD", help="Starburst password (or set STARBURST_PASSWORD env var)")
@click.option("--catalog", default="system", help="Catalog name (default: system)")
@click.option("--schema", default="runtime", help="Schema name (default: runtime)")
@click.option("--query", required=True, help="SQL query to execute")
def run_query(host, port, user, password, catalog, schema, query):
    """Run a single SQL query on a Starburst cluster."""
    connector = StarburstConnector(host, port, user, password, catalog, schema)
    if connector.connect():
        result = connector.execute_query(query)
        if result:
            click.echo(f"Query result: {result}")
        else:
            click.echo("Query failed. Check logs for details.", err=True)
    else:
        click.echo("Connection failed. Verify host, port, credentials, and cluster status.", err=True)

@cli.command()
@click.option("--host", required=True, help="Starburst cluster host")
@click.option("--port", type=int, default=443, help="Starburst cluster port (default: 443)")
@click.option("--user", required=True, help="Starburst username")
@click.option("--password", required=True, envvar="STARBURST_PASSWORD", help="Starburst password (or set STARBURST_PASSWORD env var)")
@click.option("--catalog", default="system", help="Catalog name (default: system)")
@click.option("--schema", default="runtime", help="Schema name (default: runtime)")
@click.option("--query", required=True, help="SQL query to schedule")
@click.option("--frequency", required=True, type=int, help="Frequency of execution (e.g., 60 for every 60 seconds)")
@click.option("--time-unit", default="seconds", type=click.Choice(["seconds", "minutes", "hours", "days"]), help="Time unit for frequency")
def schedule_query(host, port, user, password, catalog, schema, query, frequency, time_unit):
    """Schedule a SQL query to run at regular intervals."""
    connector = StarburstConnector(host, port, user, password, catalog, schema)
    if connector.connect():
        scheduler = QueryScheduler(connector)
        scheduler.schedule_query(query, frequency, time_unit)
        scheduler.run()
    else:
        click.echo("Connection failed. Verify host, port, credentials, and cluster status.", err=True)

if __name__ == "__main__":
    cli()