"""Inventory management system module.

Object-oriented design without global variables.
Provides secure, type-safe, and PEP8-compliant inventory operations.
"""

from __future__ import annotations
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional


class InventoryManager:
    """A class-based inventory manager."""

    def __init__(self) -> None:
        """Initialize an empty inventory."""
        self.stock_data: Dict[str, int] = {}

    def add_item(
        self,
        item: str,
        qty: int = 0,
        logs: Optional[List[str]] = None,
    ) -> None:
        """Add quantity of an item to the inventory."""
        if not isinstance(item, str) or not item.strip():
            raise ValueError("item must be a non-empty string")
        if not isinstance(qty, int) or qty < 0:
            raise ValueError("qty must be a non-negative integer")

        current = self.stock_data.get(item, 0)
        self.stock_data[item] = current + qty

        if logs is None:
            logs = []
        timestamp = datetime.now().isoformat(timespec="seconds")
        logs.append(f"{timestamp}: Added {qty} of {item}")

        logging.debug(
            "Added %d of %s (new total=%d)",
            qty,
            item,
            self.stock_data[item],
        )

    def remove_item(self, item: str, qty: int) -> None:
        """Remove quantity of an existing item."""
        if not isinstance(item, str) or not item.strip():
            raise ValueError("item must be a non-empty string")
        if not isinstance(qty, int) or qty <= 0:
            raise ValueError("qty must be a positive integer")
        if item not in self.stock_data:
            raise KeyError(f"Item '{item}' not found in inventory")

        new_qty = self.stock_data[item] - qty
        if new_qty > 0:
            self.stock_data[item] = new_qty
        else:
            del self.stock_data[item]

        logging.debug(
            "Removed %d of %s (remaining=%s)",
            qty,
            item,
            self.stock_data.get(item),
        )

    def get_qty(self, item: str) -> int:
        """Return quantity for an item, or 0 if not present."""
        if not isinstance(item, str) or not item.strip():
            raise ValueError("item must be a non-empty string")
        return self.stock_data.get(item, 0)

    def load_data(self, file_path: str = "inventory.json") -> None:
        """Load inventory data from JSON file into the in-memory store."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Inventory file must contain a JSON object")

            cleaned: Dict[str, int] = {}
            for key, value in data.items():
                if (
                    isinstance(key, str)
                    and isinstance(value, int)
                    and value >= 0
                ):
                    cleaned[key] = value
                else:
                    logging.warning(
                        "Ignoring invalid record: %r -> %r",
                        key,
                        value,
                    )

            self.stock_data = cleaned

            logging.info(
                "Loaded %d items from %s",
                len(self.stock_data),
                file_path,
            )
        except FileNotFoundError:
            logging.info(
                "No inventory file found at %s; starting fresh",
                file_path,
            )
            self.stock_data = {}
        except (json.JSONDecodeError, OSError, ValueError) as exc:
            logging.error("Failed to load from %s: %s", file_path, exc)

    def save_data(self, file_path: str = "inventory.json") -> None:
        """Persist current inventory to a JSON file."""
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.stock_data, f, ensure_ascii=False, indent=2)

        logging.info(
            "Saved %d items to %s",
            len(self.stock_data),
            file_path,
        )

    def print_data(self) -> None:
        """Print all inventory items and quantities."""
        print("Items Report")
        for name in sorted(self.stock_data):
            print(f"{name} -> {self.stock_data[name]}")

    def check_low_items(self, threshold: int = 5) -> List[str]:
        """Return items below a certain threshold."""
        if not isinstance(threshold, int) or threshold < 0:
            raise ValueError("threshold must be non-negative")
        return [n for n, q in self.stock_data.items() if q < threshold]


def _demo_flow() -> None:
    """Demonstrate the inventory manager."""
    logs: List[str] = []
    inv = InventoryManager()
    inv.add_item("apple", 10, logs)
    try:
        inv.add_item("banana", -2, logs)
    except ValueError:
        logging.info("Rejected negative quantity for banana")

    try:
        inv.remove_item("apple", 3)
        inv.remove_item("orange", 1)
    except KeyError as exc:
        logging.info("Tried to remove non-existent item: %s", exc)

    print("Apple stock:", inv.get_qty("apple"))
    print("Low items:", inv.check_low_items())
    inv.save_data()
    inv.load_data()
    inv.print_data()

    if logs:
        print("\nAudit trail:")
        for line in logs:
            print(line)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    _demo_flow()
