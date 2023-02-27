🧭 Simulation

So this is Simulation. my first attempt within OOP paradigm.

It uses:
- tkinter to implement GUI
- breadth-first search algorithm 🥕 for creatures to find theit shortest path to food
- some lengthy variable and method names

Gameparameters can be defined separately in GameParameters module, including:
- map width and height
- game speed
- creatures populations and
- minimum threshold for creatures' respawn

🐱‍🐉🐰
Creatures' behaviour:
Creatures either move, or attack/consume food.
Basically, herbivores are to be killed before consumption.
Hunger mechanism is implemented for predators - they do not hunt if not hungry.
Creatures have vision radius, so they won't hunt food which they don'see(they will then roam randomly till they see food).
But when food is spotted, creatures will establish their shortest path to food, taking into account obstacles on the way, and the probability that there is no path to target(in this case, again, creature will make a random move).

Thanks for reading this, peace.