from datetime import datetime
from app.models import AmountDateBase


def investing(
    target: AmountDateBase,
    sources: list[AmountDateBase]
) -> list[AmountDateBase]:
    changed = []
    for source in sources:
        amount_to_invest = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for object in (target, source):
            object.invested_amount += amount_to_invest
            if object.full_amount == object.invested_amount:
                object.fully_invested = True
                object.close_date = datetime.now()
        changed.append(source)
        if target.fully_invested:
            break
    return changed
