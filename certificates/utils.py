from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
import textwrap
import cStringIO
import clubs.utils
import media.utils
import random
import os


def get_temporary_paths(request_pk):
    if settings.DEBUG:
        root = settings.DEFAULT_STATIC_ROOT
    else:
        root = settings.STATIC_ROOT
    request_pk = str(request_pk)
    file_path = os.path.join(root, 'certificate_tmp', request_pk)
    relative_url = static('certificate_tmp/' + str(request_pk))
    return file_path, relative_url

def generate_certificate_image(request_pk, template, texts,
                               template_bytes=None, positions=None):
    # if template.font_family:
    #     font_family = template.font_family
    # else:
    #     # By default, we are shipping a font
    #     font_name = 'Unique.ttf'
    #     #font_name = 'Carlito-Regular.ttf'
        

    # If the template is saved, we don't really need to pass
    # positions, and template_byes
    if not positions:
        positions = template.text_positions.all()
    if not template_bytes:
        template_bytes = template.image.read()

    base = Image.open(cStringIO.StringIO(template_bytes))
    base = base.convert("RGBA")
    txt = Image.new('RGBA', base.size, (255, 255, 255, 0))
    count = 0
    for position in positions:
        text = texts[count]
        # get a font
        if position.font_family:
            font_name = position.font_family.name
        else:
            font_name = 'Unique.ttf'
        font_family = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', font_name)
        fnt = ImageFont.truetype(font_family, position.size)
        # get a drawing context
        d = ImageDraw.Draw(txt)
        lines = textwrap.wrap(text, width=60)
        if position.y_center:
            line = lines[0]
            height_per_line = fnt.getsize(line)[1]
            total_height = height_per_line * len(lines)
            text_y_center = (total_height / 2)
            initial_y = position.y_position - text_y_center
        else:
            initial_y = position.y_position

        for line in lines:
            width, height = fnt.getsize(line)
            if position.x_center:
                text_x_center = width / 2
                initial_x = position.x_position - text_x_center
            else:
                initial_x = position.x_position

            # draw text, full opacity
            d.text((initial_x, initial_y), line, font=fnt, fill="#"+position.color)
            line_space = height * 0.2
            initial_y += height + line_space
        count += 1
    out = Image.alpha_composite(base, txt)
    file_path, relative_url = get_temporary_paths(request_pk)

    out.save(file_path, format=template.image_format)
    return file_path, relative_url

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
