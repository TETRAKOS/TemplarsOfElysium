import pygame

class Item:
    def __init__(self):
        self.name = "Unknown"
        self.description = "No description provided."
        self.icon = None

class Material(Item):
    def __init__(self):
        super().__init__()
        self.name = "Material"
class Weapon(Item):
    def __init__(self):
        super().__init__()
        self.damage = 0
        self.range = 0
class RangedWeapon(Weapon):
    def __init__(self):
        super().__init__()
        self.range = 6
        self.damage = 2
        self.ammo = 2
        self.name = "ranged Weapon"
        self.icon = "Assets/Sprites/Items/Weapons/surv_gun.png"