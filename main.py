import dungeon_maker
import map_to_image
import tile_crop

tileset = tile_crop.main()
dungeon = dungeon_maker.main()
map_to_image.main(dungeon.map, tileset)
print('done!')
