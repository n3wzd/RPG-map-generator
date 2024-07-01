import dungeon_maker
import map_to_image
import map_to_json
import parameter as param
import tile_crop

tileset = tile_crop.main()
dungeon = dungeon_maker.main()
map_to_image.main(dungeon.map, tileset, param.map_id)
map_to_json.main(dungeon.map, param.tileset_id, param.map_id)
print('done!')
