import click

from mosamatic.tasks import DecompressDicomFilesTask


@click.command(help='Decompress DICOM files')
@click.option(
    '--input', 
    required=True, 
    type=click.Path(exists=True), 
    help='Input directory'
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
    task = DecompressDicomFilesTask(input, output, overwrite=overwrite)
    task.run()