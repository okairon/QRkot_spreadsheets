from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


FORMAT = "%Y/%m/%d %H:%M:%S"


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    date_time_now = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheets_body = {
        'properties': {'title': f'Отчет от {date_time_now}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 3}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheets_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
    spreadsheetid: str,
    projects: list,
    wrapper_services: Aiogoogle,
) -> None:
    date_time_now = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
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

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
