from flask import Flask, request, render_template, jsonify, url_for

import dungeon_maker
import map_to_image
import map_to_json
import parameter as param
import tile_crop

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
  output_path = 'static/output/'

  for key, value in request.form.items():
    if hasattr(param, key):
      setattr(param, key, int(value))

  tileset = tile_crop.main()
  dungeon = dungeon_maker.main()
  img_path = map_to_image.main(dungeon.map, tileset, param.map_id, output_path)
  map_to_json.main(dungeon.map, param.tileset_id, param.map_id, output_path)

  return jsonify(img_path=img_path)


if __name__ == '__main__':
  app.run(debug=True)
