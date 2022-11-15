from collections import namedtuple
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


FORMAT = "%Y/%m/%d %H:%M:%S"

SHEETS_VERSION = {'sheets': 'v4'}
DRIVE_VERSION = {'drive': 'v3'}

TITLE_BODY = 'Отчет от {}'
LOCALE = 'ru_RU'

USER_TYPE = 'user'
USER_ROLE = 'writer'
USER_EMAIL = settings.email
PERMISSIONS_BODY = namedtuple('Permissions_body',
                              ['type', 'role', 'emailAddress'])
PERMISSIONS_FIELDS = 'id'

DIMENSION = 'ROWS'
UPDATE_BODY = namedtuple('Update_body', ['majorDimension', 'values'])

SHEET_PROPERTIES = {'sheetType': 'GRID',
                    'sheetId': 0,
                    'title': 'Лист1'}

GRID_PROPERTIES = {'gridProperties': {'rowCount': 100,
                   'columnCount': 3}}

SHEET_RANGE = 'A1:E30'
VALUE_INPUT_OPTION = 'USER_ENTERED'


def strfdelta(tdelta, fmt):
    time_result = {'days': abs(tdelta.days)}
    time_result['hours'], remaining = divmod(tdelta.seconds, 3600)
    time_result['minutes'], time_result['seconds'] = divmod(remaining, 60)
    return fmt.format(**time_result)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    date_time_now = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover(SHEETS_VERSION)
    spreadsheets_body = {'properties': {'title': TITLE_BODY.format(date_time_now),
                                        'locale': LOCALE},
                         'sheets': [{'properties': {**SHEET_PROPERTIES,
                                    **GRID_PROPERTIES}}]}
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheets_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
) -> None:
    permissions_body = PERMISSIONS_BODY(
        type=USER_TYPE,
        role=USER_ROLE,
        emailAddress=USER_EMAIL
    )._asdict()
    service = await wrapper_services.discover(DRIVE_VERSION)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields=PERMISSIONS_FIELDS
        ))


async def spreadsheets_update_value(
    spreadsheetid: str,
    projects: list,
    wrapper_services: Aiogoogle,
) -> None:
    date_time_now = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover(SHEETS_VERSION)
    table_values = [
        ['Отчет от', date_time_now],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for prj in projects:
        new_row = [
            str(prj['name']),
            str(
                strfdelta(
                    prj['duration'],
                    '{days} days {hours}:{minutes}:{seconds}'
                )
            ),
            str(prj['description'])]
        table_values.append(new_row)

    update_body = UPDATE_BODY(
        majorDimension=DIMENSION,
        values=table_values
    )._asdict()

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=SHEET_RANGE,
            valueInputOption=VALUE_INPUT_OPTION,
            json=update_body
        )
    )
