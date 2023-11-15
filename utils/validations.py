import re
import filetype
import datetime
from database import db

#####
def validate_region(value):
    n = int(value) > 0 and int(value) < 17
    return value and n
#####
def validate_comuna(value):
    a = db.get_comuna_by_id(value)
    if len(a)==0:
        return False
    return value 

def validate_calle(value):
    a= bool(re.search(r"^[a-zA-Z\s]+[\d]+$", value))
    return value and a
######
def validate_tipo(value):
    if value == "fruta":
        return True
    elif value == "verdura":
        return True
    elif value == "otro":
        return True
    else:
        return False

def validate_cantidad(value):
    if int(value) <= 0:
        return False
    
    e =bool(re.search(r"^[A-Za-z0-9\s]+$", value))
    return value and e


def validate_fecha(value):
    l = len(value) == 10
    e = bool(re.search(r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$", value))

    date = datetime.date.today()
    year= date.year
    month = date.month
    day = date.day

    f = re.split(r'-', value)

    if (int(f[0]) < year):
        return False
    elif (int(f[0])== year):
        if (int(f[1])< month) :
            return False
        elif (int(f[1])== month) :
            if (int(f[3])< day) :
                return False
            
        
    return value and l and e

def validate_descripcion(value):
    l = len(value) <= 250

    e =bool(re.search(r"^[\w]+$", value))
    return value and l and e

def validate_condiciones(value):
    return True


def validate_nombre(value):
    l = len(value) <= 80 and len(value) >=3

    e =bool(re.search(r"[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+(?:\s+[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+){0,5}(?<!\s)$", value))
    return value and l and e 
    

def validate_email(value):
    e =bool(re.search(r"[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+(?:\s+[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+){0,5}(?<!\s)$", value))
    return value and e 

def validate_celular(value):
    l = len(value) >= 8

    e =bool(re.search(r"^[\d]+$", value))
    return value and l and e
    return True

def validate_foto(conf_img):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

    # check if a file was submitted
    if conf_img is None:
        return False

    # check if the browser submitted an empty file
    if conf_img.filename == "":
        return False
    
    # check file extension
    ftype_guess = filetype.guess(conf_img)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    # check mimetype
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True

def validate_foto2(conf_img):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

    # check if a file was submitted
    if conf_img is None:
        return True

    # check if the browser submitted an empty file
    if conf_img.filename == "":
        return True
    
    # check file extension
    ftype_guess = filetype.guess(conf_img)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    # check mimetype
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True




def validate_donacion(region,comuna,calle,tipo,cantidad,fecha,descripcion,condiciones,foto1,foto2,foto3,nombre,email,celular):
    r=validate_region(region)
    c=validate_comuna(comuna)
    ca=validate_calle(calle)
    t=validate_tipo(tipo)
    cant=validate_cantidad(cantidad)
    fe=validate_fecha(fecha)
    d=validate_descripcion(descripcion)
    cond=validate_condiciones(condiciones)
    f1=validate_foto(foto1)
    f2=validate_foto2(foto2)
    f3=validate_foto2(foto3)
    n=validate_nombre(nombre)
    e=validate_email(email)
    ce=validate_celular(celular)

    return r and c and ca and t and cant and fe and d and cond and f1 and f2 and f3 and n and e and ce

def validate_pedido(region,comuna,tipo,descripcion,cantidad,nombre,email,celular):
    r=validate_region(region)
    c=validate_comuna(comuna)
    t=validate_tipo(tipo)
    d=validate_descripcion(descripcion)
    cant=validate_cantidad(cantidad)
    n=validate_nombre(nombre)
    e=validate_email(email)
    ce=validate_celular(celular)
    return r and c and t and d and cant and n and e and ce