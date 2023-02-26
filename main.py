import time
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
        self.endgame = False
        self.on_pause = True
        self.sim_window = self.create_window()

    def create_window(self):
        self.buttonsdict = {}
        sim_window = Tk()
        sim_window.title('Simulation2')
        self.create_buttons(sim_window)
        self.create_stats_display(sim_window)
        return sim_window

    def create_buttons(self, screen):
        buttons = {'Start':self.trigger_pause, 'Exit':self.exit}
        row = 2
        for name, function in buttons.items():
            buttonframe = ttk.Frame(screen, padding=10)
            buttonframe.grid(column=0, row=row)
            button = ttk.Button(buttonframe, name=name.lower(), text=name, command=function)
            button.grid(column=0, row=0)
            self.buttonsdict.update({f'{name}':button})
            row += 1

    def create_stats_display(self, screen):
        statsframe = ttk.Frame(screen,padding= 10)
        statsframe.grid(column=0, row=1)
        stats = ttk.Label(statsframe, text="Stats")
        stats.grid(column=0, row=0)


    def trigger_pause(self):
        button = self.buttonsdict['Start']
        if self.on_pause:
            self.on_pause = False
            button.configure(text='Pause')
        else:
            self.on_pause = True
            button.configure(text='Resume')

    def exit(self):
        self.endgame = True
        self.sim_window.destroy()
        exit()

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
            pass



        def render_gui_initial(self, worldmap, screen):
            mainframe = ttk.Frame(screen, padding=30)
            mainframe.grid(column=0, row=0)

            for width in range(worldmap.mapwidth):
                for height in range(worldmap.mapheight):

                    obj = worldmap.worldpopulation[(width, height)]
                    widget = ttk.Label(mainframe, background=self.colordict[obj.__class__.__name__], text='   ')
                    widget.grid(column=width, row=height)
                    self.widgetsdict.update({(width, height): widget})

        def render_gui_update(self, worldmap):
            for i in range(len(worldmap.cells_to_redraw)):
                width, height = worldmap.cells_to_redraw.pop()
                obj = worldmap.worldpopulation[(width, height)]
                self.widgetsdict[(width, height)].configure(background=self.colordict[obj.__class__.__name__])


    def start_simulation(self):
        """startSimulation() - запустить бесконечный цикл симуляции и рендеринга"""
        start_actions = [getattr(self.actions.initactions, action) for action in self.actions.initactionslist]
        for action in start_actions:
            action(gameparams, self.worldmap)
        self.renderer.render_gui_initial(self.worldmap, self.sim_window)
        self.make_a_turn()
        self.sim_window.mainloop()


    def make_a_turn(self):
        """nextTurn() - просимулировать и отрендерить один ход"""
        while True:
            if self.endgame:
                break
            if not self.on_pause:
                turnactions = [getattr(self.actions.turnactions, action) for action in self.actions.turnactionsdict]
                for action in turnactions:
                    action(gameparams, self.worldmap)
                self.renderer.render_gui_update(self.worldmap)
                time.sleep(1)

            self.sim_window.update()


if __name__ == '__main__':

    game = Simulation(gameparams)
    game.start_simulation()


