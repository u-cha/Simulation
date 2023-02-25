from random import randint, choice
from os import system as os
from platform import system as platform
from time import sleep
import threading

import keyboard

from tkinter import *
from tkinter import ttk

from gameparameters import GameParameters as gameparams
from actions import Actions


class Simulation:

    def __init__ (self, *args, **kwargs):
        self.worldmap = Simulation.Map(gameparams.mapwidth, gameparams.mapheight, gameparams.entities)
        self.renderer = Simulation.Renderer()
        self.counter = Simulation.Counter()
        self.actions = Actions()


    class Map:

        def __init__(self, mapwidth, mapheight, *args, **kwargs):
            self.mapwidth = mapwidth
            self.mapheight = mapheight
            self.worldpopulation = self.__form_free_cells()
            self.cells_to_redraw = []
            for entityname in gameparams.entities.keys():
                setattr(self, f'count_entities.{entityname}', 0)

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
        colordict = {'NoneType':'white', 'Grass':'green', 'Obstacle':'black',
                     'Water':'blue', 'Herbivore':'yellow', 'Predator':'red'}
        widgetsdict = {}


        def render(self, map, gameparams):
            clear = lambda: os('cls') if platform() == 'Windows' else os('clear')
            clear()
            for width in range(map.mapwidth):
                for height in range(map.mapheight):
                    image = map.worldpopulation.get((width, height))
                    print('\033[;;47m  \033[0;0;m' if image is None else image, end='')
                print()

            print('\n' * 3)

            for entityname in gameparams.entities.keys():
                num = getattr(map, f'count_entities.{entityname}')
                print(f'{entityname}: {num}')
            print(f'COUNTER: {game.counter.counter_current_state}')

        def render_gui_initial(self, map, gameparams):

            for width in range(map.mapwidth):
                for height in range(map.mapheight):

                    obj = map.worldpopulation[(width, height)]
                    widget = ttk.Label(mainframe, background=self.colordict[obj.__class__.__name__], text='   ')
                    widget.grid(column=width, row=height)
                    self.widgetsdict.update({(width, height): widget})

            buttonframe = ttk.Frame(window, padding=30)
            buttonframe.grid(column=0, row=1)
            button = ttk.Button(buttonframe, text='Play').grid(column=gameparams.mapwidth//2,row=0)

        def render_gui_update(self, map, gameparams):
            for i in range(len(map.cells_to_redraw)):
                width, height = map.cells_to_redraw.pop()
                obj = map.worldpopulation[(width, height)]
                self.widgetsdict[(width, height)].configure(background=self.colordict[obj.__class__.__name__])




    def start_simulation(self):
        """startSimulation() - запустить бесконечный цикл симуляции и рендеринга"""
        start_actions = [getattr(self.actions.initactions, action) for action in self.actions.initactionslist]
        for action in start_actions:
            action(gameparams, self.worldmap)
        self.renderer.render_gui_initial(game.worldmap, gameparams)


    def make_a_turn(self):
        """nextTurn() - просимулировать и отрендерить один ход"""
        turnactions = [getattr(self.actions.turnactions, action) for action in self.actions.turnactionsdict]
        for action in turnactions:
            action(gameparams, self.worldmap)
        self.renderer.render_gui_update(game.worldmap, gameparams)

    def pause_simulation(self):
        global game_is_running
        while environment_is_running:
            if keyboard.is_pressed('c'):
                if main_is_running:
                    main_is_running.clear()
            if keyboard.is_pressed('f'):
                main_is_running.set()
            if keyboard.is_pressed('l'):
                main_is_running.set()
                environment_is_running = False
        else:
            pass

if __name__ == '__main__':
    def update():
        game.make_a_turn()
        window.update()
        window.after(500, update)

    window = Tk()
    window.title('Simulation')
    mainframe = ttk.Frame(window, padding=30)
    mainframe.grid(column=0, row=0)
    colordict = {'Grass': 'green', 'Obstacle': 'grey', 'Water': 'blue',
                 'Predator': 'red', 'Herbivore': 'yellow', 'NoneType': 'white'}

    game = Simulation()
    game.start_simulation()
    update()
    window.mainloop()


