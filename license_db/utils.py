from datetime import date, timedelta
from typing import Dict, Union


def year_after() -> date:
    return date.today() + timedelta(days=365)


def excel_columns() -> Dict[str, int]:
    columns = {
        'name': 0,
        'category': 1,
        'location': 2,
        'lic_type': 3,
        'quantity': 4,
        'expires': 5,
        'comment': 6,
    }

    return columns


def prepare_cell_value(
        row: tuple,
        column: str) -> Union[int, date, str]:

    columns = excel_columns()
    cell = row[columns[column]]

    if column == 'quantity':
        return int(cell.value)

    if column == 'expires':
        day, month, year = map(int, cell.value.split('.'))

        return date(year, month, day)

    return cell.value
