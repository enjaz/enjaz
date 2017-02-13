from PIL import Image, ImageDraw, ImageFont
import cStringIO
import clubs.utils
import media.utils


def generate_certificate_image(template_bytes, image_format, y_position, x_position, text, color, font_size, font_family=None):
    font_family = '/usr/share/fonts/google-crosextra-carlito/Carlito-Regular.ttf'
    base = Image.open(cStringIO.StringIO(template_bytes))
    base = base.convert("RGBA")

    txt = Image.new('RGBA', base.size, (255,255,255,0))
    # get a font
    fnt = ImageFont.truetype(font_family, font_size)
    # get a drawing context
    d = ImageDraw.Draw(txt)
    text_x_center = fnt.getsize(text)[0] / 2
    text_y_center = fnt.getsize(text)[1] / 2
    # draw text, full opacity
    a = d.text((x_position - text_x_center, y_position - text_y_center), text, font=fnt, fill="#"+color)
    out = Image.alpha_composite(base, txt)
    img_response = cStringIO.StringIO()
    out.show()
    out.save(img_response, format=image_format)
    return img_response


def can_approve_certificates(user):
    if user.is_superuser or \
       media.utils.is_media_coordinator_or_member(user):
        return True
    else:
        return False

def can_edit_certificate_request(user, certificate_request):
    if certificate_request.episode:
        coordination_status = clubs.utils.has_coordination_to_activity(user, certificate_request.episode.activity)
    else:
        coordination_status = False

    if coordination_status or \
       user == certificate_request.submitter or \
       user.is_superuser or \
       media.utils.is_media_coordinator_or_member(user):
        return True
    else:
        return False

def can_view_all_certificates(user):
    if user.is_superuser or \
       media.utils.is_media_coordinator_or_member(user):
        return True
    else:
        return False
