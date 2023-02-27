class CreatureState:

    def __init__(self):
        self._is_hungry = 1
        self._is_attacking = 0
        self._is_chasing = 0
        self._is_alive = 1
        self._is_being_consumed = 0
        self._is_under_attack = 0
        self.hungertimer = HungerTimer()

class HungerTimer:
    def __init__(self):
        self.timer = 0

    def tick(self):
        if self.timer < 10:
            self.timer += 1