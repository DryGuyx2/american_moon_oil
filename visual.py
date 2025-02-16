import pygame

def draw_tilegrid(grid, screen, assets, tile_size, cursor_position=None):
    draw_order = build_tile_draw_order(grid, screen, assets, tile_size, cursor_position)
    draw_tiles_from_order(draw_order, screen)


def build_tile_draw_order(grid, screen, assets, tile_size, cursor_position):
    # Draw order is a nested list structure where
    # every sub-list contains a tile image,
    # with a screen position
    # Every tile in each layer is then
    # drawn in order based on the layer position in the list
    draw_order = []

    # Here we set up the layers, and tiles
    for row_index, row in enumerate(grid):
        for tile_index, tile in enumerate(row):
            screen_position = (tile.position[0] * tile_size[0], tile.position[1] * tile_size[1])
            for layer_index, layer in enumerate(tile.layers):

                # For some reason there is one too few draw
                # layers added at the top-left corner of the grid,
                # so we just add a layer at that position.
                # This is most likely a bad way to handle the edge case,
                # but i dont have the energy, nor time to handle this now
                if (row_index, tile_index) == (0, 0):
                    draw_order.append([])

                if layer_index == 0:
                    draw_order.append([])

                # Here we add the tile to the correct layer index in the draw order list
                draw_info = ()
                if assets[layer]["type"] == "image":
                    draw_info = (assets[layer]["surface"], screen_position)
                elif assets[layer]["type"] == "animation":
                    draw_info = (assets[layer]["surface"].blit_ready(), screen_position)
                draw_order[layer_index].append(draw_info)

            # After setting up all the tiles, we finally place the cursor at the top of its position
            if cursor_position == (row_index, tile_index):
                top_layer = len(grid[row_index][tile_index].layers) - 1
                draw_order[top_layer].append((assets["cursor"]["surface"], screen_position))

    return draw_order

def draw_tiles_from_order(order, screen):
    for layer in order:
        for tile in layer:
            screen.blit(tile[0], tile[1])

def draw_stats(screen, stats, assets, display_position, screen_size, stat_colors, defaul_stat_color=(255, 255, 255)):
    screen.blit(assets["stat_display"]["surface"], display_position)

    y_offset = display_position[1] * 4
    stat_position_y = 0

    for stat, value in stats.items():
        color = stat_colors[stat] if stat in stat_colors.keys() else defaul_stat_color
        text = assets["font"].render(f"{stat}: {value}", False, color)

        x_position = display_position[0] * 4
        y_position = stat_position_y * display_position[1] * 5 + y_offset
        stat_position_y += 1

        screen.blit(text, (x_position, y_position))

def render_structure_selection(selection, assets):
    selection_bar = assets["selection_bar"]["surface"].copy()

    icon_x_offset = 11
    icon_y_offset = 18
    icon_spacing = 22
    y_position = icon_y_offset

    frame_x_offset = 3
    frame_y_offset = 2
    for index, structure in enumerate(selection.selection):
        x_position = icon_spacing * index + icon_x_offset
        selection_bar.blit(assets["selection"][structure]["surface"], (x_position, y_position))

        if index == selection.position:
            selection_bar.blit(assets["selection_frame"]["surface"], (x_position - frame_x_offset, y_position - frame_y_offset))

    return selection_bar
