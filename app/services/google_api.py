import copy
from datetime import datetime

from aiogoogle import Aiogoogle

from .constants import SHEET_COLUMN_COUNT, SHEET_ROW_COUNT
from .validators import check_column_count, check_row_count
from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'
SPREADSHEET_TITLE = 'Отчёт от {current_date_time}'
SPREADSHEET_BODY = {
    'properties': {
        'title': '',
        'locale': 'ru_RU'
    },
    'sheets': [{
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Лист1',
            'gridProperties': {
                'rowCount': SHEET_ROW_COUNT,
                'columnCount': SHEET_COLUMN_COUNT
            }
        }
    }]
}
FIRST_SHEET_COLUMN_HEADERS = [
    ['Отчёт от'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> tuple[str, str]:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = copy.deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] = SPREADSHEET_TITLE.format(
        current_date_time=datetime.now().strftime(FORMAT)
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(
            json=spreadsheet_body
        )
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json={
                'type': 'user',
                'role': 'writer',
                'emailAddress': settings.email
            },
            fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: list,
    wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_headers = copy.deepcopy(FIRST_SHEET_COLUMN_HEADERS)
    table_headers[0].append(datetime.now().strftime(FORMAT))
    table_values = [
        *table_headers,
        *[list(map(str, (
            project['name'],
            project['close_date'] - project['create_date'],
            project['description']
        ))) for project in projects],
    ]
    insert_row_count = len(table_values)
    insert_column_count = max(map(len, table_values))
    check_row_count(insert_row_count)
    check_column_count(insert_column_count)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{insert_row_count}C{insert_column_count}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    )
