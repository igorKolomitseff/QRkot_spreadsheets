INVALID_ROW_SHEET_ROW_COUNT = (
    'Данные для обновления превышают допустимое количество строк. '
    'Допустимо: {sheet_row_count}. '
    'Требуется: {insert_row_count}.'
)
INVALID_COLUMN_SHEET_ROW_COUNT = (
    'Данные для обновления превышают допустимое количество столбцов. '
    'Допустимо: {sheet_column_count}. '
    'Требуется: {insert_column_count}.'
)


def check_row_count(
    insert_row_count, sheet_row_count
) -> None:
    if insert_row_count > sheet_row_count:
        raise ValueError(
            INVALID_ROW_SHEET_ROW_COUNT.format(
                sheet_row_count=sheet_row_count,
                insert_row_count=insert_row_count
            )
        )


def check_column_count(
    insert_column_count, sheet_column_count
) -> None:
    if insert_column_count > sheet_column_count:
        raise ValueError(
            INVALID_COLUMN_SHEET_ROW_COUNT.format(
                sheet_column_count=sheet_column_count,
                insert_column_count=insert_column_count
            )
        )
