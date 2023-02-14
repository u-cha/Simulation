from random import randint, choice
from os import system as os
from platform import system as platform
from time import sleep


from tkinter import *
from tkinter import ttk

from gameparameters import GameParameters as gameparams
from actions import Actions


class Simulation:

    def __init__ (self, *args, **kwargs):
        self.worldmap = Simulation.Map(gameparams.mapwidth, gameparams.mapheight)
        self.renderer = Simulation.Renderer()
        self.counter = Simulation.Counter()
        self.actions = Actions()


    class Map:

        def __init__(self, mapwidth, mapheight, *args, **kwargs):
            self.mapwidth = mapwidth
            self.mapheight = mapheight
            self.worldpopulation = self.__form_free_cells()
            self.count_predators, self.count_herbivores = self.__count_preds_and_herbs()


        def __form_free_cells(self):
            worldfreecells = {}
            for width in range(self.mapwidth):
                for height in range(self.mapheight):
                    worldfreecells[(width, height)] = None
            return worldfreecells

        def __count_preds_and_herbs(self):
            count_predators = len(list(filter(lambda x: self.worldpopulation[x].__class__.__name__ == 'Predator', self.worldpopulation)))
            count_herbivores = len(list(filter(lambda x: self.worldpopulation[x].__class__.__name__ == 'Herbivore', self.worldpopulation)))
            return count_predators, count_herbivores


        #TODO починить счетчик
        # предусмотреть обновление этого счетчика после каждого хода



    class Counter:
        def __init__(self, *args) -> None:
            self.counter_current_state = 0

        def __make_one_tick(self):
            self.counter_current_state += 1


    class Renderer:

        def render(self, map):
            clear = lambda: os('cls') if platform() == 'Windows' else os('clear')
            clear()
            for width in range(map.mapwidth):
                for height in range(map.mapheight):
                    image = map.worldpopulation.get((width, height))
                    print('    ' if image is None else image, end=' ')
                print()

            print('\n' * 3)
            print(f'Herbs {map.count_herbivores} , Predators {map.count_predators}')

        def render_gui(self, map):
            window = Tk()
            window.title('Simulation')
            mainframe = ttk.Frame(window, padding=30)
            mainframe.grid(column=0, row=0)
            colordict = {'Grass': 'green', 'Obstacle': 'grey', 'Water':'blue',
                         'Predator':'red', 'Herbivore': 'yellow', 'NoneType':'white'}

            for width in range(map.mapwidth):
                for height in range(map.mapheight):

                    obj = map.worldpopulation[(width, height)]
                    ttk.Label(mainframe, text='   ', background=colordict[obj.__class__.__name__]).grid(column=width, row=height)

            window.mainloop()

    def start_simulation(self):
        """startSimulation() - запустить бесконечный цикл симуляции и рендеринга"""
        start_actions = [getattr(self.actions.initactions, action) for action in self.actions.initactionslist]
        for action in start_actions:
            action(gameparams.entities, self.worldmap)
        self.renderer.render(game.worldmap)


    def make_a_turn(self):
        """nextTurn() - просимулировать и отрендерить один ход"""
        turnactions = [getattr(self.actions.turnactions, action) for action in self.actions.turnactionsdict]
        for action in turnactions:
            action(self.worldmap)
        self.renderer.render(game.worldmap)

    def pause_simulation(self):
        """pauseSimulation() - приостановить бесконечный цикл симуляции и рендеринга"""
        pass


if __name__ == '__main__':

    game = Simulation()
    game.start_simulation()

    print()
    for i in range(100):
        game.make_a_turn()
        sleep(1)












