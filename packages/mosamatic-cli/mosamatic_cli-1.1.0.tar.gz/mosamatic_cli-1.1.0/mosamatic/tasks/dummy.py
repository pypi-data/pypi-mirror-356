import click

from mosamatic.tasks.task import Task
from mosamatic.utils import input_dict_from_input, param_dict_from_params


class DummyTask(Task):
    def __init__(self, input, output, params=None, overwrite=False):
        super(DummyTask, self).__init__(input, output, params=params, overwrite=overwrite)

    def run(self):
        value = self.param('param1')
        print(f'DummyTask(input={self.input()}, params={value})')


@click.command(help='Tests handling of multiple inputs')
@click.option('--input', multiple=True, type=click.Path(), required=True, help='Multiple named input files')
@click.option('--output', required=True, type=click.Path(), help='Output directory')
@click.option('--params', multiple=True, required=True, type=str, help='Parameters: param1=value, param2=value')
@click.option('--overwrite', default=False, type=click.BOOL, help='Overwrite (true/false)')
def dummy(input, output, params, overwrite):
    input = input_dict_from_input(input)
    params = param_dict_from_params(params)
    task = DummyTask(input, output, params=params, overwrite=overwrite)
    task.run()