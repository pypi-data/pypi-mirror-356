"""Command to interact with the orders endpoint."""

from __future__ import annotations

import requests
import typer

from app.console import console
from app.constants import API_KEY_NAME, ApiPaths, API_REQUEST_TIMEOUT_SEC
from app.utils.checks import require_api_endpoint_and_key
from app.utils.datetime_utils import format_utc_to_local
from rich.table import Table

order_commands = typer.Typer()


def format_items(items_list):
    """Format the items list as a comma-separated string of
    part_number:count.
    """
    return ', '.join(
        f"{item['part_number']}:{item['count']}"
        for item in items_list
        if 'part_number' in item and 'count' in item
    )


@order_commands.command(name='display')
@require_api_endpoint_and_key()
def print_orders(
    ctx: typer.Context,
):
    """Display all of the orders in the inventory."""

    api_endpoint = ctx.obj['api_endpoint']
    api_key = ctx.obj['api_key']

    orders_url = f'{api_endpoint}{ApiPaths.ORDERS}'
    headers = {API_KEY_NAME: api_key}

    page = 1
    size = 50
    items = []

    while True:
        result = requests.get(
            orders_url,
            headers=headers,
            params={'page': page, 'size': size},
            timeout=API_REQUEST_TIMEOUT_SEC,
        )
        result.raise_for_status()
        data = result.json()
        current_items = data.get('items', [])
        items.extend(current_items)
        pages = data.get('pages', 1)
        if page >= pages:
            break
        page += 1

    if not items:
        console.print('No orders found.')
        raise typer.Exit(code=0)

    table = Table(title='Orders', show_lines=True)
    table.add_column('Quote Reference', justify='left')
    table.add_column('Order Reference', justify='left')
    table.add_column('Invoice Reference', justify='left')
    table.add_column('Status', justify='left')
    table.add_column('Items', justify='left')
    table.add_column('Created By', justify='left')
    table.add_column('Created At', justify='left')
    table.add_column('Updated By', justify='left')
    table.add_column('Updated At', justify='left')

    for item in items:
        table.add_row(
            item.get('quote_reference', ''),
            item.get('order_reference', ''),
            item.get('invoice_reference', ''),
            item.get('status', ''),
            format_items(item.get('items', [])),
            item.get('created_by', ''),
            format_utc_to_local(item['created_at_utc']),
            item.get('updated_by', ''),
            format_utc_to_local(item['updated_at_utc']),
        )

    console.print(table)
