import click

from mosamatic.tasks import DummyTask
from mosamatic.utils import input_dict_from_input, param_dict_from_params


@click.command(help='Tests handling of multiple inputs')
@click.option(
    '--input', 
    multiple=True, 
    type=click.Path(), 
    required=True, 
    help='Multiple named input files'
)
@click.option(
    '--output', 
    required=True, 
    type=click.Path(), 
    help='Output directory'
)
@click.option(
    '--params', 
    multiple=True, 
    required=True, 
    type=str, 
    help='Parameters: param1, param2'
)
@click.option(
    '--overwrite', 
    default=False, 
    type=click.BOOL, 
    help='Overwrite (true/false)'
)
def dummy(input, output, params, overwrite):
    input = input_dict_from_input(input)
    params = param_dict_from_params(params)
    task = DummyTask(input, output, params=params, overwrite=overwrite)
    task.run()