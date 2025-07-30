import click

from mosamatic.commands import (
    decompress,
    rescale,
    segmentmusclefatl3,
)


class CustomHelpGroup(click.Group):
    def format_commands(self, ctx, formatter):
        commands = self.list_commands(ctx)
        with formatter.section('Commands'):
            for command_name in commands:
                command = self.get_command(ctx, command_name)
                if command is None or command.hidden:
                    continue
                help_text = command.get_short_help_str()
                formatter.write_text(f'{command_name:15} {help_text}')


@click.group(cls=CustomHelpGroup)
def cli():
    pass


cli.add_command(decompress.decompress)
cli.add_command(rescale.rescale)
cli.add_command(segmentmusclefatl3.segmentmusclefatl3)