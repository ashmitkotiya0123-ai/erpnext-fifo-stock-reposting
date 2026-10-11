"""Minimal FIFO valuation queue for a single item/warehouse demonstration."""
from collections import deque
from dataclasses import dataclass
from typing import Deque


@dataclass
class Layer:
    qty: float
    rate: float


class FIFOStock:
    def __init__(self) -> None:
        self.layers: Deque[Layer] = deque()

    @property
    def quantity(self) -> float:
        return sum(layer.qty for layer in self.layers)

    @property
    def value(self) -> float:
        return sum(layer.qty * layer.rate for layer in self.layers)

    def receive(self, qty: float, rate: float) -> None:
        if qty <= 0:
            raise ValueError("Receipt quantity must be positive")
        if rate < 0:
            raise ValueError("Rate cannot be negative")
        self.layers.append(Layer(qty, rate))

    def issue(self, qty: float) -> float:
        """Issue qty from oldest layers; return total issue value."""
        if qty <= 0:
            raise ValueError("Issue quantity must be positive")
        if qty > self.quantity + 1e-9:
            raise ValueError(
                f"Insufficient stock: requested {qty}, available {self.quantity}"
            )

        remaining = qty
        total_cost = 0.0
        while remaining > 1e-9:
            layer = self.layers[0]
            used = min(layer.qty, remaining)
            total_cost += used * layer.rate
            layer.qty -= used
            remaining -= used
            if layer.qty <= 1e-9:
                self.layers.popleft()
        return round(total_cost, 2)

    def snapshot(self) -> list[tuple[float, float]]:
        """Return remaining (quantity, rate) layers for assertions/debugging."""
        return [(round(x.qty, 6), x.rate) for x in self.layers]
