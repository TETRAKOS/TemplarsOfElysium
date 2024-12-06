import Entities

def get_distance_from_actors(actor1, actor2):
    if isinstance(actor1, Entities.Actor) and isinstance(actor2, Entities.Actor):
        distance_x = abs(actor1.pos[0] - actor2.pos[0])
        distance_y = abs(actor1.pos[1] - actor2.pos[1])
        actor_distance = max(distance_x, distance_y)
        return actor_distance