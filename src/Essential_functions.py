from Game_object import Game_object

def inside((x1, y1), (x2, y2, w, h)):
    return x2 <= x1 <= x2 + w and y2 <= y1 <= y2 + h

def collision(obj_1, obj_2):
    (x1, y1, w1, h1) = obj_1.wymiary()
    (x2, y2, w2, h2) = obj_2.wymiary()
    return not (x2 >= x1 + w1 or x2 + w2 <= x1 or y2 >= y1 + h1 or y2 + h2 <= y1)

def collision_with_many(obj, l):
    result = None
    for x in l:
        if collision(obj, x):
            result = add(result, x)
    return result

def get_collides_objects(obj, l):
    result = []
    for candidat in l:
        if collision(obj, candidat):
            result.append(candidat)
    return result

def add(obj_1, obj_2):
    if obj_1 is None:
        return obj_2
    if obj_2 is None:
        return obj_1
    min_x = min(obj_1.x, obj_2.x)
    max_x = max(obj_1.x + obj_1.w, obj_2.x + obj_2.w)
    min_y = min(obj_1.y, obj_2.y)
    max_y = max(obj_1.y + obj_1.h, obj_2.y + obj_2.h)
    return Game_object(min_x, min_y, max_x - min_x, max_y - min_y)

def area_sum(objects):
    return reduce(lambda obj_1, obj_2: add(obj_1, obj_2), objects, None)


