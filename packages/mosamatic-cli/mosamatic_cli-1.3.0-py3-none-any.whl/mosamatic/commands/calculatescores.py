import click

from mosamatic.tasks import CalculateScoresTask


@click.command(help='Calculates body composition scores')
@click.option(
    '--input', 
    multiple=True,
    required=True, 
    type=click.Path(exists=True), 
    help='Named input directories: images, segmentations',
)
@click.option(
    '--output', 
    required=True, 
    type=click.Path(), 
    help='Output directory'
)
@click.option(
    '--overwrite', 
    type=click.BOOL, 
    default=False, 
    help='Overwrite (true/false)'
)
def decompress(input, output, overwrite):
    task = CalculateScoresTask(input, output, overwrite=overwrite)
    task.run()