from replay import replay


def show(label, result):
    print(f"\n{label}")
    print(f"Jan 15 Milk issue value:       ₹{result.jan15_issue_value:,.2f}")
    print(f"Jan 21 Milk consumption cost:  ₹{result.jan21_milk_consumption_value:,.2f}")
    print(f"Milk Powder cost per kg:       ₹{result.powder_unit_cost:,.2f}")
    print(f"Jan 25 Powder issue value:     ₹{result.jan25_powder_issue_value:,.2f}")
    print(f"Remaining Milk quantity:       {result.remaining_milk_qty:.2f} L")
    print(f"Remaining Milk value:          ₹{result.remaining_milk_value:,.2f}")
    print(f"Remaining Milk FIFO layers:    {result.milk_layers_after_manufacture}")


if __name__ == "__main__":
    show("BEFORE EDIT (Jan 10 rate ₹60/L)", replay(60))
    show("AFTER EDIT (Jan 10 rate ₹80/L)", replay(80))
