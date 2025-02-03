def build_structure(stats, structure_name, tile, structure_map):
    for layer in tile.layers:
        if layer in structure_map.keys():
            return

    for build_resource, amount in structure_map[structure_name]["build_resources"].items():
        if not build_resource in stats.keys():
            return

        if stats[build_resource] < amount:
            return

    for build_resource, amount in structure_map[structure_name]["build_resources"].items():
        stats[build_resource] -= amount

    tile.layers.append(structure_name)


def process_structures(grid, stats, STRUCTURE_MAP):
    for row in grid.grid:
        for tile in row:
            for layer in tile.layers:
                if not layer in STRUCTURE_MAP.keys():
                    continue

                if STRUCTURE_MAP[layer]["product"] in stats.keys():
                    stats[STRUCTURE_MAP[layer]["product"]] += STRUCTURE_MAP[layer]["amount"]
                    continue

                stats[STRUCTURE_MAP[layer]["product"]] = STRUCTURE_MAP[layer]["amount"]
