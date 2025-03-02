# main.py
from interfaces import Battle
from fighters import Knight
from weapons import Sword, Bow
from monsters import Drakiro, Groak
from items import SmallBag

def generate_item_id(counter: int = 1):
    """
    Функция для генерации уникального числового идентификатора для предмета.
    """
    counter += 1
    return counter


if __name__ == '__main__':
    # Инициализация объектов
    knight = Knight(id=generate_item_id(), health=100, defense=5)
    sword = Sword(id=generate_item_id(), attack_power=15)
    small_bag = SmallBag()

    small_bag.put(sword)
    knight.bag = small_bag
    knight.weapon = small_bag.take(sword.id)

    # Первый монстр
    drakiro_bag = SmallBag(1)
    bow = Bow(id=generate_item_id(), attack_power=10)
    drakiro_bag.put(bow)
    drakiro = Drakiro(id=generate_item_id(), health=50, attack_power=10)
    drakiro.bag = drakiro_bag

    Battle.fight(knight, drakiro)
    # Выпадает лук
    knight.weapon = bow

    # Второй монстр
    groak = Groak(id=generate_item_id(), health=60, attack_power=12)
    
    # Рыцарь стреляет из лука во второго монстра
    Battle.fight(knight, groak)