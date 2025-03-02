from typing import Dict

from fighters import Fighter
from interfaces import Items
from monsters import Monster

class Battle:
   @staticmethod
   def fight(fighter: Fighter, monster: Monster):

      if isinstance(fighter, Fighter) and isinstance(monster, Monster):
         print(f"{fighter.__class__.__name__} берет {fighter.weapon.__class__.__name__}.")

         while fighter.alive or monster.alive:
            print(f"{fighter.__class__.__name__} атакует {monster.__class__.__name__}.")
            monster.take_damage(fighter.attack())
            if not monster.is_alive():
               prize: Dict[int, Items] = monster.dead()
               if prize:
                  fighter.take_prize(prize)

               break

            print(f"{monster.__class__.__name__} атакует рыцаря.")
            fighter.take_damage(monster.attack())
            if not fighter.is_alive():
               fighter.dead()
               break
