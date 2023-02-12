class CreatureState:

    def __init__(self):
        self.is_hungry = 1
        self.is_thirsty = 1
        self.is_fleeing = 0
        self.is_attacking = 0
        self.is_alive = 1
        self.is_a_threat = 0  # this is only overruled for Predators in Predator Class