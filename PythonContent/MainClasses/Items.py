import pygame
import Entities
import time
import Utils
import random

class Item:
    def __init__(self):
        self.name = "Unknown"
        self.description = "No description provided."
        self.icon = None
    def call_menu(self, inventory_ref):
        pass
    def use(self, inventory_ref):
       # inventory_ref.remove_item(self)
        print(f"Can't use {self.name}!")
        return False

class Material(Item):
    def __init__(self):
        super().__init__()
        self.name = "Material"

class Weapon(Item):
    def __init__(self, player_ref):
        super().__init__()
        self.player_ref = player_ref
        self.damage = 0
        self.range = 0

    def attack(self, actor):
        pass

class RangedWeapon(Weapon):
    def __init__(self, player_ref):
        super().__init__(player_ref)
        self.range = 6
        self.damage = 2
        self.ammo = 2
        self.max_ammo = 2
        self.name = "ranged Weapon"
        self.icon = "Assets/Sprites/Items/Weapons/surv_gun.png"
        self.accuracy = 100
        pygame.mixer.init()

    def calculate_hit_chance(self, distance):
        return max(0, self.accuracy - (distance * 10))

    def attack(self, actor):
        self.fire_at(actor)
        self.player_ref.pass_turn()

    def fire_at(self, enemy):
        distance = Utils.get_distance_from_actors(self.player_ref, enemy)
        hit_chance = self.calculate_hit_chance(distance)
        if self.ammo > 0:
            self.ammo -= 1
            if random.randint(1, 100) <= hit_chance:
                enemy.take_damage(self.damage)
                print(f"Fired at {enemy.name} for {self.damage} damage!")
            else:
                pygame.mixer.music.load('Assets/Sound/sfx/smallarms_fire/sm1.wav')
                pygame.mixer.music.play()
                print("missed")
                if isinstance(self.player_ref, Entities.Player):
                    return None  # Indicate a miss
            pygame.mixer.music.load('Assets/Sound/sfx/smallarms_fire/sm1.wav')
            pygame.mixer.music.play()
            if isinstance(self.player_ref, Entities.Player):
      #         self.player_ref.pass_turn()
                return enemy.pos  # Return the position of the hit

        else:
            print("no ammo!")
            return None  # Indicate a miss

    def reload(self):
        self.ammo = self.max_ammo
        print("Reloaded!")
        pygame.mixer.music.load("Assets/Sound/sfx/small_reload/smReload.wav")
        pygame.mixer.music.play()
        if isinstance(self.player_ref, Entities.Player):
            self.player_ref.pass_turn()

class surv_pistol(RangedWeapon):
    def __init__(self, player_ref):
        super().__init__(player_ref)
        self.damage = 1
        self.range = 4
        self.ammo = 2
        self.name = "Survival Pistol"
        self.icon = "Assets/Sprites/Items/Weapons/surv_gun.png"

class smg(RangedWeapon):
    def __init__(self, player_ref):
        super().__init__(player_ref)
        self.damage = 2
        self.range = 10
        self.ammo = 30
        self.max_ammo = 30
        self.name = "SMG"
        self.icon = "Assets/Sprites/Items/Weapons/smg.png"
    def attack(self, actor):
        for i in range(3):
            self.fire_at(actor)
            pygame.mixer.music.load('Assets/Sound/sfx/smallarms_fire/sm1.wav')
            pygame.mixer.music.play()
            time.sleep(0.075)
        self.player_ref.pass_turn()

class Shard(Item):
    def __init__(self):
        super().__init__()
        self.name = "Metal shard"
        self.description = "A shard of unknown metal."
        self.icon = pygame.image.load("Assets/Sprites/Items/Materials/Shard/Shard.png")
class Cells(Item):
    def __init__(self):
        super().__init__()
        self.name = "Cells"
        self.description = "A collection of powercells."
        self.icon = pygame.image.load("Assets/Sprites/Items/Materials/Shard/cells.png")
class Box(Item):
    def __init__(self):
        super().__init__()
        self.name = "Polygel box"
        self.description = "A container with polygel."
        self.icon = pygame.image.load("Assets/Sprites/Items/Materials/Shard/box.png")
class MediPatch(Item):
    def __init__(self):
        super().__init__()
        self.name = "MediPatch"
        self.description = "A kit to restore small amount health."
        self.icon = pygame.image.load("Assets/Sprites/Items/Medical/mediPatch.png")
    def use(self, inventory_ref):
        inventory_ref.actor_ref.health.heal(25)
        inventory_ref.remove_item(self)
        print(f"Healed with {self.name} by 25 HP!")
        return True
class MedInjector(Item):
    def __init__(self):
        super().__init__()
        self.name = "Medical Injector"
        self.description = "A syringe filled with life-saving chemicals"
        self.icon = pygame.image.load("Assets/Sprites/Items/Medical/Injector.png")
    def use(self, inventory_ref):
        inventory_ref.actor_ref.health.heal(50)
        inventory_ref.remove_item(self)
        print(f"Healed with {self.name} by 50 HP!")
        return True