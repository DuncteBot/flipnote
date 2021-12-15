from utils.textbox import TextBox
from io import BytesIO
from PIL import Image
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('drake', __name__)


def create_drake(top, bottom, image_template: str = None):
    b = BytesIO()
    template_use = image_template if image_template else 'template.jpg'
    font_size = 35
    font_path = "assets/_fonts/verdana_edited.ttf"
    base = Image.open(f"assets/drake/{template_use}").convert("RGBA")
    [_, img_height] = base.size
    txtO = Image.new("RGBA", base.size, (255, 255, 255, 0))

    top_box = TextBox(txtO)
    top_box.set_font(font_path, font_size)
    # top_box.set_background_color("White")
    top_box.set_box(250, 0, 250, img_height // 2 + 5)

    top_box.draw(top)

    bottom_box = TextBox(txtO)
    bottom_box.set_font(font_path, font_size)
    # bottom_box.set_background_color("Lime")
    bottom_box.set_box(250, 258, 250, img_height // 2 + 5)

    bottom_box.draw(bottom)

    out = Image.alpha_composite(base, txtO)

    out.save(b, "PNG")
    b.seek(0)
    return b


@blueprint.route('/drake')
async def drake():
    """?top=text&bottom=text"""
    top = request.args.get('top')
    bottom = request.args.get('bottom')
    ayano = request.args.get('ayano')
    if not top or not bottom:
        abort(400, "You must provide top and bottom text")

    if len(top + bottom) > 500:
        abort(400, "You are limited to 500 characters only, sorry")

    image_template = None
    if ayano:
        image_template = "template_ayano.jpg"

    return await send_file(
        create_drake(top, bottom, image_template=image_template),
        mimetype='image/png',
        attachment_filename='drake.png'
    )
