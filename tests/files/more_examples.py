from tests.files.example import ThingTwo

class ThingThree():
    def baz(self):
        return ThingTwo.two()
    def call_cycle(self):
        ContainsCycle().zed()

class ContainsCycle():
    def zed(self):
        ThingThree().call_cycle()
    

