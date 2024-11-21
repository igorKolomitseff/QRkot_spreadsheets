from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'
ROW_COUNT_SPREADSHEET = 100
COLUMN_COUNT_SPREADSHEET = 5
SPREADSHEET_BODY_PROPERTIES = {
    'title': 'Отчёт от {current_date_time}',
    'locale': 'ru_RU'
}
FIRST_SHEET_PROPERTIES = {
    'sheetType': 'GRID',
    'sheetId': 0,
    'title': 'Лист1',
    'gridProperties': {
        'rowCount': ROW_COUNT_SPREADSHEET,
        'columnCount': COLUMN_COUNT_SPREADSHEET
    }
}
FIRST_SHEET_COLUMN_HEADERS = [
    ['Отчёт от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
RANGE = 'A1:E{row_count_max}'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body_properties = SPREADSHEET_BODY_PROPERTIES.copy()
    spreadsheet_body_properties['title'] = spreadsheet_body_properties[
        'title'
    ].format(
        current_date_time=datetime.now().strftime(FORMAT)
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(
            json={
                'properties': spreadsheet_body_properties,
                'sheets': [{
                    'properties': FIRST_SHEET_PROPERTIES
                }]
            }
        )
    )
    return response['spreadsheetId']


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
    table_values = [row[:] for row in FIRST_SHEET_COLUMN_HEADERS]
    table_values[0][1] = datetime.now().strftime(FORMAT)
    for project in projects:
        table_values.append([
            project['name'],
            str(project['close_date'] - project['create_date']),
            project['description']
        ])
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=RANGE.format(row_count_max=len(table_values)),
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    )
