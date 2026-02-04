from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import List

from flask import Flask, render_template, request

app = Flask(__name__)


@dataclass
class LineItem:
    description: str
    quantity: Decimal
    unit_price: Decimal
    discount_rate: Decimal

    @property
    def total(self) -> Decimal:
        subtotal = self.quantity * self.unit_price
        discount_amount = subtotal * self.discount_rate / Decimal("100")
        return subtotal - discount_amount


def _to_decimal(value: str, default: Decimal = Decimal("0")) -> Decimal:
    try:
        cleaned = value.replace(",", ".").strip()
        if cleaned == "":
            return default
        return Decimal(cleaned)
    except (InvalidOperation, AttributeError):
        return default


def _parse_items(form: dict) -> List[LineItem]:
    descriptions = form.getlist("item_desc[]")
    quantities = form.getlist("item_qty[]")
    prices = form.getlist("item_price[]")
    discounts = form.getlist("item_discount[]")

    items: List[LineItem] = []
    for description, qty, price, discount in zip(descriptions, quantities, prices, discounts):
        quantity = _to_decimal(qty)
        unit_price = _to_decimal(price)
        discount_rate = _to_decimal(discount)
        if quantity <= 0 or unit_price < 0:
            continue
        items.append(
            LineItem(
                description=description.strip() or "Producto",
                quantity=quantity,
                unit_price=unit_price,
                discount_rate=discount_rate,
            )
        )
    return items


@app.route("/", methods=["GET", "POST"])
def index():
    items: List[LineItem] = []
    tax_rate = Decimal("19")
    discount = Decimal("0")

    if request.method == "POST":
        items = _parse_items(request.form)
        tax_rate = _to_decimal(request.form.get("tax_rate", "0"))
        discount = _to_decimal(request.form.get("discount", "0"))

    subtotal = sum((item.total for item in items), Decimal("0"))
    tax_amount = subtotal * tax_rate / Decimal("100")
    total = subtotal + tax_amount - discount
    if total < 0:
        total = Decimal("0")

    return render_template(
        "index.html",
        items=items,
        tax_rate=tax_rate,
        discount=discount,
        subtotal=subtotal,
        tax_amount=tax_amount,
        total=total,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
