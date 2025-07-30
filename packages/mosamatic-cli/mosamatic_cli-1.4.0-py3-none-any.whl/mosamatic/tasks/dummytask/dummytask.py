from mosamatic.tasks.task import Task


class DummyTask(Task):
    def __init__(self, input, output, params=None, overwrite=False):
        super(DummyTask, self).__init__(input, output, params=params, overwrite=overwrite)

    def run(self):
        value = self.param('param1')
        print(f'DummyTask(input={self.input()}, params={value})')
