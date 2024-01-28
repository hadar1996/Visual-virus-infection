STATE_VACCINATED = 1
STATE_SICK = 2
STATE_HEALTHY = 3
STATE_TO_STRING = {STATE_VACCINATED: "Vaccinated", STATE_SICK: "Sick", STATE_HEALTHY: "Healthy"}
STATE_TO_COLOR = {STATE_VACCINATED: (127, 255, 0), STATE_SICK: (220, 60, 20), STATE_HEALTHY: (0, 0, 255)}


class Human:
    def __init__(self, start_index, state):
        """

        :param start_index:
        :type: C{tuple}
        :param state:
        :type: C{int}
        """
        self.start_index = start_index
        self.current_index = start_index
        self.state = state
        self.t = 0

    def get_color(self):
        return STATE_TO_COLOR[self.state]

    def __str__(self):
        return "Human state {} and in index: {}".format(STATE_TO_STRING[self.state], self.current_index)
