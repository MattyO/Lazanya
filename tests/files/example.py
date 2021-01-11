class ThingTwo():
    def two():
        return "foo"

class Example():
    def something(self):
        return 0

    def somethingelse(self):
        three = 'bar'
        self.takes_params(self.something())
        ThingTwo().two()

    def takes_params(self, value):
        return 3


def start():
    return Example().somethingelse()
