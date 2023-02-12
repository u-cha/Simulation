class GameParameters:
    mapwidth = 20
    mapheight = 20
    maparea = mapwidth * mapheight

    # is used to regulate map population
    entities = {'Water': int(0.1 * maparea), 'Grass': int(0.1 * maparea), 'Obstacle': int(0.1 * maparea),
                'Herbivore': 5, 'Predator': 5}

    # is used to trigger map refill
    entities_min_threshold = {'Water': int(entities['Water'] * 0.5),
                              'Herbivore': int(entities['Herbivore'] * 0.5),
                              'Predator': int(entities['Predator'] * 0.5)}
