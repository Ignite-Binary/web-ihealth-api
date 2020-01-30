import os
from flask_restplus import abort


def allowed_images(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    if '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return filename.rsplit('.', 1)[1].lower()


def delete_temp_image(filename):
    file_path = f'static/temporary/{filename}'
    if os.path.isfile(f'{file_path}.jpg'):
        os.remove(f'{file_path}.jpg')
    if os.path.isfile(f'{file_path}.jpeg'):
        os.remove(f'{file_path}.jpeg')
    if os.path.isfile(f'{file_path}.png'):
        os.remove(f'{file_path}.png')


def save_temp_image(filename):
    temp_path = f'static/temporary/{filename}'
    permanent_path = f'static/images/{filename}'
    if os.path.isfile(temp_path):
        os.rename(temp_path, permanent_path)
        return filename


def verify_owner(owner, identity):
    if owner != identity:
        abort(403, 'You are not authorized!')
