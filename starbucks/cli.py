import click

from .starbucks import Starbucks

@click.command()
@click.option('--id', 'id_', help='starbucks id', required=True)
@click.option('--password', 'password', help='starbucks password',
              required=True)
@click.option('--reg-number', 'reg_number', help='starbucks card reg number',
              required=True)
def card_info(id_, password, reg_number):
    sb = Starbucks()
    click.echo('Trying to login with {}'.format(id_))
    logined = sb.login(id_, password)
    if not logined:
        raise click.BadParameter('id or password incorrect')
    click.echo('[login success] hello {} :) !'.format(id_))
    click.echo('-------- [card information] --------')
    click.echo(sb.get_card_info(reg_number))
