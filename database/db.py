import pymysql
import json

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

with open('database/querys.json', 'r') as querys:
	QUERY_DICT = json.load(querys)


def get_conn():
	conn = pymysql.connect(
		db=DB_NAME,
		user=DB_USERNAME,
		passwd=DB_PASSWORD,
		host=DB_HOST,
		port=DB_PORT,
		charset=DB_CHARSET
	)
	return conn


def get_donacion_by_id(id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_donacion_by_id"], (id))
	donacion = cursor.fetchone()
	return donacion

def get_pedido_by_id(id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_pedido_by_id"], (id))
	pedido = cursor.fetchone()
	return pedido

def get_foto_by_donacion(donacion_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_foto_by_donacion"], (donacion_id))
	foto = cursor.fetchone()
	return foto

def get_Nfoto_by_donacion(donacion_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_Nfoto_by_donacion"], (donacion_id))
	foto = cursor.fetchone()
	return foto

def get_foto_by_id(id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_foto_by_id"], (id))
	foto = cursor.fetchone()
	return foto
	
def get_comuna_id(comuna):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_comuna_id"], (comuna,))
	id = cursor.fetchone()
	return id

def get_comuna_by_id(id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_comuna_by_id"], (id))
	comuna = cursor.fetchone()
	return comuna

def get_region_by_id(id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_region_by_id"], (id))
	region = cursor.fetchone()
	return region

def get_region_id_by_comuna(comunaid):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_region_id_by_comuna"], (comunaid))
	id = cursor.fetchone()
	return id

def get_id_donacion(comuna, calle, tipo, cantidad, descripcion, condiciones, nombre, email, celular):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_id_donacion"], (comuna, calle, tipo, cantidad, descripcion, condiciones, nombre, email, celular))
	id = cursor.fetchone()
	return id

def get_donaciones(page):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_donaciones"], (page))
	donaciones = cursor.fetchall()
	return donaciones

def get_pedidos(page):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_pedidos"], (page))
	pedidos = cursor.fetchall()
	return pedidos
	

def create_donacion(comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["create_donacion"], (comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular))
	conn.commit()

def create_pedido(comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["create_pedido"], (comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante))
	conn.commit()

def create_foto(ruta_archivo, nombre_archivo, donacion_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["create_foto"], (ruta_archivo, nombre_archivo, donacion_id))
	conn.commit()
	
def pedidos():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["pedidos"])
	pedidos = cursor.fetchall()
	return len(pedidos)

def donaciones():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["donaciones"])
	donaciones = cursor.fetchall()
	return len(donaciones)

def createfoto(path, img_filename, donacion_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["create_photo"], (path, img_filename, donacion_id))
	conn.commit()

def get_mapa_don():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_mapa_don"])
	donaciones = cursor.fetchall()
	return donaciones

def get_mapa_ped():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_mapa_ped"])
	pedidos = cursor.fetchall()
	return pedidos

def get_type_fruta_don():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_type_fruta_don"])
	donacion = cursor.fetchall()
	return len(donacion)

def get_type_verdura_don():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_type_verdura_don"])
	donacion = cursor.fetchall()
	return len(donacion)

def get_type_otro_don():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_type_otro_don"])
	donacion = cursor.fetchall()
	return len(donacion)

def get_type_fruta_ped():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_type_fruta_ped"])
	pedido = cursor.fetchall()
	return len(pedido)

def get_type_verdura_ped():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_type_verdura_ped"])
	pedido = cursor.fetchall()
	return len(pedido)

def get_type_otro_ped():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_type_otro_ped"])
	pedido = cursor.fetchall()
	return len(pedido)