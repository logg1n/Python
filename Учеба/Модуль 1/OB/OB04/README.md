# Приложение для демонстрации принципа открытости/закрытости (Open/Closed Principle)

Цель этого домашнего задания - закрепить понимание и навыки применения принципа открытости/закрытости (Open/Closed Principle), одного из пяти SOLID принципов объектно-ориентированного программирования. Принцип гласит, что программные сущности (классы, модули, функции и т.д.) должны быть открыты для расширения, но закрыты для модификации.

## Описание

Принцип открытости/закрытости (OCP) предполагает, что поведение программы можно изменять и расширять без изменения ее исходного кода. Это достигается путем наследования и создания новых классов, которые расширяют функциональность базовых классов.

## Структура проекта

### fighters
- `fighter.py`: Абстрактный класс для бойцов.
- `knight.py`: Класс рыцаря, наследуется от `Fighter`.

### interfaces
- `bag.py`: Класс для управления сумкой персонажа.
- `character.py`: Абстрактный базовый класс для персонажей.
- `fight.py`: Класс для управления боями между персонажами и монстрами.
- `items.py`: Класс для предметов, которые могут находиться в сумке персонажа.

### items
- `small_bag.py`: Класс для небольших сумок.

### monsters
- `drakiro.py`: Класс монстра `Drakiro`.
- `groak.py`: Класс монстра `Groak`.
- `monster.py`: Абстрактный класс для монстров.

### weapons
- `bow.py`: Класс для лука.
- `sword.py`: Класс для меча.
- `weapon.py`: Класс для оружия.

### Пример вывода
    Knight берет Sword.
    Knight атакует Drakiro.
    Knight атакует с Sword!
    Drakiro получает урон 20. Оставшееся здоровье: 30
    Drakiro атакует рыцаря.
    Drakiro выпускает поток огня!
    Knight получает урон 5. Оставшееся здоровье: 95
    Knight атакует Drakiro.
    Knight атакует с Sword!
    Drakiro получает урон 20. Оставшееся здоровье: 10
    Drakiro атакует рыцаря.
    Drakiro выпускает поток огня!
    Knight получает урон 5. Оставшееся здоровье: 90
    Knight атакует Drakiro.
    Knight атакует с Sword!
    Drakiro получает урон 20. Оставшееся здоровье: -10
    Drakiro падает в куче пепла.
    Предмет Bow выпал.
    Knight берет Bow.
    Knight атакует Groak.
    Knight атакует с Bow!
    Groak получает урон 15. Оставшееся здоровье: 45
    Groak атакует рыцаря.
    Groak бросается с острыми когтями!
    Knight получает урон 7. Оставшееся здоровье: 83
    Knight атакует Groak.
    Knight атакует с Bow!
    Groak получает урон 15. Оставшееся здоровье: 30
    Groak атакует рыцаря.
    Groak бросается с острыми когтями!
    Knight получает урон 7. Оставшееся здоровье: 76
    Knight атакует Groak.
    Knight атакует с Bow!
    Groak получает урон 15. Оставшееся здоровье: 15
    Groak атакует рыцаря.
    Groak бросается с острыми когтями!
    Knight получает урон 7. Оставшееся здоровье: 69
    Knight атакует Groak.
    Knight атакует с Bow!
    Groak получает урон 15. Оставшееся здоровье: 0
    Groak издает последний рев, прежде чем замолчать навсегда.