from pathlib import Path

import pygame


def load_assets(raw_asset_path):
    asset_path = Path(raw_asset_path)

    # Load sprite files
    sprites = [pygame.image.load(sprite) for sprite in asset_path.iterdir() if not sprite.is_dir()]

    # Locate sprite folders that contain animations
    animation_folders = [sprite_animation for sprite_animation in asset_path.iterdir() if sprite_animation.is_dir()]

    for animation_folder in animation_folders:
        animation = []

        for frame_file in sorted(animation_folder.iterdir()):
            animation.append(pygame.image.load(frame_file))

        sprites.append(animation)

    return sprites
