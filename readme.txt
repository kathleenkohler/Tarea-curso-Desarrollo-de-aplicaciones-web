El zip contiene los 7 archivos html solicitados en el enunciado más un archivo .js por cada uno y 5 archivos css.
El archivo inicio.html contiene 4 botones que al apretarlos redirigen a lo que cada uno describe.
El primero que aparece envía a agregar donación, que contiene los datos solicitados y sus validaciones correspondientes en el archivo del mismo nombre en js. Además la vista contiene dos botones al final del formulario, uno para enviar la donación, el cual avisa de datos ingresados incorrectamente y luego pregunta por una confirmación antes de enviar los datos, el otro botón es para volver a la página de inicio del comienzo. El archivo agregar pedido es similar en presentación y en funcionamiento.
Luego tenemos los archivos html ver-pedidos y ver-donaciones a los cuales se llega con los otros botones que aparecen en el inicio. En estos se muestra una tabla con 5 filas, cada una con la información correspondiente solicitada en el enunciado, en ambas, al clickear en alguna fila se redirige a otra página que muestra la información completa de la primera fila del pedido o donación según corresponda, además de incluir ambas un botón para volver a la página inicial. En el archivo información donacion mencionado anteriormente, al clickear en la foto que se muestra, esta se agranda a un tamaño de 1280x1024, del cual se puede volver a lo original presionando la X que se muestra en la esquina superior derecha.
----------
tarea 2

La url para acceder a la pagina de inicio corresponde a http://127.0.0.1:5000/inicio,
Los archivos subidos en una donacion se guardan en la carpeta uploads.
En la carpeta database se encuentra todo lo relacionado a la base de datos, con las consultas en el archivo querys, sus ejecuciones en db.py y las tablas y los datos iniciales a cargar en los archivos .sql
En la carpeta statics se encuentran todos los archivos creados en la primera tarea .css y .js en sus respectivas carpetas.
En la carpeta templates se encuentran los archivos .html adaptados para esta tarea con el uso de flask.
Por ultimo en la carpeta utils se encuentra el archivo que realiza las validaciones del backend.
Además, fuera de las carpetas se encuentra el archivo app.py que corre la aplicación creada, definiendo sus rutas.

En las vistas de ver donaciones y ver pedidos, las flechas para cambiar de pagina se encuentran al lado izquierdo arriba de la linea del boton volver al inicio.

para obtener el id de una donacion, se asumió que sus atributos en conjunto son únicos.
---------------------------------
Tarea 3:

En la página de inicio debajo de los botones se muestra un mapa que contiene las últimas 5 donaciones, las cuales aparecen en color azul y los últimos 5 pedidos que aparecen con un marcador morado.
Al hacer click en el marcador de algún pedido se muestra el id de este, el tipo, la cantidad y el email del solicitante.
Al clickear en un marcador de una donación se muestra su id, la calle y número, tipo, cantidad, fecha de disponibilidad y el email del donante.
A la latitud y longitud de los pedidos se les agrego 0.001 para que no coincidieran con la posicion de las donaciones en la misma comuna. Pir lo anteior, con poco zoom los marcadores se pueden notar superpuestos, pero al acercarse se notan los dos correspondientes.
Para agrupar pedidos o donaciones dentro de una misma comuna se utilizaron markerClusters de leaflet.
(Se editaron los datos del json entregado que contiene la latitud y longitud de las comunas, corrigiendo las letras de las comunas con tilde y esto se pegó como una variable al final de app.py)
En la página de inicio tambien se muestra la opción "Ver Gráficos" la cual redirige a otra página donde se muestran dos gráficos de barras, uno para donaciones y otro para los pedidos.
Los gráficos anteriores muestran la cantidad de donaciones/pedidos por tipo (fruta, verdura u otro). Al poner el mouse sobre una barra se indica el número exacto de ese tipo correspondiente.
