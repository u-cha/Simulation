from random import randint, choice
import creature_state


class Entity:

    def __init__(self, *args, **kwargs):
        self.is_edible = 1  # this is only overrided in Obstacle subclass which is considered inedible


class Obstacle(Entity):
    collection = {'Rock': {'hp': 1000},
                  'Log': {'hp': 1000}}

    def __init__(self):
        super().__init__()
        self.is_edible = 0

    def __repr__(self):
        return f'Obst'  # first 2 letters in ...color


class Water(Entity):
    collection = {'Water': {'hp': 100}}

    def __init__(self):
        super().__init__()
        self.hp = self.collection['Water']['hp']

    def __repr__(self):
        return f'\033[34mWate\033[0m'  # first 2 letters in ...color


class Grass(Entity):
    collection = {'Grass': {'hp': 15}}

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f'\033[32mGras\033[0m'  # first 2 letters in ...color


class Creature(Entity):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.name = self.get_creature_a_name()
        role, hp, speed, vision_radius = self.get_creature_attributes()
        self.role = role
        self.hp = hp
        self.speed = speed
        self.vision_radius = vision_radius
        self.creature_state = creature_state.CreatureState()

    @staticmethod
    def get_creature_a_name():
        with open('names.txt') as names:
            name = choice(names.readlines()).strip()
        return name

    def get_creature_attributes(self):
        dic = self.collection
        role = choice(list(dic))
        hp = dic[role]['maxhp']
        speed = dic[role]['speed']
        vision_radius = dic[role]['vision_radius']
        return role, hp, speed, vision_radius

    def make_move(self):  # Наследники будут реализовывать этот метод каждый по-своему.
        pass

    def die(self):
        pass

    def consume(self):
        pass

    def decide_what_to_do(self):
        pass


class Herbivore(Creature):
    """Стремятся найти ресурс (траву),
     может потратить свой ход на движение в сторону травы, либо на её поглощение."""

    collection = {'Horse': {'speed': 3, 'maxhp': 100, 'vision_radius': 10},
                  'Rabbit': {'speed': 5, 'maxhp': 10, 'vision_radius': 10}}

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f'\033[36m{self.role[:4]}\033[0m'


class Predator(Creature):
    """
    На что может потратить ход хищник:

    Переместиться (чтобы приблизиться к жертве - травоядному)
    Атаковать травоядное. При этом количество HP травоядного уменьшается на силу атаки хищника.
    Если значение HP жертвы опускается до 0, травоядное исчезает
    """
    collection = {'Tiger': {'speed': 6, 'maxhp': 500, 'attack_power': 10, 'vision_radius': 5},
                  'Lion': {'speed': 4, 'maxhp': 700, 'attack_power': 10, 'vision_radius': 7}}

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f'\033[31m{self.role[:4]}\033[0m'

    def attack(self):
        pass
