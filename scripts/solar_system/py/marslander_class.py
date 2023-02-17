from dataclasses import dataclass


#marslanderSpecs = { 'length': 6, 'width': 1.56, 'weight': 360, 'deckHeight': (83, 108), 'robotArmLength': 1.8, 'numberOfSolarPanels': 2}

@dataclass
class Marslander:
    length: int = 6
    width: float = 1.56
    weight: int = 360
    deckHeight: tuple = (83,108)
    robotArmLength: float = 1.8
    numberOfSolarPanels: int = 2



new_lander = Marslander(8, 2.3, 500, (120,208), 3.4, 5)






