from random import randint, choice
from gameparameters import GameParameters as gameparams
from creature_state import CreatureState


class Entity:
    collection = {}

    def __init__(self):
        self._is_edible = 1  # this is only overrided in Obstacle subclass which is considered inedible
        if len(self.collection) > 0:
            entityrole = choice(list(self.collection.keys()))
            setattr(self, '_role', entityrole)
            for attribute in self.collection[entityrole]:
                setattr(self, attribute, self.collection[entityrole][attribute])
            if getattr(self, '_maxhp', None):
                self._hp = self._maxhp

    def __repr__(self):
        if getattr(self, '_role', None):
            return f'{self._role[:4]}'
        return 'class Entity'

    def _find_adjacent_cells(self, searchradius=1, *args):
        adjacent_cells = []
        already_visited_cells = []
        for width in range(self.width - searchradius, self.width + searchradius + 1):
            for height in range(self.height - searchradius, self.height + searchradius + 1):
                if (width < 0 or height < 0
                        or width >= gameparams.mapwidth
                        or height >= gameparams.mapheight
                        or width == self.width and height == self.height
                        or (width, height) in already_visited_cells):
                    pass
                else:
                    adjacent_cells.append((width, height))
                    already_visited_cells.append((width, height))
        return adjacent_cells

    @staticmethod
    def _filter_free_cells(cells, worldmap):
        return list(filter(lambda x: worldmap.worldpopulation[x] is None, cells))

    def _end_existence(self):
        self._is_to_be_deleted = 1


class Obstacle(Entity):
    collection = {'Rock': {'_maxhp': 1000},
                  'Log': {'_maxhp': 1000}}

    def __init__(self):
        super().__init__()
        self.is_edible = 0

    def make_move(self, *args):
        pass


class Water(Entity):
    collection = {'Water': {'_drink_value': 100}}

    def __init__(self):
        super().__init__()

    def make_move(self, *args):
        pass


class Grass(Entity):
    collection = {'Grass': {'_food_value': 15}}

    def __init__(self):
        super().__init__()
        self._is_being_consumed = 0

    def make_move(self, *args):
        if self._is_being_consumed:
            self._food_value -= 1
        if self._food_value <= 0:
            self._end_existence()


class Creature(Entity):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.name = self.__get_creature_a_name()
        self.creature_state = CreatureState()

    @staticmethod
    def __get_creature_a_name():
        with open('names.txt') as names:
            name = choice(names.readlines()).strip()
        return name

    def __die(self):
        self.is_alive = 0

    def make_move(self, worldmap):
        if self.creature_state._is_to_be_deleted:
            pass
        else:
            if self.creature_state._is_alive:
                if self.creature_state._is_fleeing:
                    self._make_escape_move()
                elif not self.creature_state._is_hungry:
                    self._make_foodhunt_move(worldmap)
                else:
                    self._make_free_move(worldmap)
            else:
                if self.creature_state._is_being_consumed and self._food_value > 0:
                    self._food_value -= 1
                else:
                    self._end_to_exist()

    def _make_free_move(self, worldmap):
        free_adjacent_cells = self._filter_free_cells(self._find_adjacent_cells(), worldmap)
        if len(free_adjacent_cells) == 0:
            pass

        else:
            next_cell = choice(free_adjacent_cells)
            worldmap.worldpopulation[self.width, self.height] = None
            worldmap.worldpopulation[next_cell] = self
            self.width, self.height = next_cell


    def _make_escape_move(self):
        pass

    def _make_foodhunt_move(self, worldmap):
        target_cell = self._find_cell_with_food(self, worldmap)
        if target_cell is None:
            self._make_free_move(self, worldmap)
        else:
            next_cell = self._find_next_cell_with_bfs(self, target_cell, worldmap)
            # make_targeted_move

    def _find_cell_with_food(self, worldmap):
        for search_radius in range(1, self._vision_radius + 1):
            current_search_scope = self._find_adjacent_cells(searchradius=search_radius)
            for cell in current_search_scope:
                if worldmap.worldpopulation[cell].__class__.__name__ == self._food_type:
                    return cell
        else:
            return None


    def die(self):
        pass

    def consume(self):
        pass

    def decide_what_to_do(self):
        pass



class Herbivore(Creature):
    """Стремятся найти ресурс (траву),
     может потратить свой ход на движение в сторону травы, либо на её поглощение."""

    collection = {'Horse':
                      {'_speed': 3, '_maxhp': 100, '_vision_radius': 10,
                       '_food_value': 10, '_food_type': 'Grass'},
                  'Rabbit':
                      {'_speed': 5, '_maxhp': 10, '_vision_radius': 10,
                       '_food_value': 10, '_food_type': 'Grass'}}

    def __init__(self):
        super().__init__()






class Predator(Creature):
    """
    На что может потратить ход хищник:

    Переместиться (чтобы приблизиться к жертве - травоядному)
    Атаковать травоядное. При этом количество HP травоядного уменьшается на силу атаки хищника.
    Если значение HP жертвы опускается до 0, травоядное исчезает
    """
    collection = {'Tiger':
                      {'_speed': 6, '_maxhp': 500, '_attack_power': 10,
                       '_vision_radius': 5, '_food_value': 10, '_food_type': 'Herbivore'},
                  'Lion':
                      {'_speed': 4, '_maxhp': 700, '_attack_power': 10,
                       '_vision_radius': 7, '_food_value': 10, '_food_type': 'Herbivore'}}

    def __init__(self):
        super().__init__()
        self._is_a_threat = 1

    def attack(self):
        pass

