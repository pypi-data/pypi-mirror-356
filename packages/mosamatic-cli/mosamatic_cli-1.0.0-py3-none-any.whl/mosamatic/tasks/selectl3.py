import click


@click.command()
@click.option('--input-dir', required=True, type=click.Path(exists=True), help='Input directory')
@click.option('--output-dir', required=True, type=click.Path(), help='Output directory')
@click.option('--name', help='Name')
def selectl3(input_dir, output_dir, name):
    click.echo(f'Running selectl3 with input_dir={input_dir}, output_dir={output_dir}, name={name}')