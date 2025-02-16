from typing import Dict


class Store:
    def __init__(self, name, address, items: Dict[str, float] = {}):
        self.name = name
        self.address = address
        self.items = items

    def product_add(self, product, price: float):
        self.items.update({product: price})

    def product_remove(self, product):
        return self.items.pop(product, False)

    def price_get(self, product) -> float:
        return self.items.get(product)

    def price_update(self, product, price):
        self.items.update({product: price})

    def products_get(self) -> Dict[str, float]:
        return self.items


store1 = Store("Магазин №1", "Улица 1, Город А")
store2 = Store("Магазин №2", "Улица 2, Город Б")
store3 = Store("Магазин №3", "Улица 3, Город В")
store4 = Store("Магазин №4", "Улица 4, Город Г")

products = {"Яблоки": 2.5, "Бананы": 1.2, "Хлеб": 1.0, "Молоко": 0.8, "Кофе": 5.0}

for product, price in products.items():
    store1.product_add(product, price)

print("Исходный список товаров в магазине:")
print(store1.products_get())

# Добавление товара
store1.product_add("Чай", 3.0)
print("\nПосле добавления товара 'Чай':")
print(store1.products_get())

# Удаление товара
store1.product_remove("Хлеб")
print("\nПосле удаления товара 'Хлеб':")
print(store1.products_get())

# Получение цены товара
price = store1.price_get("Бананы")
print(f"\nЦена товара 'Бананы': {price}")

# Обновление цены товара
store1.price_update("Молоко", 0.9)
print("\nПосле обновления цены товара 'Молоко':")
print(store1.products_get())

# Получение всех товаров
print("\nТекущий список товаров в магазине:")
print(store1.products_get())


# Исходный список товаров в магазине:
# {'Яблоки': 2.5, 'Бананы': 1.2, 'Хлеб': 1.0, 'Молоко': 0.8, 'Кофе': 5.0}
#
# После добавления товара 'Чай':
# {'Яблоки': 2.5, 'Бананы': 1.2, 'Хлеб': 1.0, 'Молоко': 0.8, 'Кофе': 5.0, 'Чай': 3.0}
#
# После удаления товара 'Хлеб':
# {'Яблоки': 2.5, 'Бананы': 1.2, 'Молоко': 0.8, 'Кофе': 5.0, 'Чай': 3.0}
#
# Цена товара 'Бананы': 1.2
#
# После обновления цены товара 'Молоко':
# {'Яблоки': 2.5, 'Бананы': 1.2, 'Молоко': 0.9, 'Кофе': 5.0, 'Чай': 3.0}
#
# Текущий список товаров в магазине:
# {'Яблоки': 2.5, 'Бананы': 1.2, 'Молоко': 0.9, 'Кофе': 5.0, 'Чай': 3.0}
