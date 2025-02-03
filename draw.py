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
                draw_order[layer_index].append((assets[layer], screen_position))
            # After setting up all the tiles, we finally place the cursor at the top of its position
            if cursor_position == (row_index, tile_index):
                top_layer = len(grid[row_index][tile_index].layers) - 1
                draw_order[top_layer].append((assets["cursor"], screen_position))

    return draw_order

def draw_tiles_from_order(order, screen):
    for layer in order:
        for tile in layer:
            screen.blit(tile[0], tile[1])

def draw_stats(screen, stats, assets, scree_size, stat_colors, defaul_stat_color=(255, 255, 255)):
    stat_position_y = 0
    for stat, value in stats.items():
        if stat in stat_colors.keys():
            text = assets["font"].render(f"{stat}: {value}", False, stat_colors[stat])
            position = (0, stat_position_y * scree_size[1] // 30)
            screen.blit(text, position)
            return

        text = assets["font"].render(f"{stat}: {value}", False, defaul_stat_color)
        position = (0, stat_position_y * scree_size[1] // 30)
        screen.blit(text, position)
        stat_position_y += 1
