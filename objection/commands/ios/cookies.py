import click
from tabulate import tabulate

from objection.utils.frida_transport import FridaRunner
from objection.utils.templates import ios_hook


def get(args: list = None) -> None:
    """
        Gets cookies using the iOS NSHTTPCookieStorage sharedHTTPCookieStorage
        and primpts them to the screen.

        :param args:
        :return:
    """

    hook = ios_hook('binarycookie/get')

    runner = FridaRunner(hook=hook)
    runner.run()

    response = runner.get_last_message()

    if not response.is_successful():
        click.secho('Failed to get cookies with error: {0}'.format(
            response.error_reason), fg='red')
        return

    if not response.data:
        click.secho('No cookies found')
        return

    data = []

    for cookie in response.data:
        data.append([
            cookie['name'],
            cookie['value'],
            cookie['expiresDate'],
            cookie['domain'],
            cookie['path'],
            cookie['isSecure']
        ])

    click.secho(tabulate(data, headers=['Name', 'Value', 'Expires', 'Domain', 'Path', 'Secure']), bold=True)
