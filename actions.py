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
        occupied_coords = self._find_occupied_coords(worldmap)
        for entity_coords in occupied_coords:
            entity = worldmap.worldpopulation[entity_coords]
            entity.make_move(worldmap)

    @staticmethod
    def _find_occupied_coords(worldmap):
        occupied_coords = list(filter(lambda x: worldmap.worldpopulation[x] is not None, worldmap.worldpopulation))
        return occupied_coords



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