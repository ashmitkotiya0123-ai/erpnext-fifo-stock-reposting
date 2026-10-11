"""Chronological replay for the simplified Milk -> Milk Powder scenario."""
from dataclasses import dataclass
from fifo import FIFOStock


@dataclass
class ReplayResult:
    jan15_issue_value: float
    jan21_milk_consumption_value: float
    powder_unit_cost: float
    jan25_powder_issue_value: float
    remaining_milk_qty: float
    remaining_milk_value: float
    milk_layers_after_manufacture: list[tuple[float, float]]


def replay(jan10_rate: float = 60.0) -> ReplayResult:
    milk = FIFOStock()
    powder = FIFOStock()

    # Opening balance is the initial FIFO layer.
    milk.receive(100, 50)

    # Jan 10 Purchase Receipt (rate is editable).
    milk.receive(50, jan10_rate)

    # Jan 15 Delivery Note.
    jan15_issue = milk.issue(80)

    # Jan 20 Purchase Receipt.
    milk.receive(50, 60)

    # Jan 21 Manufacture Entry: consume 100 L and produce 10 kg.
    manufacturing_cost = milk.issue(100)
    powder_rate = manufacturing_cost / 10
    powder.receive(10, powder_rate)

    milk_layers = milk.snapshot()
    remaining_milk_qty = milk.quantity
    remaining_milk_value = milk.value

    # Jan 25 Delivery Note.
    jan25_issue = powder.issue(10)

    return ReplayResult(
        jan15_issue_value=jan15_issue,
        jan21_milk_consumption_value=manufacturing_cost,
        powder_unit_cost=round(powder_rate, 2),
        jan25_powder_issue_value=jan25_issue,
        remaining_milk_qty=round(remaining_milk_qty, 2),
        remaining_milk_value=round(remaining_milk_value, 2),
        milk_layers_after_manufacture=milk_layers,
    )
