from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_cors import cross_origin
from utils.validations import *
from database import db
from werkzeug.utils import secure_filename
import filetype
import hashlib
import os


UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/inicio')
def inicio():
    msg=None
    return render_template('html/inicio.html', msg=msg)

@app.route('/donacion', methods=('GET', 'POST'))
def donacion():
    error = None
    if request.method == 'POST':
        region = request.form.get('region')
        comuna = request.form.get('comuna')
        calle = request.form.get('calle-numero')
        tipo = request.form.get('tipo')
        cantidad = request.form.get('cantidad')
        fecha = request.form.get('fecha-disponibilidad')
        descripcion = request.form.get('descripcion')
        condiciones = request.form.get('condiciones')
        foto1 = request.files.get('foto-1')
        foto2 = request.files.get('foto-2')
        foto3 = request.files.get('foto-3')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('celular')

        error=None

        if validate_donacion(region,comuna,calle,tipo,cantidad,fecha,descripcion,condiciones,foto1,foto2,foto3,nombre,email,celular):

            # 1. generate random name for img
            _filename = hashlib.sha256(secure_filename(foto1.filename).encode("utf-8")).hexdigest()
            _extension = filetype.guess(foto1).extension
            img_filename = f"{_filename}.{_extension}"
            # 2. save img as a file
            foto1.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))
            # 3. save confession in db
            db.create_donacion(comuna, calle, tipo, cantidad, fecha, descripcion, condiciones, nombre, email, celular)
            donacion_id = db.get_id_donacion(comuna, calle, tipo, cantidad, descripcion, condiciones, nombre, email, celular)
            #query que devuelve el id (select id de todo lo que subi recien)
            db.create_foto(UPLOAD_FOLDER, img_filename, donacion_id)
            if foto2 is not None and validate_foto(foto2):
                _filename2 = hashlib.sha256(secure_filename(foto2.filename).encode("utf-8")).hexdigest()
                _extension2 = filetype.guess(foto2).extension
                img_filename2 = f"{_filename2}.{_extension2}"
                foto2.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename2))
                db.create_foto(UPLOAD_FOLDER, img_filename2, donacion_id)
            if foto3 is not None and validate_foto(foto3):
                _filename3 = hashlib.sha256(secure_filename(foto3.filename).encode("utf-8")).hexdigest()
                _extension3 = filetype.guess(foto3).extension
                img_filename3 = f"{_filename3}.{_extension3}"
                foto3.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename3))
                db.create_foto(UPLOAD_FOLDER, img_filename3, donacion_id)
            return render_template('html/inicio.html', msg=" Hemos recibido la información de su donación. Muchas gracias.")
        else:
            if not validate_region(region):
                error = "Region invalida"
            elif not validate_comuna(comuna):
                error = "Comuna invalida"
            elif not validate_calle(calle):
                error = "Calle invalida"
            elif not validate_tipo(tipo):
                error = "Tipo invalida"
            elif not validate_cantidad(cantidad):
                error = "Cantidad invalida"
            elif (not validate_fecha(fecha)):
                error = "Fecha invalida"
            elif (not validate_descripcion(descripcion)):
                error = "Descripción invalida"
            elif (not validate_nombre(nombre)):
                error = "Nombre invalida"
            elif (not validate_email(email)):
                error = "Email invalida"
            elif (not validate_celular(celular)):
                error = "Celular invalida"
            elif (not validate_foto(foto1)):
                error = "Foto 1 invalida"
            elif (not validate_foto2(foto2)):
                error = "Foto 2 invalida"
            elif (not validate_foto2(foto3)):
                error = "Foto 3 invalida"
            else:
                error = 'Algún campo es invalido'

    return render_template('html/agregar-donacion.html',error=error)

@app.route('/pedido', methods=('GET', 'POST'))
def pedido():
    error = None
    if request.method == 'POST':
        region = request.form.get('region')
        comuna = request.form.get('comuna')
        tipo = request.form.get('tipo')
        descripcion = request.form.get('descripcion')
        cantidad = request.form.get('cantidad')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('celular')
        
        if validate_pedido(region,comuna,tipo,descripcion,cantidad,nombre,email,celular):
            db.create_pedido(comuna,tipo,descripcion,cantidad,nombre,email,celular)
            return render_template('html/inicio.html', msg=" Hemos recibido la información de su donación. Muchas gracias.")
        #mostrar mensaje apropiado
        else:
            if not validate_region(region):
                error = "Region invalida"
            elif not validate_comuna(comuna):
                error = "Comuna invalida"
            elif (not validate_tipo(tipo)):
                error = "Tipo invalida"
            elif (not validate_cantidad(cantidad)):
                error = "Cantidad invalida"
            elif (not validate_descripcion(descripcion)):
                error = "Descripción invalida"
            elif (not validate_nombre(nombre)):
                error = "Nombre invalida"
            elif (not validate_email(email)):
                error = "Email invalida"
            elif (not validate_celular(celular)):
                error = "Celular invalida"
            else:
                error = 'Algún campo es invalido'

    return render_template('html/agregar-pedido.html', error=error)

@app.route('/ver-donacion/<page>')
def ver_donacion(page):
    donaciones = db.donaciones()
    data = []
    page=int(page)
    if (page-1)*5 >= donaciones:
        page-=1
    if (page-1)*5 < 0:
        page +=1
    for don in db.get_donaciones((page-1)*5):
        
        donacion_id, comuna_id, _, tipo, cantidad, fecha, descripcion, condiciones, nombre, email, celular = don
        comuna = db.get_comuna_by_id(comuna_id)

        fotos= db.get_Nfoto_by_donacion(donacion_id)
        nombre_archivo = fotos
        img_filename= f"uploads/{nombre_archivo}"

        # for foto in db.get_foto_by_donacion(donacion_id):
        #     _, ruta_archivo, nombre_archivo, _ = foto
        #     img_filename= f"uploads/{nombre_archivo}"
        #     fotos.append({
        #         "path_image": url_for('static', filename=img_filename)
        #     })

        data.append({
            "comuna": comuna[0],
            "tipo": tipo,
            "cantidad": cantidad,
            "fecha": fecha,
            "nombre": nombre,
            "foto": url_for('static', filename=img_filename),
            "id": donacion_id,    
        })
    pag = {
        "pag": page
    }
    return render_template('html/ver-donaciones.html', data=data, pag=pag)

@app.route('/ver-pedido/<page>')
def ver_pedido(page):
    pedidos = db.pedidos()
    data = []
    page=int(page)
    if (page-1)*5 >= pedidos:
        page-=1
    if (page-1)*5 < 0:
        page +=1
    for ped in db.get_pedidos((page-1)*5):
        id, comuna_id, tipo, descripcion, cantidad, nombre, email, celular = ped
        comuna = db.get_comuna_by_id(comuna_id)
        data.append({
            "comuna": comuna[0],
            "tipo": tipo,
            "descripcion": descripcion,
            "cantidad": cantidad,
            "nombre": nombre,
            "id": id
    
        })
    pag = {
        "pag": page
    }

    return render_template('html/ver-pedidos.html', data=data, pag=pag)

@app.route('/donacion-info/<id>')
def info_donacion(id):
    data=[]
    files=[]
    don_id,comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular = db.get_donacion_by_id(id)
    comuna = db.get_comuna_by_id(comuna_id)
    regionid = db.get_region_id_by_comuna(comuna_id)
    region = db.get_region_by_id(regionid)

    fotos = db.get_Nfoto_by_donacion(don_id)
    f= fotos
    n= len(f)
    for i in range(0, n):
        files.append(f"uploads/{f[i]}")
    if n==1:
        data.append({
            "region": region[0],
            "comuna": comuna[0],
            "calle": calle_numero,
            "tipo": tipo,
            "cantidad": cantidad,
            "fecha": fecha_disponibilidad,
            "descripcion": descripcion,
            "condiciones": condiciones_retirar,
            "foto1": url_for('static', filename=files[0]),
            "foto2": "",
            "foto3": "",
            "nombre": nombre,
            "email": email,
            "celular": celular

        })
    elif n==2:
        data.append({
            "region": region[0],
            "comuna": comuna[0],
            "calle": calle_numero,
            "tipo": tipo,
            "cantidad": cantidad,
            "fecha": fecha_disponibilidad,
            "descripcion": descripcion,
            "condiciones": condiciones_retirar,
            "foto1": url_for('static', filename=files[0]),
            "foto2": url_for('static', filename=files[1]),
            "foto3": "",
            "nombre": nombre,
            "email": email,
            "celular": celular

        })
    else:
        data.append({
            "region": region[0],
            "comuna": comuna[0],
            "calle": calle_numero,
            "tipo": tipo,
            "cantidad": cantidad,
            "fecha": fecha_disponibilidad,
            "descripcion": descripcion,
            "condiciones": condiciones_retirar,
            "foto1": url_for('static', filename=files[0]),
            "foto2": url_for('static', filename=files[1]),
            "foto3": url_for('static', filename=files[2]),
            "nombre": nombre,
            "email": email,
            "celular": celular

        })

    return render_template('html/informacion-donacion.html', data=data)

@app.route('/pedido-info/<id>')
def info_pedido(id):
    data=[]
    id, comuna_id, tipo, descripcion, cantidad, nombre, email, celular = db.get_pedido_by_id(id)
    comuna = db.get_comuna_by_id(comuna_id)
    regionid = db.get_region_id_by_comuna(comuna_id)
    region = db.get_region_by_id(regionid)
    data.append({
        "region": region[0],
        "comuna": comuna[0],
        "tipo": tipo,
        "descripcion": descripcion,
        "cantidad": cantidad,
        "nombre": nombre,
        "email": email,
        "celular": celular

    })
    return render_template('html/informacion-pedido.html', data=data)

@app.route("/get-don-map-data", methods=["GET"])
@cross_origin(origin="localhost", supports_credentials=True)
def get_don_map_data():
    
    don = db.get_mapa_don()

    markers = []
    for d in don:
        id, comuna, calle_numero, tipo, cantidad, fecha_disponibilidad, email = d
        comunaa= db.get_comuna_by_id(comuna)

        for i in ll:
            if i["name"] == comunaa[0]:
                lat = i["lat"]
                long = i["lng"]

        markers.append({
            "id": id,
            "calle": calle_numero,
            "tipo": tipo,
            "cantidad": cantidad,
            "fecha": fecha_disponibilidad,
            "email": email,
            "lat": lat,
            "long": long
        })

    return jsonify(markers)

@app.route("/get-ped-map-data", methods=["GET"])
@cross_origin(origin="localhost", supports_credentials=True)
def get_ped_map_data():
    
    ped = db.get_mapa_ped()

    markers = []
    for p in ped:
        id, comuna, tipo, cantidad, email = p
        comunaa= db.get_comuna_by_id(comuna)

        for i in ll:
            if i["name"] == comunaa[0]:
                lat = str(float(i["lat"])+ 0.001)
                long = str(float(i["lng"])+ 0.001)

        markers.append({
            "id": id,
            "tipo": tipo,
            "cantidad": cantidad,
            "email": email,
            "lat": lat,
            "long": long
        })

    return jsonify(markers)

@app.route("/stats", methods=["GET"])
def stats():
    return render_template("html/stats.html")

@app.route("/get-don-stats-data", methods=["GET"])
@cross_origin(origin="localhost", supports_credentials=True)
def get_don_stats_data():
    
    fd = db.get_type_fruta_don()
    vd = db.get_type_verdura_don()
    od = db.get_type_otro_don()

    random_data = {
        "fruta": fd,
        "verdura": vd,
        "otro": od
    }
    return jsonify(random_data)

@app.route("/get-ped-stats-data", methods=["GET"])
@cross_origin(origin="localhost", supports_credentials=True)
def get_ped_stats_data():
    
    fd = db.get_type_fruta_ped()
    vd = db.get_type_verdura_ped()
    od = db.get_type_otro_ped()

    random_data = {
        "fruta": fd,
        "verdura": vd,
        "otro": od
    }
    return jsonify(random_data)



if __name__ == "__main__":
    app.run(debug=True)

ll = [{
    "name": "Santiago",
    "lng": "-70.6666667",
    "lat": "-33.4500000"
}, {
    "name": "Cerro Navia",
    "lng": "-70.7166667",
    "lat": "-33.4166667"
}, {
    "name": "El Bosque",
    "lng": "-70.7000000",
    "lat": "-33.5666667"
}, {
    "name": "Huechuraba",
    "lng": "-70.6666667",
    "lat": "-33.3500000"
}, {
    "name": "La Cisterna",
    "lng": "-70.6833333",
    "lat": "-33.5500000"
}, {
    "name": "La Granja",
    "lng": "-70.5833333",
    "lat": "-33.5833333"
}, {
    "name": "La Reina",
    "lng": "-70.5500000",
    "lat": "-33.4500000"
}, {
    "name": "Lo Barnechea",
    "lng": "-70.5166667",
    "lat": "-33.3500000"
}, {
    "name": "Lo Prado",
    "lng": "-70.7166667",
    "lat": "-33.4333333"
}, {
    "name": "Maipú",
    "lng": "-70.7666667",
    "lat": "-33.5166667"
}, {
    "name": "Pedro Aguirre Cerda",
    "lng": "-70.6780860",
    "lat": "-33.4924550"
}, {
    "name": "Providencia",
    "lng": "-70.6166667",
    "lat": "-33.4333333"
}, {
    "name": "Quilicura",
    "lng": "-70.7500000",
    "lat": "-33.3666667"
}, {
    "name": "Recoleta",
    "lng": "-33.4081480",
    "lat": "-70.6391920"
}, {
    "name": "San Joaquín",
    "lng": "-70.6166667",
    "lat": "-33.5000000"
}, {
    "name": "San Ramón",
    "lng": "-70.5000000",
    "lat": "-33.4500000"
}, {
    "name": "Puente Alto",
    "lng": "-70.5833333",
    "lat": "-33.6166667"
}, {
    "name": "Padre Hurtado",
    "lng": "-70.8333333",
    "lat": "-33.5666667"
}, {
    "name": "El Monte",
    "lng": "-71.0166667",
    "lat": "-33.6833333"
}, {
    "name": "San Pedro",
    "lng": "-71.4666667",
    "lat": "-33.9000000"
}, {
    "name": "Curacaví",
    "lng": "-71.1500000",
    "lat": "-33.4000000"
}, {
    "name": "Melipilla",
    "lng": "-71.2166667",
    "lat": "-33.7000000"
}, {
    "name": "Calera de Tango",
    "lng": "-70.8166667",
    "lat": "-33.6500000"
}, {
    "name": "San Bernardo",
    "lng": "-70.7166667",
    "lat": "-33.6000000"
}, {
    "name": "Lampa",
    "lng": "-70.9000000",
    "lat": "-33.2833333"
}, {
    "name": "San José de Maipo",
    "lng": "-70.3666667",
    "lat": "-33.6333333"
}, {
    "name": "Peñaflor",
    "lng": "-70.9166667",
    "lat": "-33.6166667"
}, {
    "name": "Isla de Maipo",
    "lng": "-70.9000000",
    "lat": "-33.7500000"
}, {
    "name": "Talagante",
    "lng": "-70.9333333",
    "lat": "-33.6666667"
}, {
    "name": "María Pinto",
    "lng": "-71.1333333",
    "lat": "-33.5333333"
}, {
    "name": "Paine",
    "lng": "-70.7500000",
    "lat": "-33.8166667"
}, {
    "name": "Buin",
    "lng": "-70.7500000",
    "lat": "-33.7333333"
}, {
    "name": "Tiltil",
    "lng": "-70.9333333",
    "lat": "-33.0833333"
}, {
    "name": "Colina",
    "lng": "-70.6833333",
    "lat": "-33.2000000"
}, {
    "name": "Pirque",
    "lng": "-70.5500000",
    "lat": "-33.6333333"
}, {
    "name": "Vitacura",
    "lng": "-70.6000000",
    "lat": "-33.4000000"
}, {
    "name": "San Miguel",
    "lng": "-70.6666667",
    "lat": "-33.5000000"
}, {
    "name": "Renca",
    "lng": "-70.7333333",
    "lat": "-33.4000000"
}, {
    "name": "Quinta Normal",
    "lng": "-70.7000000",
    "lat": "-33.4500000"
}, {
    "name": "Pudahuel",
    "lng": "-70.7166667",
    "lat": "-33.4333333"
}, {
    "name": "Peñalolén",
    "lng": "-70.5333333",
    "lat": "-33.4833333"
}, {
    "name": "Ñuñoa",
    "lng": "-70.6000000",
    "lat": "-33.4666667"
}, {
    "name": "Macul",
    "lng": "-70.5666667",
    "lat": "-33.5000000"
}, {
    "name": "Lo Espejo",
    "lng": "-70.7166667",
    "lat": "-33.5333333"
}, {
    "name": "Las Condes",
    "lng": "-70.5833333",
    "lat": "-33.4166667"
}, {
    "name": "La Pintana",
    "lng": "-70.6166667",
    "lat": "-33.5833333"
}, {
    "name": "La Florida",
    "lng": "-70.5666667",
    "lat": "-33.5500000"
}, {
    "name": "Independencia",
    "lng": "-70.6549320",
    "lat": "-33.4219880"
}, {
    "name": "Estación Central",
    "lng": "-70.7029760",
    "lat": "-33.4633150"
}, {
    "name": "Conchalí",
    "lng": "-70.6166667",
    "lat": "-33.3500000"
}, {
    "name": "Cerrillos",
    "lng": "-70.7000000",
    "lat": "-33.4833333"
}, {
    "name": "Arica",
    "lng": "-70.3144444",
    "lat": "-18.4750000"
}, {
    "name": "Camarones",
    "lng": "-69.8666667",
    "lat": "-19.0166667"
}, {
    "name": "Putre",
    "lng": "-69.5977778",
    "lat": "-18.1916667"
}, {
    "name": "General Lagos",
    "lng": "-69.5000000",
    "lat": "-17.5666667"
}, {
    "name": "Iquique",
    "lng": "-70.1666667",
    "lat": "-20.2166667"
}, {
    "name": "Alto Hospicio",
    "lng": "-70.1166667",
    "lat": "-20.2500000"
}, {
    "name": "Pozo Almonte",
    "lng": "-69.7833333",
    "lat": "-20.2666667"
}, {
    "name": "Camiña",
    "lng": "-69.4166667",
    "lat": "-19.3000000"
}, {
    "name": "Colchane",
    "lng": "-68.6166667",
    "lat": "-19.2666667"
}, {
    "name": "Huara",
    "lng": "-69.7666667",
    "lat": "-19.9666667"
}, {
    "name": "Pica",
    "lng": "-69.3333333",
    "lat": "-20.5000000"
}, {
    "name": "Antofagasta",
    "lng": "-70.4000000",
    "lat": "-23.6333333"
}, {
    "name": "Mejillones",
    "lng": "-70.4500000",
    "lat": "-23.1000000"
}, {
    "name": "Sierra Gorda",
    "lng": "-69.3166667",
    "lat": "-22.8833333"
}, {
    "name": "Taltal",
    "lng": "-69.7666667",
    "lat": "-25.2833333"
}, {
    "name": "Calama",
    "lng": "-68.9166667",
    "lat": "-22.4666667"
}, {
    "name": "Ollague",
    "lng": "-68.2666667",
    "lat": "-21.2166667"
}, {
    "name": "San Pedro de Atacama",
    "lng": "-68.2166667",
    "lat": "-22.9166667"
}, {
    "name": "María Elena",
    "lng": "-69.6666667",
    "lat": "-22.3500000"
}, {
    "name": "Tocopilla",
    "lng": "-70.2000000",
    "lat": "-22.0666667"
}, {
    "name": "Copiapó",
    "lng": "-70.3166667",
    "lat": "-27.3666667"
}, {
    "name": "Caldera",
    "lng": "-70.8166667",
    "lat": "-27.0666667"
}, {
    "name": "Tierra Amarilla",
    "lng": "-70.2666667",
    "lat": "-27.4666667"
}, {
    "name": "Chañaral",
    "lng": "-70.6000000",
    "lat": "-26.3333333"
}, {
    "name": "Diego de Almagro",
    "lng": "-70.0500000",
    "lat": "-26.3666667"
}, {
    "name": "Vallenar",
    "lng": "-70.7500000",
    "lat": "-28.5666667"
}, {
    "name": "Alto del Carmen",
    "lng": "-70.4622222",
    "lat": "-28.9336111"
}, {
    "name": "Freirina",
    "lng": "-71.0666667",
    "lat": "-28.5000000"
}, {
    "name": "Huasco",
    "lng": "-71.2166667",
    "lat": "-28.4500000"
}, {
    "name": "Río Hurtado",
    "lng": "-70.7000000",
    "lat": "-30.2666667"
}, {
    "name": "Monte Patria",
    "lng": "-70.9333333",
    "lat": "-30.6833333"
}, {
    "name": "Ovalle",
    "lng": "-71.2000000",
    "lat": "-30.5833333"
}, {
    "name": "Los Vilos",
    "lng": "-71.5166667",
    "lat": "-31.9000000"
}, {
    "name": "Illapel",
    "lng": "-71.1500000",
    "lat": "-31.6166667"
}, {
    "name": "Paiguano",
    "lng": "-70.5166667",
    "lat": "-30.0166667"
}, {
    "name": "Andacollo",
    "lng": "-71.0833333",
    "lat": "-30.2166667"
}, {
    "name": "La Serena",
    "lng": "-71.2500000",
    "lat": "-29.9000000"
}, {
    "name": "Punitaqui",
    "lng": "-71.2666667",
    "lat": "-30.9000000"
}, {
    "name": "Combarbalá",
    "lng": "-71.0500000",
    "lat": "-31.1666667"
}, {
    "name": "Salamanca",
    "lng": "-70.9666667",
    "lat": "-31.7666667"
}, {
    "name": "Canela",
    "lng": "-71.4500000",
    "lat": "-31.4000000"
}, {
    "name": "Vicuña",
    "lng": "-70.7000000",
    "lat": "-30.0166667"
}, {
    "name": "La Higuera",
    "lng": "-71.2666667",
    "lat": "-29.5000000"
}, {
    "name": "Coquimbo",
    "lng": "-71.3333333",
    "lat": "-29.9500000"
}, {
    "name": "Valparaíso",
    "lng": "-71.6163889",
    "lat": "-33.0458333"
}, {
    "name": "Concón",
    "lng": "-71.5166667",
    "lat": "-32.9166667"
}, {
    "name": "Puchuncaví",
    "lng": "-71.4166667",
    "lat": "-32.7333333"
}, {
    "name": "Los Andes",
    "lng": "-70.6166667",
    "lat": "-32.8166667"
}, {
    "name": "Viña del Mar",
    "lng": "-71.5333333",
    "lat": "-33.0333333"
}, {
    "name": "Rinconada",
    "lng": "-70.7000000",
    "lat": "-32.8333333"
}, {
    "name": "La Ligua",
    "lng": "-71.2166667",
    "lat": "-32.4500000"
}, {
    "name": "Papudo",
    "lng": "-71.4500000",
    "lat": "-32.5166667"
}, {
    "name": "Zapallar",
    "lng": "-71.4666667",
    "lat": "-32.5333333"
}, {
    "name": "Calera",
    "lng": "-71.2166667",
    "lat": "-32.7833333"
}, {
    "name": "San Antonio",
    "lng": "-71.6166667",
    "lat": "-33.6000000"
}, {
    "name": "Cartagena",
    "lng": "-71.6000000",
    "lat": "-33.5500000"
}, {
    "name": "El Tabo",
    "lng": "-71.6666667",
    "lat": "-33.4500000"
}, {
    "name": "San Felipe",
    "lng": "-70.7333333",
    "lat": "-32.7500000"
}, {
    "name": "Llaillay",
    "lng": "-70.9666667",
    "lat": "-32.8500000"
}, {
    "name": "La Cruz",
    "lng": "-71.2333333",
    "lat": "-32.8166667"
}, {
    "name": "Villa Alemana",
    "lng": "-71.3666667",
    "lat": "-33.0500000"
}, {
    "name": "Limache",
    "lng": "-71.2833333",
    "lat": "-32.9833333"
}, {
    "name": "Putaendo",
    "lng": "-70.7333333",
    "lat": "-32.6333333"
}, {
    "name": "Olmué",
    "lng": "-71.2000000",
    "lat": "-33.0000000"
}, {
    "name": "Quilpué",
    "lng": "-71.4500000",
    "lat": "-33.0500000"
}, {
    "name": "Santa María",
    "lng": "-70.6666667",
    "lat": "-32.7500000"
}, {
    "name": "Panquehue",
    "lng": "-70.8333333",
    "lat": "-32.8000000"
}, {
    "name": "Catemu",
    "lng": "-71.0333333",
    "lat": "-32.6333333"
}, {
    "name": "Santo Domingo",
    "lng": "-71.6500000",
    "lat": "-33.6333333"
}, {
    "name": "El Quisco",
    "lng": "-71.7000000",
    "lat": "-33.4000000"
}, {
    "name": "Algarrobo",
    "lng": "-71.6927778",
    "lat": "-33.3911111"
}, {
    "name": "Nogales",
    "lng": "-71.2333333",
    "lat": "-32.7166667"
}, {
    "name": "Hijuelas",
    "lng": "-71.1666667",
    "lat": "-32.8000000"
}, {
    "name": "Quillota",
    "lng": "-71.2666667",
    "lat": "-32.8833333"
}, {
    "name": "Petorca",
    "lng": "-70.9333333",
    "lat": "-32.2500000"
}, {
    "name": "Cabildo",
    "lng": "-71.1333333",
    "lat": "-32.4166667"
}, {
    "name": "San Esteban",
    "lng": "-70.5833333",
    "lat": "-32.8000000"
}, {
    "name": "Calle Larga",
    "lng": "-70.6333333",
    "lat": "-32.8500000"
}, {
    "name": "Isla de Pascua",
    "lng": "-109.3750000",
    "lat": "-27.0833333"
}, {
    "name": "Quintero",
    "lng": "-71.5333333",
    "lat": "-32.7833333"
}, {
    "name": "Juan Fernández",
    "lng": "-78.8666667",
    "lat": "-33.6166667"
}, {
    "name": "Casablanca",
    "lng": "-71.4166667",
    "lat": "-33.3166667"
}, {
    "name": "Rancagua",
    "lng": "-70.7397222",
    "lat": "-34.1652778"
}, {
    "name": "Coinco",
    "lng": "-70.9666667",
    "lat": "-34.2666667"
}, {
    "name": "Doñihue",
    "lng": "-70.9666667",
    "lat": "-34.2333333"
}, {
    "name": "Las Cabras",
    "lng": "-71.3166667",
    "lat": "-34.3000000"
}, {
    "name": "Malloa",
    "lng": "-70.9500000",
    "lat": "-34.4500000"
}, {
    "name": "Olivar",
    "lng": "-70.8175000",
    "lat": "-34.2100000"
}, {
    "name": "San Vicente",
    "lng": "-71.1333333",
    "lat": "-34.5000000"
}, {
    "name": "Marchihue",
    "lng": "-71.6333333",
    "lat": "-34.4000000"
}, {
    "name": "Paredones",
    "lng": "-71.1666667",
    "lat": "-34.7833333"
}, {
    "name": "Chépica",
    "lng": "-71.2833333",
    "lat": "-34.7333333"
}, {
    "name": "Lolol",
    "lng": "-71.6447222",
    "lat": "-34.7286111"
}, {
    "name": "Palmilla",
    "lng": "-71.3666667",
    "lat": "-34.6000000"
}, {
    "name": "Santa Cruz",
    "lng": "-71.3666667",
    "lat": "-34.6333333"
}, {
    "name": "Placilla",
    "lng": "-71.1166667",
    "lat": "-34.6333333"
}, {
    "name": "La Estrella",
    "lng": "-71.6666667",
    "lat": "-34.2000000"
}, {
    "name": "Rengo",
    "lng": "-70.8666667",
    "lat": "-34.4166667"
}, {
    "name": "Pichidegua",
    "lng": "-71.3000000",
    "lat": "-34.3500000"
}, {
    "name": "Pumanque",
    "lng": "-71.6666667",
    "lat": "-34.6000000"
}, {
    "name": "Peralillo",
    "lng": "-71.4833333",
    "lat": "-34.4833333"
}, {
    "name": "Nancagua",
    "lng": "-71.2166667",
    "lat": "-34.6666667"
}, {
    "name": "Chimbarongo",
    "lng": "-71.0500000",
    "lat": "-34.7000000"
}, {
    "name": "San Fernando",
    "lng": "-70.9666667",
    "lat": "-34.5833333"
}, {
    "name": "Navidad",
    "lng": "-71.8333333",
    "lat": "-33.9333333"
}, {
    "name": "Litueche",
    "lng": "-71.7333333",
    "lat": "-34.1166667"
}, {
    "name": "Pichilemu",
    "lng": "-72.0000000",
    "lat": "-34.3833333"
}, {
    "name": "Requínoa",
    "lng": "-70.8333333",
    "lat": "-34.2833333"
}, {
    "name": "Quinta de Tilcoco",
    "lng": "-70.9833333",
    "lat": "-34.3500000"
}, {
    "name": "Peumo",
    "lng": "-71.1666667",
    "lat": "-34.4000000"
}, {
    "name": "Mostazal",
    "lng": "-70.7000000",
    "lat": "-33.9833333"
}, {
    "name": "Machalí",
    "lng": "-70.6511111",
    "lat": "-34.1825000"
}, {
    "name": "Graneros",
    "lng": "-70.7266667",
    "lat": "-34.0647222"
}, {
    "name": "Coltauco",
    "lng": "-71.0857230",
    "lat": "34.2872290"
}, {
    "name": "Codegua",
    "lng": "-70.6666667",
    "lat": "-34.0333333"
}, {
    "name": "Talca",
    "lng": "-71.6666667",
    "lat": "-35.4333333"
}, {
    "name": "Curepto",
    "lng": "-72.0166667",
    "lat": "-35.0833333"
}, {
    "name": "Maule",
    "lng": "-71.7000000",
    "lat": "-35.5333333"
}, {
    "name": "Pencahue",
    "lng": "-71.8166667",
    "lat": "-35.4000000"
}, {
    "name": "San Clemente",
    "lng": "-71.4833333",
    "lat": "-35.5500000"
}, {
    "name": "Cauquenes",
    "lng": "-72.3500000",
    "lat": "-35.9666667"
}, {
    "name": "Pelluhue",
    "lng": "-72.6333333",
    "lat": "-35.8333333"
}, {
    "name": "Hualañé",
    "lng": "-71.8047222",
    "lat": "-34.9766667"
}, {
    "name": "Molina",
    "lng": "-71.2833333",
    "lat": "-34.1166667"
}, {
    "name": "Romeral",
    "lng": "-71.1333333",
    "lat": "-34.9666667"
}, {
    "name": "Teno",
    "lng": "-71.1833333",
    "lat": "-34.8666667"
}, {
    "name": "Linares",
    "lng": "-71.6000000",
    "lat": "-35.8500000"
}, {
    "name": "Longaví",
    "lng": "-71.6833333",
    "lat": "-35.9666667"
}, {
    "name": "Retiro",
    "lng": "-71.7666667",
    "lat": "-36.0500000"
}, {
    "name": "Villa Alegre",
    "lng": "-71.7500000",
    "lat": "-35.6666667"
}, {
    "name": "Constitución",
    "lng": "-72.4166667",
    "lat": "-35.3333333"
}, {
    "name": "Empedrado",
    "lng": "-72.2833333",
    "lat": "-35.6000000"
}, {
    "name": "Pelarco",
    "lng": "-71.4500000",
    "lat": "-35.3833333"
}, {
    "name": "Río Claro",
    "lng": "-71.2666667",
    "lat": "-35.2833333"
}, {
    "name": "San Rafael",
    "lng": "-71.5333333",
    "lat": "-35.3166667"
}, {
    "name": "Curicó",
    "lng": "-71.2333333",
    "lat": "-34.9833333"
}, {
    "name": "Chanco",
    "lng": "-72.5333333",
    "lat": "-35.7333333"
}, {
    "name": "Licantén",
    "lng": "-72.0000000",
    "lat": "-34.9833333"
}, {
    "name": "Rauco",
    "lng": "-71.3166667",
    "lat": "-34.9333333"
}, {
    "name": "Sagrada Familia",
    "lng": "-71.3833333",
    "lat": "-35.0000000"
}, {
    "name": "Vichuquén",
    "lng": "-72.0000000",
    "lat": "-34.8833333"
}, {
    "name": "Colbún",
    "lng": "-71.4166667",
    "lat": "-35.7000000"
}, {
    "name": "Parral",
    "lng": "-71.8333333",
    "lat": "-36.1500000"
}, {
    "name": "San Javier",
    "lng": "-71.7500000",
    "lat": "-35.6000000"
}, {
    "name": "Yerbas Buenas",
    "lng": "-71.5833333",
    "lat": "-35.7500000"
}, {
    "name": "Concepción",
    "lng": "-73.0500000",
    "lat": "-36.8333333"
}, {
    "name": "Chiguayante",
    "lng": "-73.0166667",
    "lat": "-36.9166667"
}, {
    "name": "Hualqui",
    "lng": "-72.9333333",
    "lat": "-36.9666667"
}, {
    "name": "Penco",
    "lng": "-72.9833333",
    "lat": "-36.7333333"
}, {
    "name": "Santa Juana",
    "lng": "-72.9333333",
    "lat": "-37.1666667"
}, {
    "name": "Tomé",
    "lng": "-72.9500000",
    "lat": "-36.6166667"
}, {
    "name": "Lebu",
    "lng": "-73.6500000",
    "lat": "-37.6166667"
}, {
    "name": "Cañete",
    "lng": "-73.3833333",
    "lat": "-37.8000000"
}, {
    "name": "Curanilahue",
    "lng": "-73.3500000",
    "lat": "-37.4666667"
}, {
    "name": "Tirúa",
    "lng": "-73.5000000",
    "lat": "-38.3333333"
}, {
    "name": "Antuco",
    "lng": "-71.6833333",
    "lat": "-37.3333333"
}, {
    "name": "Laja",
    "lng": "-72.7000000",
    "lat": "-37.2666667"
}, {
    "name": "Nacimiento",
    "lng": "-72.6666667",
    "lat": "-37.5000000"
}, {
    "name": "Quilaco",
    "lng": "-71.9833333",
    "lat": "-37.6666667"
}, {
    "name": "San Rosendo",
    "lng": "-72.7166667",
    "lat": "-37.2666667"
}, {
    "name": "Tucapel",
    "lng": "-71.9500000",
    "lat": "-37.2833333"
}, {
    "name": "Alto Biobío",
    "lng": "-71.3166667",
    "lat": "-38.0500000"
}, {
    "name": "Bulnes",
    "lng": "-72.3014290",
    "lat": "-36.7419870"
}, {
    "name": "Coelemu",
    "lng": "-72.7000000",
    "lat": "-36.4833333"
}, {
    "name": "Chillán Viejo",
    "lng": "-72.1333333",
    "lat": "-36.6166667"
}, {
    "name": "Ninhue",
    "lng": "-72.4000000",
    "lat": "-36.4000000"
}, {
    "name": "Pemuco",
    "lng": "-72.1000000",
    "lat": "-36.9666667"
}, {
    "name": "Portezuelo",
    "lng": "-72.4333333",
    "lat": "-36.5333333"
}, {
    "name": "Quirihue",
    "lng": "-72.5333333",
    "lat": "-36.2833333"
}, {
    "name": "Treguaco",
    "lng": "-72.6666667",
    "lat": "-36.4333333"
}, {
    "name": "San Ignacio",
    "lng": "-72.0333333",
    "lat": "-36.8000000"
}, {
    "name": "San Carlos",
    "lng": "-71.9580556",
    "lat": "-36.4247222"
}, {
    "name": "Yungay",
    "lng": "-72.0166667",
    "lat": "-37.1166667"
}, {
    "name": "San Nicolás",
    "lng": "-72.2166667",
    "lat": "-36.5000000"
}, {
    "name": "San Fabián",
    "lng": "-71.5500000",
    "lat": "-36.5500000"
}, {
    "name": "Ránquil",
    "lng": "-72.5500000",
    "lat": "-36.6500000"
}, {
    "name": "Quillón",
    "lng": "-72.4666667",
    "lat": "-36.7333333"
}, {
    "name": "Pinto",
    "lng": "-71.9000000",
    "lat": "-36.7000000"
}, {
    "name": "Ñiquén",
    "lng": "-71.9000000",
    "lat": "-36.3000000"
}, {
    "name": "El Carmen",
    "lng": "-72.0323130",
    "lat": "-36.8994440"
}, {
    "name": "Coihueco",
    "lng": "-71.8333333",
    "lat": "-36.6166667"
}, {
    "name": "Cobquecura",
    "lng": "-72.7833333",
    "lat": "-36.1333333"
}, {
    "name": "Chillán",
    "lng": "-72.1166667",
    "lat": "-36.6000000"
}, {
    "name": "Yumbel",
    "lng": "-72.5333333",
    "lat": "-37.1333333"
}, {
    "name": "Santa Bárbara",
    "lng": "-72.0166667",
    "lat": "-37.6666667"
}, {
    "name": "Quilleco",
    "lng": "-71.9666667",
    "lat": "-37.4666667"
}, {
    "name": "Negrete",
    "lng": "-72.5166667",
    "lat": "-37.5833333"
}, {
    "name": "Mulchén",
    "lng": "-72.2333333",
    "lat": "-37.7166667"
}, {
    "name": "Cabrero",
    "lng": "-72.4000000",
    "lat": "-37.0333333"
}, {
    "name": "Los Angeles",
    "lng": "-72.3500000",
    "lat": "-37.4666667"
}, {
    "name": "Los Alamos",
    "lng": "-73.4666667",
    "lat": "-37.6166667"
}, {
    "name": "Contulmo",
    "lng": "-73.2333333",
    "lat": "-38.0000000"
}, {
    "name": "Arauco",
    "lng": "-73.3166667",
    "lat": "-37.2500000"
}, {
    "name": "Hualpén",
    "lng": "-73.0833333",
    "lat": "-36.7833333"
}, {
    "name": "Talcahuano",
    "lng": "-73.1166667",
    "lat": "-36.7166667"
}, {
    "name": "San Pedro de la Paz",
    "lng": "-73.1166667",
    "lat": "-36.8333333"
}, {
    "name": "Lota",
    "lng": "-73.1560560",
    "lat": "-37.0870730"
}, {
    "name": "Florida",
    "lng": "-72.6666667",
    "lat": "-36.8166667"
}, {
    "name": "Coronel",
    "lng": "-73.1333333",
    "lat": "-37.0166667"
}, {
    "name": "Temuco",
    "lng": "-72.6666667",
    "lat": "-38.7500000"
}, {
    "name": "Cunco",
    "lng": "-72.0333333",
    "lat": "-38.9166667"
}, {
    "name": "Freire",
    "lng": "-72.6333333",
    "lat": "-38.9500000"
}, {
    "name": "Gorbea",
    "lng": "-72.6833333",
    "lat": "-39.1000000"
}, {
    "name": "Loncoche",
    "lng": "-72.6333333",
    "lat": "-39.3666667"
}, {
    "name": "Nueva Imperial",
    "lng": "-72.9500000",
    "lat": "-38.7333333"
}, {
    "name": "Perquenco",
    "lng": "-72.3833333",
    "lat": "-38.4166667"
}, {
    "name": "Pucón",
    "lng": "-71.9666667",
    "lat": "-39.2666667"
}, {
    "name": "Teodoro Schmidt",
    "lng": "-73.0500000",
    "lat": "-38.9666667"
}, {
    "name": "Vilcún",
    "lng": "-72.3794444",
    "lat": "-39.1183333"
}, {
    "name": "Cholchol",
    "lng": "-72.8500000",
    "lat": "-38.6000000"
}, {
    "name": "Collipulli",
    "lng": "-72.4333333",
    "lat": "-37.9500000"
}, {
    "name": "Ercilla",
    "lng": "-72.3833333",
    "lat": "-38.0500000"
}, {
    "name": "Los Sauces",
    "lng": "-72.8333333",
    "lat": "-37.9666667"
}, {
    "name": "Purén",
    "lng": "-73.0833333",
    "lat": "-38.0166667"
}, {
    "name": "Traiguén",
    "lng": "-72.6833333",
    "lat": "-38.2500000"
}, {
    "name": "Carahue",
    "lng": "-73.1666667",
    "lat": "-38.7000000"
}, {
    "name": "Curarrehue",
    "lng": "-71.5833333",
    "lat": "-39.3500000"
}, {
    "name": "Galvarino",
    "lng": "-72.7833333",
    "lat": "-38.4000000"
}, {
    "name": "Lautaro",
    "lng": "-72.4350000",
    "lat": "-38.5291667"
}, {
    "name": "Padre Las Casas",
    "lng": "-72.6000000",
    "lat": "-38.7666667"
}, {
    "name": "Pitrufquén",
    "lng": "-72.6500000",
    "lat": "-38.9833333"
}, {
    "name": "Toltén",
    "lng": "-73.2333333",
    "lat": "-39.2166667"
}, {
    "name": "Villarrica",
    "lng": "-72.2166667",
    "lat": "-39.2666667"
}, {
    "name": "Angol",
    "lng": "-72.7166667",
    "lat": "-37.8000000"
}, {
    "name": "Curacautín",
    "lng": "-71.8833333",
    "lat": "-38.4333333"
}, {
    "name": "Lonquimay",
    "lng": "-71.2333333",
    "lat": "-38.4333333"
}, {
    "name": "Lumaco",
    "lng": "-72.9166667",
    "lat": "-38.1500000"
}, {
    "name": "Renaico",
    "lng": "-72.5833333",
    "lat": "-37.6666667"
}, {
    "name": "Victoria",
    "lng": "-72.3333333",
    "lat": "-38.2166667"
}, {
    "name": "Saavedra",
    "lng": "-73.4000000",
    "lat": "-38.7833333"
}, {
    "name": "Melipeuco",
    "lng": "-71.7000000",
    "lat": "-38.8500000"
}, {
    "name": "Valdivia",
    "lng": "-73.2333333",
    "lat": "-39.8000000"
}, {
    "name": "Corral",
    "lng": "-73.4333333",
    "lat": "-39.8666667"
}, {
    "name": "Lanco",
    "lng": "-72.7666667",
    "lat": "-39.4333333"
}, {
    "name": "Los Lagos",
    "lng": "-72.8333333",
    "lat": "-39.8500000"
}, {
    "name": "Máfil",
    "lng": "-72.9500000",
    "lat": "-39.6500000"
}, {
    "name": "Mariquina",
    "lng": "-72.9666667",
    "lat": "-39.5166667"
}, {
    "name": "Paillaco",
    "lng": "-72.8833333",
    "lat": "-40.0666667"
}, {
    "name": "Panguipulli",
    "lng": "-72.3333333",
    "lat": "-39.6333333"
}, {
    "name": "La Unión",
    "lng": "-73.0833333",
    "lat": "-40.2833333"
}, {
    "name": "Futrono",
    "lng": "-72.4000000",
    "lat": "-40.1333333"
}, {
    "name": "Lago Ranco",
    "lng": "-72.5000000",
    "lat": "-40.3166667"
}, {
    "name": "Río Bueno",
    "lng": "-72.9666667",
    "lat": "-40.3166667"
}, {
    "name": "Puerto Montt",
    "lng": "-72.9333333",
    "lat": "-41.4666667"
}, {
    "name": "Cochamó",
    "lng": "-72.3166667",
    "lat": "-41.5000000"
}, {
    "name": "Frutillar",
    "lng": "-73.1000000",
    "lat": "-41.1166667"
}, {
    "name": "Puerto Varas",
    "lng": "-72.9833333",
    "lat": "-41.3166667"
}, {
    "name": "Ancud",
    "lng": "-73.8333333",
    "lat": "-41.8666667"
}, {
    "name": "Curaco de Vélez",
    "lng": "-73.5833333",
    "lat": "-42.4333333"
}, {
    "name": "Puqueldón",
    "lng": "-73.6333333",
    "lat": "-42.5833333"
}, {
    "name": "Quellón",
    "lng": "-73.6000000",
    "lat": "-43.1000000"
}, {
    "name": "Quinchao",
    "lng": "-73.4166667",
    "lat": "-42.5333333"
}, {
    "name": "Puerto Octay",
    "lng": "-72.9000000",
    "lat": "-40.9666667"
}, {
    "name": "Puyehue",
    "lng": "-72.6166667",
    "lat": "-40.6666667"
}, {
    "name": "Hualaihué",
    "lng": "-72.6833333",
    "lat": "-42.0166667"
}, {
    "name": "Chaitén",
    "lng": "-72.7088889",
    "lat": "-42.9194444"
}, {
    "name": "San Juan de la Costa",
    "lng": "-73.4000000",
    "lat": "-40.5166667"
}, {
    "name": "Llanquihue",
    "lng": "-73.0166667",
    "lat": "-41.2500000"
}, {
    "name": "Calbuco",
    "lng": "-73.1333333",
    "lat": "-41.7666667"
}, {
    "name": "Fresia",
    "lng": "-73.4500000",
    "lat": "-41.1500000"
}, {
    "name": "Los Muermos",
    "lng": "-73.4833333",
    "lat": "-41.4000000"
}, {
    "name": "Maullín",
    "lng": "-73.6000000",
    "lat": "-41.6166667"
}, {
    "name": "Castro",
    "lng": "-73.8000000",
    "lat": "-42.4666667"
}, {
    "name": "Queilén",
    "lng": "-73.4666667",
    "lat": "-42.8666667"
}, {
    "name": "Quemchi",
    "lng": "-73.5166667",
    "lat": "-42.1333333"
}, {
    "name": "Osorno",
    "lng": "-73.1500000",
    "lat": "-40.5666667"
}, {
    "name": "Purranque",
    "lng": "-73.1666667",
    "lat": "-40.9166667"
}, {
    "name": "Río Negro",
    "lng": "-73.2333333",
    "lat": "-40.7833333"
}, {
    "name": "San Pablo",
    "lng": "-73.0166667",
    "lat": "-40.4000000"
}, {
    "name": "Futaleufú",
    "lng": "-71.8500000",
    "lat": "-43.1666667"
}, {
    "name": "Palena",
    "lng": "-71.8000000",
    "lat": "-43.6166667"
}, {
    "name": "Dalcahue",
    "lng": "-73.7000000",
    "lat": "-42.3666667"
}, {
    "name": "Chonchi",
    "lng": "-73.8166667",
    "lat": "-42.6166667"
}, {
    "name": "Coyhaique",
    "lng": "-72.0666667",
    "lat": "-45.5666667"
}, {
    "name": "Aisén",
    "lng": "-72.7000000",
    "lat": "-45.4000000"
}, {
    "name": "Guaitecas",
    "lng": "-73.7333333",
    "lat": "-43.8833333"
}, {
    "name": "O'Higgins",
    "lng": "-72.5666667",
    "lat": "-48.4666667"
}, {
    "name": "Chile Chico",
    "lng": "-71.7333333",
    "lat": "-46.5500000"
}, {
    "name": "Verde",
    "lng": "-71.8333333",
    "lat": "-44.2333333"
}, {
    "name": "Cisnes",
    "lng": "-72.7000000",
    "lat": "-44.7500000"
}, {
    "name": "Cochrane",
    "lng": "-72.5500000",
    "lat": "-47.2666667"
}, {
    "name": "Tortel",
    "lng": "-73.5666667",
    "lat": "-47.8333333"
}, {
    "name": "Río Ibáñez",
    "lng": "-71.9333333",
    "lat": "-46.3000000"
}, {
    "name": "Punta Arenas",
    "lng": "-70.9336111",
    "lat": "-53.1669444"
}, {
    "name": "Río Verde",
    "lng": "-71.4833333",
    "lat": "-52.6500000"
}, {
    "name": "Cabo de Hornos (Ex-Navarino)",
    "lng": "-67.6166667",
    "lat": "-54.9333333"
}, {
    "name": "Porvenir",
    "lng": "-70.3666667",
    "lat": "-53.3000000"
}, {
    "name": "Timaukel",
    "lng": "-69.9000000",
    "lat": "-53.6666667"
}, {
    "name": "Torres del Paine",
    "lng": "-72.3500000",
    "lat": "-51.2666667"
}, {
    "name": "Natales",
    "lng": "-72.5166667",
    "lat": "-51.7333333"
}, {
    "name": "Primavera",
    "lng": "-69.2500000",
    "lat": "-52.7166667"
}, {
    "name": "Antártica",
    "lng": "-71.5000000",
    "lat": "-75.0000000"
}, {
    "name": "San Gregorio",
    "lng": "-69.6833333",
    "lat": "-52.3166667"
}, {
    "name": "Laguna Blanca",
    "lng": "-71.9166667",
    "lat": "-52.2500000"
}]