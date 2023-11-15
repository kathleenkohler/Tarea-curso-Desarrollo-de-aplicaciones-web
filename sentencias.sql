-- DONACION
-- insertar donación
INSERT INTO donacion (comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
-- obtener información de 5 primeras donaciones
SELECT id, comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular FROM donacion ORDER BY id DESC LIMIT 0,5  
-- obtener información de las 5 segundas donaciones (página 2 de donaciones)
SELECT id, comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular FROM donacion ORDER BY id DESC LIMIT 5,5  
-- obtener información de una donación usando ID
SELECT id, comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular FROM donacion WHERE id=?

-- PEDIDO
-- insertar pedido
INSERT INTO pedido (comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante) VALUES (?, ?, ?, ?, ?, ?, ?);
-- obtener información de 5 primeros pedidos
SELECT id, comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante FROM pedido ORDER BY id DESC LIMIT 0,5
-- obtener información de 5 segundos pedidos (página 2 de pedidos)
SELECT id, comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante FROM pedido ORDER BY id DESC LIMIT 5,5
-- obtener información de un pedido usando ID
SELECT id, comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante FROM pedido WHERE id=?

-- FOTO
-- insertar foto
INSERT INTO foto (ruta_archivo, nombre_archivo, donacion_id) VALUES (?, ?, ?);
-- obtener fotos de una donación
SELECT id, ruta_archivo, nombre_archivo, donacion_id FROM foto WHERE donacion_id=?
-- obtener información de un archivo por id
SELECT id, ruta_archivo, nombre_archivo, donacion_id FROM foto WHERE id=?
