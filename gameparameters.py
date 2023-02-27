class GameParameters:
    """This class defines the simulation parameters"""
    mapwidth = 30
    mapheight = 15
    maparea = mapwidth * mapheight

    # is used to regulate map population
    entities = {'Water': int(0.05 * maparea), 'Grass': int(0.1 * maparea), 'Obstacle': int(0.1 * maparea),
                'Herbivore': 5, 'Predator': 2}

    # is used to trigger map refill
    entities_min_threshold = {'Grass': int(entities['Grass'] * 0.5),
                              'Herbivore': int(entities['Herbivore'] * 0.5),
                              'Predator': int(entities['Predator'] * 0.5)}
