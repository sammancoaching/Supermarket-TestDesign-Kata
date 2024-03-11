from dataclasses import dataclass
from enum import Enum


class ProductUnit(Enum):
    EACH = 0
    KILO = 2


@dataclass(frozen=True)
class Product:
    name: str
    unit: ProductUnit


@dataclass(frozen=True)
class ProductQuantity:
    product: Product
    quantity: float


class SupermarketCatalog:
    def add_product(self, product: Product, price: float) -> None:
        raise Exception("cannot be called from a unit test - it accesses the database")

    def unit_price(self, product: Product) -> float:
        raise Exception("cannot be called from a unit test - it accesses the database")
