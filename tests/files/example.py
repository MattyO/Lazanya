class ThingTwo():
    def two():
        return "foo"

class Example():
    blaaaa = 'blaaaaa'
    def something(self):
        def inside(param):
            def insideinside():
                return 'zed'
        return 0

    def somethingelse(self):
        three = 'bar'
        self.blaaaa
        self.takes_params(self.something())
        ThingTwo().two()

    def takes_params(self, value):
        return 3


def start():
    return Example().somethingelse()
