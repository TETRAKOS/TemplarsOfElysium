import pygame
import Entities
import time
import Utils
import random

class Item:
    def __init__(self, player_ref=None):
        self.name = "Unknown"
        self.description = "No description provided."
        self.icon = None
        self.player_ref = player_ref

    def call_menu(self, inventory_ref):
        pass

    def use(self, inventory_ref):
        print(f"Can't use {self.name}!")
        return False

class Material(Item):
    def __init__(self, player_ref=None):
        super().__init__(player_ref)
        self.name = "Material"

class Weapon(Item):
    def __init__(self, player_ref):
        super().__init__(player_ref)
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
        self.sound = None
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
                if self.sound is not None:
                    pygame.mixer.music.load(self.sound)
                else:
                    pygame.mixer.music.load('Assets/Sound/sfx/smallarms_fire/sm1.wav')
                pygame.mixer.music.play()
                print("missed")
                if isinstance(self.player_ref, Entities.Player):
                    return None
            if self.sound is not None:
                pygame.mixer.music.load(self.sound)
            else:
                pygame.mixer.music.load('Assets/Sound/sfx/smallarms_fire/sm1.wav')
            pygame.mixer.music.play()
            if isinstance(self.player_ref, Entities.Player):
                return enemy.pos
        else:
            print("no ammo!")
            return None

    def reload(self):
        self.ammo = self.max_ammo
        print("Reloaded!")
        pygame.mixer.music.load("Assets/Sound/sfx/small_reload/smReload.wav")
        pygame.mixer.music.play()
        if isinstance(self.player_ref, Entities.Player):
            self.player_ref.pass_turn()

class Surv_pistol(RangedWeapon):
    def __init__(self, player_ref):
        super().__init__(player_ref)
        self.damage = 1
        self.range = 6
        self.ammo = 2
        self.name = "Survival Pistol"
        self.icon = "Assets/Sprites/Items/Weapons/surv_gun.png"

class Shotgun(RangedWeapon):
    def __init__(self, player_ref):
        super().__init__(player_ref)
        self.damage = 6
        self.range = 4
        self.ammo = 4
        self.max_ammo = 4
        self.name = "Shotgun"
        self.icon = "Assets/Sprites/Items/Weapons/shotgun.png"

class Pistol(RangedWeapon):
    def __init__(self, player_ref):
        super().__init__(player_ref)
        self.damage = 2
        self.range = 8
        self.ammo = 10
        self.max_ammo = 10
        self.name = "Pistol"
        self.icon = "Assets/Sprites/Items/Weapons/pistol.png"

class Laser(RangedWeapon):
    def __init__(self, player_ref):
        super().__init__(player_ref)
        self.damage = 4
        self.range = 10
        self.ammo = 32
        self.max_ammo = 32
        self.name = "Laser"
        self.icon = "Assets/Sprites/Items/Weapons/laser.png"
        self.sound = "Assets/Sound/sfx/laser/fire.wav"

    def attack(self, actor):
        for i in range(6):
            self.fire_at(actor)
            time.sleep(0.1)
        self.player_ref.pass_turn()

class Smg(RangedWeapon):
    def __init__(self, player_ref):
        super().__init__(player_ref)
        self.damage = 1
        self.range = 5
        self.ammo = 30
        self.max_ammo = 30
        self.name = "SMG"
        self.icon = "Assets/Sprites/Items/Weapons/smg.png"

    def attack(self, actor):
        for i in range(3):
            self.fire_at(actor)
            time.sleep(0.075)
        self.player_ref.pass_turn()

class Shard(Item):
    def __init__(self, player_ref=None):
        super().__init__(player_ref)
        self.name = "Metal shard"
        self.description = "A shard of unknown metal."
        self.icon = pygame.image.load("Assets/Sprites/Items/Materials/Shard/Shard.png")

class Cells(Item):
    def __init__(self, player_ref=None):
        super().__init__(player_ref)
        self.name = "Cells"
        self.description = "A collection of powercells."
        self.icon = pygame.image.load("Assets/Sprites/Items/Materials/Shard/cells.png")

class Box(Item):
    def __init__(self, player_ref=None):
        super().__init__(player_ref)
        self.name = "Polygel box"
        self.description = "A container with polygel."
        self.icon = pygame.image.load("Assets/Sprites/Items/Materials/Shard/box.png")

class MediPatch(Item):
    def __init__(self, player_ref=None):
        super().__init__(player_ref)
        self.name = "MediPatch"
        self.description = "A kit to restore small amount health."
        self.icon = pygame.image.load("Assets/Sprites/Items/Medical/mediPatch.png")

    def use(self, inventory_ref):
        inventory_ref.actor_ref.health.heal(25)
        inventory_ref.remove_item(self)
        print(f"Healed with {self.name} by 25 HP!")
        return True

class MedInjector(Item):
    def __init__(self, player_ref=None):
        super().__init__(player_ref)
        self.name = "Medical Injector"
        self.description = "A syringe filled with life-saving chemicals"
        self.icon = pygame.image.load("Assets/Sprites/Items/Medical/Injector.png")

    def use(self, inventory_ref):
        inventory_ref.actor_ref.health.heal(50)
        inventory_ref.remove_item(self)
        print(f"Healed with {self.name} by 50 HP!")
        return True
