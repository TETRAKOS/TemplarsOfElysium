import pygame
import Entities

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
    def __init__(self,player_ref):
        super().__init__()
        self.player_ref = player_ref
        self.damage = 0
        self.range = 0
    def attack(self, actor):
        pass
class RangedWeapon(Weapon):
    def __init__(self,player_ref):
        super().__init__(player_ref)
        self.range = 6
        self.damage = 2
        self.ammo = 2
        self.max_ammo = 2
        self.name = "ranged Weapon"
        self.icon = "Assets/Sprites/Items/Weapons/surv_gun.png"
    def attack(self, actor):
        self.fire_at(actor)
    def fire_at(self, enemy):
        if self.ammo > 0:
            self.ammo -= 1
            enemy.take_damage(self.damage)
            print(f"Fired at {enemy.name} for {self.damage} damage!")
            if isinstance(self.player_ref, Entities.Player):
                self.player_ref.pass_turn()
        else:
            print("No ammo left!")
    def reload(self):
        self.ammo = self.max_ammo
        print("Reloaded!")
        if isinstance(self.player_ref, Entities.Player):
            self.player_ref.pass_turn()
class surv_pistol(RangedWeapon):
    def __init__(self,player_ref):
        super().__init__(player_ref)
        self.damage = 1
        self.range = 4
        self.ammo = 2
        self.name = "Survival Pistol"
        self.icon = "Assets/Sprites/Items/Weapons/surv_gun.png"
class shard(Item):
    def __init__(self):
        super().__init__()
        self.name = "Shard"
        self.description = "A shard of unknown metal."
        self.icon = pygame.image.load("Assets/Sprites/Items/Materials/Shard/Shard.png")