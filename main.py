from os import listdir
import time
from random import randint, choice

from tkinter import *
from tkinter import ttk

from gameparameters import GameParameters as gameparams
from actions import Actions


class Simulation:

    def __init__(self, gameparams):
        self.worldmap = Simulation.Map(gameparams.mapwidth, gameparams.mapheight, gameparams.entities)
        self.counter = Simulation.Counter()
        self.stats =None
        self.actions = Actions()
        self.gameparams = gameparams
        self.endgame = False
        self.on_pause = True
        self.sim_window = self.create_window()
        self.renderer = Simulation.Renderer()


    def create_window(self):
        self.buttonsdict = {}
        sim_window = Tk()
        sim_window.title('Simulation2')
        self.create_buttons(sim_window)
        return sim_window

    def create_buttons(self, screen):
        buttons = {'Start': self.trigger_pause, 'Exit': self.exit}
        row = 2
        for name, function in buttons.items():
            buttonframe = ttk.Frame(screen, padding=10)
            buttonframe.grid(column=0, row=row)
            button = ttk.Button(buttonframe, name=name.lower(), text=name, command=function)
            button.grid(column=0, row=0)
            self.buttonsdict.update({f'{name}': button})
            row += 1



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
            self.worldpopulation = self.form_free_cells()
            self.cells_to_redraw = []
            for entityname in gameparams.entities.keys():
                setattr(self, f'count_entities.{entityname}', 0)

        def form_free_cells(self):
            worldfreecells = {}
            for width in range(self.mapwidth):
                for height in range(self.mapheight):
                    worldfreecells[(width, height)] = None
            return worldfreecells



    class Counter:
        def __init__(self, *args) -> None:
            self.counter_current_state = 0


        def make_one_tick(self):
            self.counter_current_state += 1

    class Renderer:
        colordict = {'NoneType': 'white', 'Grass': 'green', 'Obstacle': 'black',
                     'Water': 'blue', 'Herbivore': 'yellow', 'Predator': 'red'}
        widgetsdict = {}

        def __init__(self, *args) -> None:
            self.imagedict = self.load_images()

        def load_images(self):
            imagedict = {}
            imagefilenames = listdir('./images/')
            for filename in imagefilenames:
                imagedict.update({filename[:-4]: PhotoImage(file=f'images/{filename}')})
            return imagedict

        def render_gui_initial(self, worldmap, screen, stats):
            mainframe = ttk.Frame(screen, padding=30)
            mainframe.grid(column=0, row=0)

            for width in range(worldmap.mapwidth):
                for height in range(worldmap.mapheight):
                    obj = worldmap.worldpopulation[(width, height)]
                    widget = ttk.Label(mainframe, padding=0, image=self.imagedict.get(obj.__class__.__name__))
                    widget.grid(column=width, row=height)
                    self.widgetsdict.update({(width, height): widget})
            self.create_stats_display(screen, stats)

        def create_stats_display(self, screen, stats):
            statsframe = ttk.Frame(screen, padding=10)
            statsframe.grid(column=0, row=1)
            column = 0
            for stat in stats:

                statwidget = ttk.Label(statsframe, image=self.imagedict.get(stat))
                statwidget.grid(column=column, row=0)
                statlabel = ttk.Label(statsframe, text=stats[stat])
                self.widgetsdict.update({stat:statlabel})
                statlabel.grid(column=column, row=1)
                column +=1



        def render_gui_update(self, worldmap, stats):

            for i in range(len(worldmap.cells_to_redraw)):
                width, height = worldmap.cells_to_redraw.pop()
                obj = worldmap.worldpopulation[(width, height)]
                self.widgetsdict[(width, height)].configure(image=self.imagedict.get(obj.__class__.__name__))
            for stat in stats:
                self.widgetsdict[stat].configure(text=stats[stat])
    def start_simulation(self):

        start_actions = [getattr(self.actions.initactions, action) for action in self.actions.initactionslist]
        for action in start_actions:
            action(gameparams, self.worldmap)
        self.stats = self.calculate_stats()
        self.renderer.render_gui_initial(self.worldmap, self.sim_window, self.stats)

        self.make_a_turn()
        self.sim_window.mainloop()

    def make_a_turn(self):

        while True:
            if self.endgame:
                break
            if not self.on_pause:
                turnactions = [getattr(self.actions.turnactions, action) for action in self.actions.turnactionsdict]
                for action in turnactions:
                    action(gameparams, self.worldmap)
                self.counter.make_one_tick()
                self.stats = self.calculate_stats()
                self.renderer.render_gui_update(self.worldmap, self.stats)
                time.sleep(.3)

            self.sim_window.update()

    def calculate_stats(self):
        count_predators = len(
            list(filter(lambda x: self.worldmap.worldpopulation[x].__class__.__name__ == 'Predator', self.worldmap.worldpopulation)))
        count_herbivores = len(
            list(filter(lambda x: self.worldmap.worldpopulation[x].__class__.__name__ == 'Herbivore', self.worldmap.worldpopulation)))
        counter_state = self.counter.counter_current_state
        return {'Predator':count_predators, 'Herbivore':count_herbivores, 'Counter':counter_state}



if __name__ == '__main__':
    game = Simulation(gameparams)
    game.start_simulation()
