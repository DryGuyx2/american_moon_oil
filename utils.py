from pathlib import Path

import pygame
from gif_pygame import transform


def scale_number(number, old_range, new_range):
    # First we shift the range of the old range
    old_range_width = old_range[1] - old_range[0]

    # If the width of the old range is 0, we raise an error
    if old_range_width == 0:
        raise ValueError("Size of old range must be larger than zero")

    # Then we shift the number to be zero in the range
    shifted_number = number - old_range[0]

    # The number then gets normalized (put in a range between 0, and 1)
    normalized_number = shifted_number / old_range_width

    # Then we multiply it by the width of the new range
    new_range_width = new_range[1] - new_range[0]
    scaled_number = normalized_number * new_range_width

    # Then we finally move the the scaled number,
    # to its position in the range
    return new_range[0] + scaled_number

def scale_tile_sprite(sprite, size_tiles, tile_size):
    if sprite["type"] == "image":
        scaled_size = (size_tiles[0] * tile_size[0], size_tiles[1] * tile_size[1])
        sprite["surface"] = pygame.transform.scale(sprite["surface"], scaled_size)

    if sprite["type"] == "animation":
        scaled_size = (size_tiles[0] * tile_size[0], size_tiles[1] * tile_size[1])
        transform.scale(sprite["surface"], scaled_size)


#def load_assets(raw_asset_path):
#    asset_path = Path(raw_asset_path)
#
#    # Load sprite files
#    sprites = {sprite.stem: [pygame.image.load(sprite)] for sprite in asset_path.iterdir() if not sprite.is_dir()}
#
#    # Locate sprite folders that contain animations
#    animation_folders = [sprite_animation for sprite_animation in asset_path.iterdir() if sprite_animation.is_dir()]
#
#    for animation_folder in animation_folders:
#        animation = []
#
#        for frame_file in sorted(animation_folder.iterdir()):
#            animation.append(pygame.image.load(frame_file))
#
#        sprites[animation_folder.name] = animation
#
#    return sprites
