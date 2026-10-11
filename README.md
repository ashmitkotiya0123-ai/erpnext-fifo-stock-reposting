# ERPNext FIFO Stock Reposting — Design Demonstration

A small, standalone Python demonstration of replaying FIFO inventory valuation after a backdated Purchase Receipt rate edit. This is **not** production ERPNext code and does not modify an ERPNext database.

## Scenario

- Opening Milk: 100 L @ ₹50/L
- Jan 10: receive 50 L @ ₹60/L (then edit to ₹80/L)
- Jan 15: issue 80 L
- Jan 20: receive 50 L @ ₹60/L
- Jan 21: consume 100 L Milk to produce 10 kg Milk Powder
- Jan 25: issue 10 kg Milk Powder

Assumptions: single warehouse, no negative stock, no extra manufacturing cost, all Milk input cost assigned to Milk Powder, and no rounding beyond Python's normal float arithmetic in this demo.

## Run

Requires Python 3.10+.

```bash
python -m unittest discover -s tests -v
python demo.py
```

## Design

- `fifo.py` implements a queue of quantity/rate layers and consumes oldest layers first.
- `replay.py` replays a deterministic event stream from the beginning, including the simplified Milk → Milk Powder dependency.
- Editing the Jan 10 receipt means changing its rate and replaying the affected chronological event stream, not applying a fixed adjustment to every later transaction.
- Tests assert the key before/after values.

## Expected results

Before edit:
- Jan 21 Milk consumption: ₹5,800
- Milk Powder cost: ₹580/kg
- Jan 25 Powder issue: ₹5,800

After Jan 10 rate changes to ₹80/L:
- Jan 21 Milk consumption: ₹6,800
- Milk Powder cost: ₹680/kg
- Jan 25 Powder issue: ₹6,800
- Remaining Milk: 20 L, value ₹1,200

The Jan 15 issue remains valued at ₹4,000 because it consumes 80 L from opening stock at ₹50/L.

## Production considerations

A real ERPNext implementation must integrate with Stock Ledger Entry replay/reposting, source vouchers, warehouse/item dimensions, posting-time ordering, cancellation and amendment semantics, stock queues, negative-stock rules, manufacturing/repack dependencies, precision/rounding, accounting ledger updates, transaction boundaries, locking, and retry/resume behaviour. Do not replace ERPNext's stock ledger code with this demo.
## Problems with Running Balances in Stock Ledger Entries

If every Stock Ledger Entry stores a running balance, editing an earlier transaction can make later balances incorrect.

- **Stale balances:** Subsequent entries may continue showing quantities and values calculated using the old purchase rate.
- **Incorrect FIFO valuation:** Later stock issues may consume incorrect cost layers if affected entries are not recalculated.
- **Dependency issues:** A changed Milk consumption cost can affect the valuation of manufactured Milk Powder and its later delivery.
- **Data inconsistency:** Stock Ledger Entries and accounting records may no longer agree if only some transactions are updated.
- **Performance and concurrency:** Recalculating many entries can be expensive, and simultaneous stock transactions can cause conflicts if reposting is not coordinated.

### Proposed Approach

Replay affected stock transactions in chronological order from a safe point before the edited transaction. Recalculate FIFO layers, quantities, and values, then propagate changes to dependent manufacturing and stock issues. Update related accounting entries consistently, using appropriate transaction controls and error handling.

This repository demonstrates the replay concept in a simplified Python model; it does not implement ERPNext's production reposting mechanism.
## Transactions Affected by the Rate Edit

Changing the January 10 Purchase Receipt rate from ₹60/L to ₹80/L changes the cost layer introduced by that receipt.

- **January 15 Milk Delivery Note:** Under the given FIFO assumptions, its value remains ₹4,000 because the 80 L issue consumes opening stock at ₹50/L.
- **January 20 Milk Purchase Receipt:** Its own incoming rate remains ₹60/L, but its resulting stock balance must be recalculated as part of the replay.
- **January 21 Manufacture Entry:** The cost of the 100 L Milk consumed changes from ₹5,800 to ₹6,800. Consequently, the 10 kg Milk Powder produced changes from ₹580/kg to ₹680/kg.
- **January 25 Milk Powder Delivery Note:** Its issue value changes from ₹5,800 to ₹6,800 because it consumes the repriced Milk Powder stock.

The edited January 10 Purchase Receipt itself must also be reflected in the replay. Exact ERPNext reposting scope depends on the stock ledger ordering and dependencies.
