#import math
import numpy

# def draw_radial_gradient(screen, color1, color2):
#     for y in range(screen.get_height()):
#         for x in range(screen.get_width()):
#             dx = x - screen.get_width() // 2
#             dy = y - screen.get_height() // 2
#             distance = math.sqrt(dx*dx + dy*dy)
#             max_distance = math.sqrt((screen.get_width()//2)**2+(screen.get_height()//2)**2)
#             ratio = distance / max_distance
#             ratio = min(ratio, 1)
#             r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
#             g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
#             b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
#             screen.set_at((x, y), (r, g, b))
def generate_gradient(from_color, to_color, height, width):
    channels = []
    for channel in range(3):
        from_value, to_value = from_color[channel], to_color[channel]
        channels.append(
            numpy.tile(
                numpy.linspace(from_value, to_value, width), [height, 1],
            ),
        )
    return numpy.dstack(channels)


def generate_radial_gradient(center, radius, from_color, to_color, height, width):
    gradient = numpy.zeros((height, width, 3), dtype=numpy.uint8)

    # Calculate the distance from the center for each pixel
    for y in range(height):
        for x in range(width):

            distance = numpy.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)

            normalized_distance = min(distance / radius, 1.0)


            for channel in range(3):

                gradient[y, x, channel] = int(
                    from_color[channel] + (to_color[channel] - from_color[channel]) * normalized_distance)
    return gradient