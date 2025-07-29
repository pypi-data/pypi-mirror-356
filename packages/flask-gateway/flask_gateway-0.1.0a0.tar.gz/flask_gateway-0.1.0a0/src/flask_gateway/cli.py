import click
from .gateway_server import start_gateway

@click.group()
def cli():
    pass

@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to run on')
@click.option('--port', default=9999, help='Port to run on')
@click.option('--targets', default=None, help='Path to targets.json')
def serve(host, port, targets):
    start_gateway(host=host, port=port, targets_path=targets)
