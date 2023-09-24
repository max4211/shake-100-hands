from manim import *
from copy import deepcopy

TOTAL_PEOPLE = 10
TOTAL_POINTS = TOTAL_PEOPLE * 2
MIDPOINT = int(TOTAL_POINTS / 2)
QUARTER = int(TOTAL_POINTS / 4)
Y_MAX = 0.5
Y_MIN = -0.5
FOCUS_POINT_INDEX = 0

def get_x(idx):
    if idx < MIDPOINT:
        return (QUARTER - 1) - idx
    elif idx == MIDPOINT - 1:
        return -(QUARTER - 0.5)
    elif idx == TOTAL_POINTS - 1:
        return QUARTER - 0.5
    elif idx >= MIDPOINT:
        return -(QUARTER - 1) + (idx - MIDPOINT)
    else:
        raise Exception(f"unhandled case in get_x for idx={idx}")
    
def get_y(idx):
    if (idx + 1) % MIDPOINT == 0:
        return 0
    elif idx < MIDPOINT:
        return Y_MAX
    elif idx >= MIDPOINT:
        return Y_MIN
    else:
        raise Exception(f"unhandled case in get_x for idx={idx}")

def get_z(idx):
    return 0

class MyPoint():
    def set_x(self):
        next_x = get_x(self.idx)
        self.x_shift = next_x - self.x
        self.x = next_x

    def set_y(self):
        next_y = get_y(self.idx)
        self.y_shift = next_y - self.y
        self.y = next_y

    def set_z(self):
        next_z = get_z(self.idx)
        self.z_shift = next_z - self.z
        self.z = next_z

    def set_coordinates(self):
        self.set_x()
        self.set_y()
        self.set_z()

    def location(self):
        return [self.x, self.y, self.z]
    
    def translation(self):
        return [self.x_shift, self.y_shift, self.z_shift]

    def __init__(self, idx):
        self.start_idx = idx
        self.idx = idx
        self.color = WHITE if self.idx % 2 == 0 else BLACK
        self.radius = 0.1 # 0.15 if idx == FOCUS_POINT_INDEX else 0.1
        self.x = get_x(idx)
        self.y = get_y(idx)
        self.z = get_z(idx)
        self.dot = Dot(point=self.location(), radius=self.radius, color=self.color)

    def update(self):
        self.idx =  (self.idx + 1) % TOTAL_POINTS
        self.set_coordinates()

    def __str__(self):
        return f"{self.idx} {self.location()}"
    
    # CR masmith: resolve this, does not work
    def is_above(self, p2):
        return (self.x == p2.x) and (self.idx != p2.idx)

MY_POINTS = [MyPoint(idx) for idx in range(TOTAL_POINTS)]

class HundredPoints(Scene):
    def construct(self):
        # keep track of hands shaken
        hands_shaken = DecimalNumber(0, num_decimal_places=0, include_sign=False, unit="  hands shaken")
        hands_shaken_tracker = ValueTracker(0)
        hands_shaken.add_updater(lambda d: d.set_value(hands_shaken_tracker.get_value()))
        hands_shaken.shift([0, 2, 0]).set_fill(GREEN_B)
        self.add(hands_shaken)

        # add a heading with experiment
        total_people = Text(f'{TOTAL_PEOPLE} total people')
        total_people.shift([0, 3, 0]).set_fill(BLUE_B)
        self.add(total_people)

        # iterate over all points
        first_point = MY_POINTS[0]
        for point in MY_POINTS:
            self.add(point.dot)
        self.wait(0.5)
        self.play(first_point.dot.animate.set_fill(RED_B))
        self.play(first_point.dot.animate.scale(2))
        self.play(first_point.dot.animate.scale(0.5))
        self.wait(0.5)
        for _ in range(TOTAL_PEOPLE - 1):
            # first see who is shaking hands
            animations = []
            for point in MY_POINTS:
                if point.is_above(first_point):
                    animations.append(point.dot.animate.set_fill(GREEN))
                    animations.append(hands_shaken_tracker.animate.increment_value(1))
            if animations:
                self.play(*animations)
                self.wait(0.1)
            animations = []
            # now update position for next round
            for point in MY_POINTS:
                point.update()
                animations.append(point.dot.animate.shift(point.translation()))
            if animations:
                self.play(*animations)
                self.wait(0.1)
        self.wait(0.5)