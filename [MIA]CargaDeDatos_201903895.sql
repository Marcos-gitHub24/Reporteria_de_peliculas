-- PARA INSERTAR PAISES
INSERT INTO Pais (pais)
SELECT DISTINCT NOMBRE 
FROM 
( 
SELECT DISTINCT PAIS_CLIENTE AS NOMBRE
FROM Temporal 
UNION 
SELECT DISTINCT PAIS_EMPLEADO AS NOMBRE
FROM Temporal
UNION
SELECT DISTINCT PAIS_TIENDA AS NOMBRE
FROM TEMPORAL
) AS JA
WHERE NOMBRE IS NOT NULL;

-- PARA INSERTAR CATEGORIAS
INSERT INTO CATEGORIA (categoria)
SELECT DISTINCT CATEGORIA_PELICULA
FROM TEMPORAL WHERE CATEGORIA_PELICULA IS NOT NULL;

-- PARA INSERTAR ACTORES 
INSERT INTO Actor (nombre, apellido)
SELECT DISTINCT
(SELECT SPLIT_PART(actor_pelicula, ' ', 1)) AS nombre,
(SELECT SPLIT_PART(actor_pelicula, ' ', 2)) AS apellido
FROM Temporal WHERE actor_pelicula IS NOT NULL;
        

-- PARA INSERTAR IDIOMAS
INSERT INTO Idioma (idioma)
SELECT DISTINCT lenguaje_pelicula
FROM Temporal WHERE lenguaje_pelicula IS NOT NULL;

-- PARA INSERTAR TIENDAS 
INSERT INTO Tienda (nombre, direccion, gerente)
SELECT DISTINCT nombre_tienda, direccion_tienda, encargado_tienda
FROM Temporal WHERE nombre_tienda IS NOT NULL
ORDER BY nombre_tienda ASC;




-- PARA INSERTAR CIUDADES
INSERT INTO CIUDAD (ciudad, codigo_postal, id_pais)
SELECT NOMBRE_CIUDAD, CODIGO_POSTAL, ID_PAIS
FROM
(
SELECT DISTINCT  CIUDAD_EMPLEADO AS NOMBRE_CIUDAD, CODIGO_POSTAL_EMPLEADO AS CODIGO_POSTAL, ID_PAIS
FROM TEMPORAL
INNER JOIN 
PAIS
ON 
PAIS_EMPLEADO = pais
UNION
SELECT DISTINCT  CIUDAD_TIENDA AS NOMBRE_CIUDAD, CODIGO_POSTAL_TIENDA AS CODIGO_POSTAL, ID_PAIS
FROM TEMPORAL
INNER JOIN 
PAIS
ON 
PAIS_TIENDA = pais
UNION
SELECT DISTINCT  CIUDAD_CLIENTE AS NOMBRE_CIUDAD, CODIGO_POSTAL_CLIENTE AS CODIGO_POSTAL, ID_PAIS
FROM TEMPORAL
INNER JOIN 
PAIS
ON 
PAIS_CLIENTE = pais
) AS M
WHERE NOMBRE_CIUDAD IS NOT NULL;

-- PARA EMPLEADOS
INSERT INTO Empleado (nombre, apellido, direccion, correo, empleado_activo, nombre_usuario, contrasena, id_tienda)
SELECT DISTINCT
(SELECT SPLIT_PART(nombre_empleado, ' ', 1)) AS NOMBRE,
(SELECT SPLIT_PART(nombre_empleado, ' ', 2)) AS APELLIDO,
direccion_empleado, correo_empleado, empleado_activo, usuario_empleado, contrasena_empleado, id_tienda
FROM Temporal
INNER JOIN 
Ciudad
ON ciudad_empleado = Ciudad.ciudad
INNER JOIN 
Tienda 
ON tienda_empleado = Tienda.nombre;


-- CLIENTES
INSERT INTO Cliente (nombre, apellido, correo, fecha_registro, cliente_activo, direccion, id_tienda, id_ciudad)
SELECT * FROM 
(SELECT DISTINCT
(SELECT SPLIT_PART(NOMBRE_CLIENTE, ' ', 1)) AS NOMBRE,
(SELECT SPLIT_PART(NOMBRE_CLIENTE, ' ', 2)) AS APELLIDO,
CORREO_CLIENTE, FECHA_CREACION,  CLIENTE_ACTIVO, DIRECCION_CLIENTE ,  Tienda.id_tienda, Ciudad.id_ciudad
FROM Temporal
INNER JOIN Ciudad 
ON CIUDAD_CLIENTE = Ciudad.ciudad AND CODIGO_POSTAL_CLIENTE = Ciudad.codigo_postal
INNER JOIN Tienda 
ON 
TIENDA_PREFERIDA = Tienda.nombre
INNER JOIN Pais 
ON 
Pais.pais = PAIS_CLIENTE and Ciudad.id_pais = Pais.id_pais
WHERE FECHA_CREACION IS NOT NULL AND NOMBRE_CLIENTE IS NOT NULL 
ORDER BY NOMBRE ASC
) foo;


-- PARA PELICULAS
INSERT INTO PELICULA (titulo, descripcion, clasificacion, ano_lanzamiento, duracion, cantidad_dia_renta, costo_renta, costo_mal_estado)
SELECT DISTINCT nombre_pelicula, descripcion_pelicula, clasificacion , ano_lanzamiento, duracion, dias_renta, costo_renta, 
costo_por_dano
FROM TEMPORAL
WHERE NOMBRE_PELICULA IS NOT NULL;

-- PARA PELICULA-CATEGORIA
INSERT INTO Pelicula_categoria (id_categoria, id_pelicula)
SELECT DISTINCT id_categoria, id_pelicula
FROM TEMPORAL
INNER JOIN 
Categoria
ON
categoria_pelicula = Categoria.categoria
INNER JOIN 
PELICULA
ON
nombre_pelicula = Pelicula.titulo;


-- PARA PELICULA-ACTOR
INSERT INTO Pelicula_actor (id_pelicula, id_actor)
SELECT 
DISTINCT id_pelicula, id_actor 
FROM 
Temporal
INNER JOIN 
Actor
ON actor_pelicula = Actor.nombre || ' ' || Actor.apellido
INNER JOIN
Pelicula
ON nombre_pelicula = titulo;


-- PARA PELICULA-IDIOMA
INSERT INTO Pelicula_idioma (id_pelicula, id_idioma)
SELECT DISTINCT id_pelicula, id_idioma
FROM Temporal
INNER JOIN
Idioma
ON lenguaje_pelicula = idioma
INNER JOIN 
Pelicula
ON nombre_pelicula = titulo;

-- PARA PELICULA-TIENDA
INSERT INTO Tienda_pelicula (id_tienda, id_pelicula, copias)
SELECT DISTINCT id_tienda, id_pelicula, COUNT(*)
FROM Temporal 
INNER JOIN 
Tienda
ON tienda_pelicula = nombre
INNER JOIN
Pelicula
ON nombre_pelicula = titulo
GROUP BY id_tienda, id_pelicula;

-- PARA RENTAS

INSERT INTO RENTA (cantidad_pagar, fecha_entrega, fecha_devolver, id_cliente, id_empleado, id_pelicula)
SELECT DISTINCT monto_a_pagar, fecha_renta, fecha_retorno, id_cliente, id_empleado, id_pelicula
FROM Temporal
INNER JOIN 
Cliente
ON nombre_cliente = Cliente.nombre || ' ' || Cliente.apellido
INNER JOIN
Empleado 
ON nombre_empleado = Empleado.nombre || ' ' || Empleado.apellido
INNER JOIN 
Pelicula
ON nombre_pelicula = titulo
WHERE fecha_renta IS NOT NULL;
