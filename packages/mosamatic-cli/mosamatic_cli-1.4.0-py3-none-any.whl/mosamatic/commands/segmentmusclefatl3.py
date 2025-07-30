import click

from mosamatic.tasks import SegmentMuscleFatL3Task
from mosamatic.utils import input_dict_from_input, param_dict_from_params


@click.command(help='Extracts muscle and fat regions from CT images at L3')
@click.option(
    '--input', 
    multiple=True, 
    required=True, 
    type=click.Path(exists=True), 
    help='Named input directories: images, model_files'
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
    help='Parameters: model_verion (default: 1.0)'
)
@click.option(
    '--overwrite', 
    default=False, 
    type=click.BOOL, 
    help='Overwrite (true/false)'
)
def segmentmusclefatl3(input, output, params, overwrite):
    input = input_dict_from_input(input)
    params = param_dict_from_params(params)
    task = SegmentMuscleFatL3Task(input, output, params=params, overwrite=overwrite)
    task.run()