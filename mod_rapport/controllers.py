from flask import Blueprint, request, render_template, flash, g, session, \
    redirect, url_for, flash, make_response
from flask.helpers import make_response
from app import db, app
from app.mod_fatquarter.models import Estampa, EstampaSchema
from app.mod_fatquarter.forms import EstampasSearchForm
import os
from .rapport import create_repeats, allowed_file, repeat_filename, REPEAT_LIST, ALLOWED_EXTENSIONS
from .forms import CartForm
from werkzeug.utils import secure_filename

mod_rapport = Blueprint('rapport', __name__, url_prefix='/rapport/')

@mod_rapport.route('/')
def select():
    cart_id = request.args['cart_id'] if 'cart_id' in request.args else None
    resp = render_template('rapport/rapport.j2', os=os, image_dir='../../static/images')
    #resp.set_cookie('cart_id', cart_id)
    return resp


@mod_rapport.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('Nenhum arquivo encontrado')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('Nenhuma imagem selecionada')
        return redirect(request.url)
    if file and allowed_file(file.filename): 
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
        create_repeats(filename, app.config['UPLOAD_DIR'])
        flash('Upload de imagem com sucesso')
        img_path = os.path.join('../../static/uploads', filename)
        img_paths = {}
        for repeat in REPEAT_LIST:
            img_paths[repeat] = os.path.join('../../static/uploads', repeat_filename(filename, repeat))
        cart_form = CartForm()
        return render_template('rapport/rapport.j2', filename=filename, img_paths=img_paths, cart_form=cart_form)
    else:
        flash('ERRO: Tipos de arquivo permitidos: ' + ', '.join(list(ALLOWED_EXTENSIONS)))
        return redirect(request.url)
