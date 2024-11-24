from .constants import SHEET_COLUMN_COUNT, SHEET_ROW_COUNT

INVALID_SHEET_ROW_COUNT = (
    'Данные для обновления превышают допустимое количество строк. '
    f'Допустимо: {SHEET_ROW_COUNT}. '
    'Требуется: {insert_row_count}.'
)
INVALID_SHEET_COLUMN_COUNT = (
    'Данные для обновления превышают допустимое количество столбцов. '
    f'Допустимо: {SHEET_COLUMN_COUNT}. '
    'Требуется: {insert_column_count}.'
)


def check_row_count(insert_row_count: int) -> None:
    if insert_row_count > SHEET_ROW_COUNT:
        raise ValueError(
            INVALID_SHEET_ROW_COUNT.format(
                insert_row_count=insert_row_count
            )
        )


def check_column_count(insert_column_count: int) -> None:
    if insert_column_count > SHEET_COLUMN_COUNT:
        raise ValueError(
            INVALID_SHEET_COLUMN_COUNT.format(
                insert_column_count=insert_column_count
            )
        )
