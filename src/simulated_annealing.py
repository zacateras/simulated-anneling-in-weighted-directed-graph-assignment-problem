import time


class SimulatedAnnealing:

    def __init__(self, instance):
        pass

    def execute(self):
        start_time = time.time()

        while self.check_stop_condition():
            yield

        end_time = time.time()

        total_time = end_time - start_time
        pass

    def check_stop_condition(self):
        pass


