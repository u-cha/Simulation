from random import randint, choice
from gameparameters import GameParameters as gameparams


class Actions:

    def __init__(self):
        self.initactions = InitActions()
        self.turnactions = TurnActions()
        self.initactionslist = ['inhabit_map']
        # 'place_entities': self.init_actions.create_entities}
        self.turnactionsdict = ['entity_make_move']
        # ['check_creature_state', 'set_creature_state',
        #                'decide_what_to_do', 'do_it', 'check_map_enough_entities', 'create_entities',
        #                'place_entities']


class InitActions(Actions):
    def __init__(self):
        pass

    def create_entities(self, entitiesdic, entitiesclass):
        entitieslist = []
        for entity, number in entitiesdic.items():
            for _ in range(number):
                obj = entitiesclass.__dict__[entity]()
                entitieslist.append(obj)
        return entitieslist

    def choose_random_free_coordinates_on_map(self, worldmap):
        width = 0
        height = 0
        while worldmap.worldpopulation[width, height] != None:
            width = randint(0, gameparams.mapwidth - 1)
            height = randint(0, gameparams.mapheight - 1)
        return width, height

    def place_entities_on_map(self, worldmap, entitieslist):
        for entity in entitieslist:
            width, height = self.choose_random_free_coordinates_on_map(worldmap)
            worldmap.worldpopulation[width, height] = entity
            worldmap.worldpopulation[width, height].width = width
            worldmap.worldpopulation[width, height].height = height

    def inhabit_map(self, entitiesdic, entititiesclass, worldmap):
        entitieslist = self.create_entities(entitiesdic, entititiesclass)
        self.place_entities_on_map(worldmap, entitieslist)


class TurnActions(Actions):

    def __init__(self):
        pass

    def entity_make_move(self, worldmap):
        filteredcoords = list(filter(lambda x: worldmap.worldpopulation[x] is not None, worldmap.worldpopulation))
        for entitycoords in filteredcoords:
            entity = worldmap.worldpopulation[entitycoords]
            entity_name = entity.__class__.__name__

            if entity_name in ('Predator', 'Herbivore'):
                adjacent_cells = self.__find_adjacent_cells(entity)
                free_adjacent_cells = self.__filter_free_cells(adjacent_cells, worldmap)
                if len(free_adjacent_cells) == 0:
                    pass

                else:
                    next_cell = choice(free_adjacent_cells)
                    worldmap.worldpopulation[entitycoords] = None
                    worldmap.worldpopulation[next_cell] = entity
                    entity.width, entity.height = next_cell

            # elif
            #
            # else:
            #     pass

    @staticmethod
    def __find_adjacent_cells(obj):
        adjacent_cells = []
        for width in range(obj.width - 1, obj.width + 2):
            for height in range(obj.height - 1, obj.height + 2):
                if (width < 0 or height < 0
                        or width >= gameparams.mapwidth
                        or height >= gameparams.mapheight
                        or width == obj.width and height == obj.height):
                    pass
                else:
                    adjacent_cells.append((width, height))
        return adjacent_cells

    @staticmethod
    def __filter_free_cells(cells, worldmap):
        return list(filter(lambda x: worldmap.worldpopulation[x] == None, cells))


"""действия, совершаемые каждый ход. Примеры - передвижение существ,
добавить травы или травоядных, если их осталось слишком мало"""
pass

"""
Поиск пути
Советую писать алгоритм поиска пути полностью с нуля, 
используя в качестве источника описание алгоритма на википедии. 
Проще всего начать с алгоритма поиска в ширину. 
Он относительно простой в реализации, 
но может работать медленно на больших полях, 
для которых лучше подойдет алгоритм [A](https://ru.wikipedia.org/wiki/A).

"""