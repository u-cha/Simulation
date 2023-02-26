from random import randint, choice
from os import system as os
from platform import system as platform
from time import sleep


from tkinter import *
from tkinter import ttk

from gameparameters import GameParameters as gameparams
from actions import Actions


class Simulation:

    def __init__ (self, gameparams):
        self.worldmap = Simulation.Map(gameparams.mapwidth, gameparams.mapheight, gameparams.entities)
        self.renderer = Simulation.Renderer()
        self.counter = Simulation.Counter()
        self.actions = Actions()
        self.gameparams = gameparams
        self.on_pause = True




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
        def __init__(self, *args) -> None:
            self.window = Tk()
            self.window.title('Simulation')
            self.pause_button = self.create_pause_button()
            self.finish_button = self.create_finish_button()
            self.on_pause = True

        # def render(self, map, gameparams):
        #     clear = lambda: os('cls') if platform() == 'Windows' else os('clear')
        #     clear()
        #     for width in range(map.mapwidth):
        #         for height in range(map.mapheight):
        #             image = map.worldpopulation.get((width, height))
        #             print('\033[;;47m  \033[0;0;m' if image is None else image, end='')
        #         print()
        #
        #     print('\n' * 3)
        #
        #     for entityname in gameparams.entities.keys():
        #         num = getattr(map, f'count_entities.{entityname}')
        #         print(f'{entityname}: {num}')
        #     print(f'COUNTER: {game.counter.counter_current_state}')

        def create_pause_button(self):
            buttonframe = ttk.Frame(self.window, padding=10)
            buttonframe.grid(column=0, row=1)
            button = ttk.Button(buttonframe, text='Start', command=self.trigger_pause)
            button.grid(column=0, row=0)
            return button

        def create_finish_button(self):
            buttonframe = ttk.Frame(self.window, padding=10)
            buttonframe.grid(column=0, row=3)
            button = ttk.Button(buttonframe, text='Exit', command=self.exit)
            button.grid(column=0, row=0)
            return button

        def exit(self):
            self.window.destroy()
            exit()
        def trigger_pause(self):
            if self.on_pause:
                self.on_pause = False
                self.pause_button.configure(text='Pause')
            else:
                self.on_pause = True
                self.pause_button.configure(text='Resume')

        def update(self):

            game.make_a_turn()
            self.window.update()
            self.window.after(500, self.update)

        def render_gui_initial(self, map, gameparams):
            mainframe = ttk.Frame(self.window, padding=30)
            mainframe.grid(column=0, row=0)

            for width in range(map.mapwidth):
                for height in range(map.mapheight):

                    obj = map.worldpopulation[(width, height)]
                    widget = ttk.Label(mainframe, background=self.colordict[obj.__class__.__name__], text='   ')
                    widget.grid(column=width, row=height)
                    self.widgetsdict.update({(width, height): widget})
            self.update()
            self.window.mainloop()
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
        self.renderer.render_gui_initial(self.worldmap, self.gameparams)
        self.make_a_turn()



    def make_a_turn(self):
        """nextTurn() - просимулировать и отрендерить один ход"""

        turnactions = [getattr(self.actions.turnactions, action) for action in self.actions.turnactionsdict]
        for action in turnactions:
            action(gameparams, self.worldmap)
        self.renderer.render_gui_update(game.worldmap, gameparams)


    def pause_simulation(self):

            pass

if __name__ == '__main__':

    game = Simulation(gameparams)
    game.start_simulation()


