from random import randint, choice
from gameparameters import GameParameters as gameparams
from creature_state import CreatureState


class Entity:
    collection = {}

    def __init__(self):
        self._is_to_be_deleted = 0
        if len(self.collection) > 0:
            entityrole = choice(list(self.collection.keys()))
            setattr(self, '_role', entityrole)
            for attribute in self.collection[entityrole]:
                setattr(self, attribute, self.collection[entityrole][attribute])
            if getattr(self, '_maxhp', None):
                self._hp = self._maxhp
            else:
                self._hp = 0000

    def __repr__(self):
        if getattr(self, '_role', None):
            return f'{self._role[:4]}, {self._hp}, {round(self._food_value)}'

    def entity_update_self_status(self):
        if hasattr(self, '_food_value') and self._food_value == 0 and self._hp == 0:
            self._is_to_be_deleted = 1



    def _find_adjacent_cells(self, coordinates: tuple = None,  searchradius=1, *args):
        """This function looks for adjacent cells, starting from the position of self or (if given)
        starting from the coordinates position.
        Basically it returns adjacent cells within 1 cell radius, but this can be changed
        if another radius is provided"""

        if coordinates:
            width_pos, height_pos = coordinates[0], coordinates[1]
        else:
            width_pos, height_pos = self.width, self.height

        adjacent_cells = []
        already_visited_cells = []
        for width in range(width_pos - searchradius, width_pos + searchradius + 1):
            for height in range(height_pos - searchradius, height_pos + searchradius + 1):
                if (width < 0 or height < 0
                        or width >= gameparams.mapwidth
                        or height >= gameparams.mapheight
                        or width == width_pos and height == height_pos
                        or (width, height) in already_visited_cells):
                    pass
                else:
                    adjacent_cells.append((width, height))
                    already_visited_cells.append((width, height))
        return adjacent_cells

    @staticmethod
    def _filter_empty_cells(cells, worldmap):
        return list(filter(lambda x: worldmap.worldpopulation[x] is None, cells))

    def _end_existence(self):
        self._is_to_be_deleted = 1


class Obstacle(Entity):
    collection = {'Rock': {'_maxhp': 1000, '_food_value': 0},
                  'Log': {'_maxhp': 1000, '_food_value': 0}}

    def __init__(self):
        super().__init__()


    def make_move(self, *args):
        pass


class Water(Entity):
    collection = {'Water': {'_food_value': 100}}

    def __init__(self):
        super().__init__()

    def make_move(self, *args):
        pass


class Grass(Entity):
    collection = {'Grass': {'_max_food_value': 1, '_growthtempo': 0.2}}

    def __init__(self):
        super().__init__()
        self._food_value = self._max_food_value

    def make_move(self, *args):
        if self._food_value < self._max_food_value:
            self._food_value += self._growthtempo


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
        if not self.creature_state._is_alive or self.creature_state._is_under_attack:
            pass
        else:
            if self.creature_state._is_hungry:
                self._make_foodhunt_move(worldmap)
            else:
                self.creature_state.hungertimer.tick()
                if self.creature_state.hungertimer.timer == 10:
                    self.creature_state._is_hungry = 1
                self._make_free_move(worldmap)


    def _make_free_move(self, worldmap):
        free_adjacent_cells = self._filter_empty_cells(self._find_adjacent_cells(), worldmap)
        if len(free_adjacent_cells) == 0:
            pass

        else:
            next_cell = choice(free_adjacent_cells)
            worldmap.worldpopulation[self.width, self.height] = None
            worldmap.worldpopulation[next_cell] = self
            self.width, self.height = next_cell


    def _make_foodhunt_move(self, worldmap):
        target_cell = self._find_cell_with_food(worldmap)
        if target_cell:
            if target_cell in self._find_adjacent_cells():
                target = worldmap.worldpopulation[target_cell]
                if hasattr(target, 'creature_state') and target.creature_state._is_alive == 1:
                    self.attack(target_cell, worldmap)
                elif hasattr(target, 'creature_state') and target.creature_state._is_alive ==0:
                    self.consume(target_cell, worldmap)
                else:
                    self.consume(target_cell, worldmap)
            else:
                next_cell = self._find_next_cell_using_bfs(target_cell, worldmap)
                worldmap.worldpopulation[self.width, self.height] = None
                worldmap.worldpopulation[next_cell] = self
                self.width, self.height = next_cell
        else:
            self._make_free_move(worldmap)


    def _find_cell_with_food(self, worldmap):
        for search_radius in range(1, self._vision_radius + 1):
            current_search_scope = self._find_adjacent_cells(searchradius=search_radius)
            for cell in current_search_scope:
                if worldmap.worldpopulation[cell].__class__.__name__ == self._food_type:
                    return cell
        else:
            return None


    def _find_next_cell_using_bfs(self, targetcell, worldmap):
        start_cell = parent_cell = self.width, self.height
        distance = 0
        search_queue = {start_cell: {'distance_from_start': distance, 'parent': parent_cell}}
        visited_cells = {}

        while len(search_queue) > 0:
            if targetcell in search_queue:
                visited_cells[targetcell] = {'distance_from_start': distance, 'parent': parent_cell}
                search_queue.clear()
            else:
                new_search_scope = {}
                distance += 1
                for cell in search_queue:
                    visited_cells[cell] = search_queue[cell]
                    parent_cell = cell
                    adjacent_cells = self._find_adjacent_cells(cell)
                    if targetcell in adjacent_cells:
                        visited_cells[targetcell] = {'distance_from_start': distance, 'parent': parent_cell}
                        new_search_scope = {}
                        break

                    filtered_adjacent_cells = self._filter_empty_cells(adjacent_cells, worldmap)
                    new_cells_to_visit = list(
                        filter(lambda x: x not in visited_cells and x not in search_queue, filtered_adjacent_cells))
                    new_search_scope.update({new_cell: {'distance_from_start': distance, 'parent': parent_cell} for new_cell in
                                             new_cells_to_visit})
                search_queue.clear()
                search_queue.update(new_search_scope)

        else:
            current_cell = targetcell
            try:
                previous_cell_on_route = visited_cells[current_cell]['parent']
            except:
                print(current_cell, targetcell, start_cell, visited_cells[current_cell]['parent'])
            # выдает ошибку иногда
            while previous_cell_on_route != start_cell:
                current_cell = previous_cell_on_route
                previous_cell_on_route = visited_cells[current_cell]['parent']
            else:
                next_cell_using_bfs = current_cell
                return next_cell_using_bfs


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
        self._hp = self._maxhp

    def __repr__(self):
        if getattr(self, '_role', None):
            return f'\033[31m{self._role[:4]}, {self._hp}, {self._food_value}\033[0m'

    def consume(self, target_cell, worldmap):
        target = worldmap.worldpopulation[target_cell]

        if target._food_value - 1 >= 0:
            target._food_value -= 1
        else:
            target._food_value = 0
            target._is_to_be_deleted = 1

        if self._hp < self._maxhp:
            self._hp += 1




class Predator(Creature):
    """
    На что может потратить ход хищник:

    Переместиться (чтобы приблизиться к жертве - травоядному)
    Атаковать травоядное. При этом количество HP травоядного уменьшается на силу атаки хищника.
    Если значение HP жертвы опускается до 0, травоядное исчезает
    """
    collection = {'Tiger':
                      {'_speed': 6, '_maxhp': 500, '_attack_power': 10,
                       '_vision_radius': 10, '_food_value': 10, '_food_type': 'Herbivore'},
                  'Lion':
                      {'_speed': 4, '_maxhp': 700, '_attack_power': 10,
                       '_vision_radius': 10, '_food_value': 10, '_food_type': 'Herbivore'}}

    def __init__(self):
        super().__init__()


    def attack(self, target_cell, worldmap):
        target = worldmap.worldpopulation[target_cell]
        if not target.creature_state._is_under_attack:
            target.creature_state._is_under_attack = 1
        if target._hp > 0:
            target._hp -= self._attack_power
        if target._hp<= 0:
            target.creature_state._is_alive = 0


    def __repr__(self):
        if getattr(self, '_role', None):
            return f'\033[32m{self._role[:4]}, {self._hp}, {self.creature_state._is_hungry}\033[0m'

    def consume(self, target_cell, worldmap):
        target = worldmap.worldpopulation[target_cell]
        target._food_value = 0
        self.creature_state._is_hungry = 0
        self.creature_state.hungertimer.timer = 0

