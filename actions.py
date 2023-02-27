from random import randint

from gameparameters import GameParameters as gameparams
import entity


class Actions:

    def __init__(self):
        self.initactions = InitActions()
        self.turnactions = TurnActions()
        self.initactionslist = ['inhabit_map', 'update_map_stats']
        self.turnactionsdict = ['entity_make_move', 'entity_update_self_status',
                                'clear_redundant_entities', 'spawn_new_entities', 'update_map_stats']


class InitActions(Actions):
    def __init__(self):
        pass

    def create_entities(self, gameparams):
        entitieslist = []
        for entityname, number in gameparams.entities.items():
            for _ in range(number):
                obj = entity.__dict__[entityname]()
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

    def inhabit_map(self, entitiesdic, worldmap):
        entitieslist = self.create_entities(entitiesdic)
        self.place_entities_on_map(worldmap, entitieslist)

    def update_map_stats(self, gameparams, worldmap):
        for entityname in gameparams.entities.keys():
            count_entities = 0
            for cell in worldmap.worldpopulation:
                if worldmap.worldpopulation[cell].__class__.__name__ == entityname:
                    count_entities += 1
            setattr(worldmap, f'count_entities.{entityname}', count_entities)


class TurnActions(Actions):

    def __init__(self):
        pass

    def entity_make_move(self, gameparams, worldmap):
        populated_coords = self._find_populated_coords(worldmap)
        for entity_coords in populated_coords:
            entity = worldmap.worldpopulation[entity_coords]
            entity.make_move(worldmap)

    @staticmethod
    def _find_populated_coords(worldmap):
        populated_coords = list(filter(lambda x: worldmap.worldpopulation[x] is not None, worldmap.worldpopulation))
        return populated_coords

    def entity_update_self_status(self, gameparams, worldmap):
        for cell, entity in worldmap.worldpopulation.items():
            if entity != None:
                entity.entity_update_self_status()

    def clear_redundant_entities(self, gameparams, worldmap):
        for cell, entity in worldmap.worldpopulation.items():
            if getattr(entity, '_is_to_be_deleted', 0) == 1:
                worldmap.worldpopulation[cell] = None
                worldmap.cells_to_redraw.append(cell)

    def create_additional_entities(self, entittiesdic, entities_min_threshold, worldmap):
        entitieslist = []
        for entityname in entittiesdic.keys():
            if entityname in entities_min_threshold.keys():
                count_entities = 0
                for cell in worldmap.worldpopulation:
                    if worldmap.worldpopulation[cell].__class__.__name__ == entityname:
                        count_entities += 1
                if count_entities < entities_min_threshold[entityname]:
                    number = entittiesdic[entityname] - count_entities
                    for _ in range(number):
                        obj = entity.__dict__[entityname]()
                        entitieslist.append(obj)
        return entitieslist

    def spawn_new_entities(self, gameparams, worldmap):
        entitieslist = self.create_additional_entities(gameparams.entities, gameparams.entities_min_threshold, worldmap)
        self.place_entities_on_map(worldmap, entitieslist)

    def place_entities_on_map(self, worldmap, entitieslist):
        for entity in entitieslist:
            width, height = self.choose_random_free_coordinates_on_map(worldmap)
            worldmap.worldpopulation[width, height] = entity
            worldmap.worldpopulation[width, height].width = width
            worldmap.worldpopulation[width, height].height = height
            worldmap.cells_to_redraw.append((width, height))

    def choose_random_free_coordinates_on_map(self, worldmap):
        width = 0
        height = 0
        while worldmap.worldpopulation[width, height] != None:
            width = randint(0, gameparams.mapwidth - 1)
            height = randint(0, gameparams.mapheight - 1)
        return width, height

    def update_map_stats(self, gameparams, worldmap):
        for entityname in gameparams.entities.keys():
            count_entities = 0
            for cell in worldmap.worldpopulation:
                if worldmap.worldpopulation[cell].__class__.__name__ == entityname:
                    count_entities += 1
            setattr(worldmap, f'count_entities.{entityname}', count_entities)


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
