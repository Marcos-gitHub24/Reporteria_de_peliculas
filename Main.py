from flask import Flask, jsonify
import psycopg2
app = Flask(__name__)
 
@app.route("/")
def hello():
    resultado = '<Table border=1> <tr><td><b>Manejo e Implementación de Archivos</b></td><td><b>Practica 1</b></td></tr>'
    resultado = resultado + '<tr><td>José Marcos García Olmino</td><td>201903895</td></tr></Table>'
    return resultado

@app.route("/cargarTemporal")
def temporal():
    con = psycopg2.connect(
    host = "localhost",
    database = "practica",
    user = "user1",
    password = "1234"
    )
    cur = con.cursor()
    cur.execute("COPY temporal FROM '/home/marcos/Practica1/BlockbusterData.csv' (FORMAT 'csv', DELIMITER ';', NULL '-', HEADER 'true');commit;")
    cur.close()
    con.close()
    return "Datos cargados a la tabla temporal"

@app.route("/cargarModelo")
def modelo():
    con = psycopg2.connect(
    host = "localhost",
    database = "practica",
    user = "user1",
    password = "1234"
    )
    # CREACIOND DE LAS TABLAS
    cur = con.cursor()
    consulta = '''
        CREATE TABLE Pais(
        id_pais SERIAL PRIMARY KEY,
        pais VARCHAR(50) NOT NULL
        );

        CREATE TABLE Idioma(
            id_idioma SERIAL PRIMARY KEY,
            idioma VARCHAR(20) NOT NULL
        );

        CREATE TABLE Categoria(
            id_categoria SERIAL PRIMARY KEY,
            categoria VARCHAR(20) NOT NULL
        );

        CREATE TABLE Actor (
            id_actor SERIAL PRIMARY KEY,
            nombre VARCHAR(30),
            apellido VARCHAR(30)
        );

        CREATE TABLE Tienda (
            id_tienda SERIAL PRIMARY KEY,
            nombre VARCHAR(30),
            direccion VARCHAR(40),
            gerente VARCHAR(30)
        );

        CREATE TABLE Ciudad(
            id_ciudad SERIAL PRIMARY KEY,
            ciudad VARCHAR(30) NOT NULL,
            codigo_postal VARCHAR(5),
            id_pais INT NOT NULL,
            CONSTRAINT fk_id_pais
            FOREIGN KEY (id_pais)
            REFERENCES pais(id_pais)
        );

        CREATE TABLE Cliente (
            id_cliente SERIAL PRIMARY KEY,
            nombre VARCHAR(30) NOT NULL,
            apellido VARCHAR(30) NOT NULL,
            correo VARCHAR(50) NOT NULL,
            fecha_registro TIMESTAMP NOT NULL,
            cliente_activo VARCHAR(2) NOT NULL,
            direccion VARCHAR(75) NOT NULL,
            id_tienda INT NOT NULL,
            id_ciudad INT NOT NULL,
            CONSTRAINT fk_id_tienda
            FOREIGN KEY (id_tienda)
            REFERENCES Tienda(id_tienda),
            CONSTRAINT fk_id_ciudad
            FOREIGN KEY (id_ciudad)
            REFERENCES Ciudad(id_ciudad)
        );

        CREATE TABLE Empleado (
            id_empleado SERIAL PRIMARY KEY,
            nombre VARCHAR(30) NOT NULL,
            apellido VARCHAR(30) NOT NULL,
            direccion VARCHAR(75) NOT NULL,
            correo VARCHAR(30) NOT NULL,
            empleado_activo VARCHAR(2) NOT NULL,
            nombre_usuario VARCHAR(30) NOT NULL,
            contrasena VARCHAR(50) NOT NULL,
            id_tienda INT NOT NULL,
            CONSTRAINT fk_id_tienda
            FOREIGN KEY (id_tienda)
            REFERENCES Tienda(id_tienda)
        );

        CREATE TABLE Pelicula (
            id_pelicula SERIAL PRIMARY KEY,
            titulo VARCHAR(30) NOT NULL,
            descripcion VARCHAR(200) NOT NULL,
            clasificacion VARCHAR(5) NOT NULL,
            ano_lanzamiento VARCHAR(4) NOT NULL,
            duracion INT NOT NULL,
            cantidad_dia_renta INT NOT NULL,
            costo_renta DOUBLE PRECISION NOT NULL,
            costo_mal_estado DOUBLE PRECISION NOT NULL
        );

        CREATE TABLE Renta (
            id_renta SERIAL PRIMARY KEY,
            cantidad_pagar DOUBLE PRECISION NOT NULL,
            fecha_entrega TIMESTAMP,
            fecha_devolver TIMESTAMP,
            id_cliente INT NOT NULL,
            id_empleado INT NOT NULL,
            id_pelicula INT NOT NULL,

            CONSTRAINT fk_id_cliente
            FOREIGN KEY (id_cliente)
            REFERENCES Cliente(id_cliente),

            CONSTRAINT fk_id_empleado
            FOREIGN KEY (id_empleado)
            REFERENCES Empleado(id_empleado),

            CONSTRAINT fk_id_pelicula
            FOREIGN KEY (id_pelicula)
            REFERENCES Pelicula(id_pelicula)
        );


        CREATE TABLE Pelicula_idioma (
            id_pelicula_idioma SERIAL PRIMARY KEY,
            id_pelicula INT NOT NULL,
            id_idioma INT NOT NULL,

            CONSTRAINT fk_id_pelicula
            FOREIGN KEY (id_pelicula)
            REFERENCES Pelicula(id_pelicula),

            CONSTRAINT fk_id_idioma
            FOREIGN KEY (id_idioma)
            REFERENCES Idioma(id_idioma)
        );

        CREATE TABLE Tienda_pelicula (
            id_tienda_pelicula SERIAL PRIMARY KEY,
            id_tienda INT NOT NULL,
            id_pelicula INT NOT NULL,
            copias INT NOT NULL,

            CONSTRAINT fk_id_tienda
            FOREIGN KEY (id_tienda)
            REFERENCES Tienda(id_tienda),

            CONSTRAINT fk_id_pelicula
            FOREIGN KEY (id_pelicula)
            REFERENCES Pelicula(id_pelicula)
        );

        CREATE TABLE Pelicula_categoria (
            id_pelicula_categoria SERIAL PRIMARY KEY,
            id_categoria INT NOT NULL,
            id_pelicula INT NOT NULL,

            CONSTRAINT fk_id_categoria
            FOREIGN KEY (id_categoria)
            REFERENCES Categoria(id_categoria),

            CONSTRAINT fk_id_pelicula
            FOREIGN KEY (id_pelicula)
            REFERENCES Pelicula(id_pelicula)
        );

        CREATE TABLE Pelicula_actor (
            id_pelicula_actor SERIAL PRIMARY KEY,
            id_pelicula INT NOT NULL,
            id_actor INT NOT NULL,

            CONSTRAINT fk_id_actor
            FOREIGN KEY (id_actor)
            REFERENCES Actor(id_actor),

            CONSTRAINT fk_id_pelicula
            FOREIGN KEY (id_pelicula)
            REFERENCES Pelicula(id_pelicula)
        );
        commit;
    '''
    cur.execute(consulta)
    cur.close()
    # CARGA DE LOS DATOS
    cur = con.cursor()
    consulta2 = '''
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

        INSERT INTO CATEGORIA (categoria)
        SELECT DISTINCT CATEGORIA_PELICULA
        FROM TEMPORAL WHERE CATEGORIA_PELICULA IS NOT NULL;

        INSERT INTO Actor (nombre, apellido)
        SELECT DISTINCT
        (SELECT SPLIT_PART(actor_pelicula, ' ', 1)) AS nombre,
        (SELECT SPLIT_PART(actor_pelicula, ' ', 2)) AS apellido
        FROM Temporal WHERE actor_pelicula IS NOT NULL;
        
        INSERT INTO Idioma (idioma)
        SELECT DISTINCT lenguaje_pelicula
        FROM Temporal WHERE lenguaje_pelicula IS NOT NULL;

        INSERT INTO Tienda (nombre, direccion, gerente)
        SELECT DISTINCT nombre_tienda, direccion_tienda, encargado_tienda
        FROM Temporal WHERE nombre_tienda IS NOT NULL
        ORDER BY nombre_tienda ASC;

        INSERT INTO CIUDAD (ciudad, codigo_postal, id_pais)
        SELECT NOMBREC, CODIGO_POSTAL, ID_PAIS
        FROM
        (
        SELECT DISTINCT  CIUDAD_EMPLEADO AS NOMBREC, CODIGO_POSTAL_EMPLEADO AS CODIGO_POSTAL, ID_PAIS
        FROM TEMPORAL
        INNER JOIN 
        PAIS
        ON 
        PAIS_EMPLEADO = pais
        UNION
        SELECT DISTINCT  CIUDAD_TIENDA AS NOMBREC, CODIGO_POSTAL_TIENDA AS CODIGO_POSTAL, ID_PAIS
        FROM TEMPORAL
        INNER JOIN 
        PAIS
        ON 
        PAIS_TIENDA = pais
        UNION
        SELECT DISTINCT  CIUDAD_CLIENTE AS NOMBREC, CODIGO_POSTAL_CLIENTE AS CODIGO_POSTAL, ID_PAIS
        FROM TEMPORAL
        INNER JOIN 
        PAIS
        ON 
        PAIS_CLIENTE = pais
        ) AS M
        WHERE NOMBREC IS NOT NULL;

        INSERT INTO Empleado (nombre, apellido, direccion, correo, empleado_activo, nombre_usuario, contrasena, id_tienda)
        SELECT DISTINCT
        (SELECT SPLIT_PART(nombre_empleado, ' ', 1)) AS NOMBRE,
        (SELECT SPLIT_PART(nombre_empleado, ' ', 2)) AS APELLIDO,
        direccion_empleado, correo_empleado, empleado_activo, usuario_empleado, contrasena_empleado, id_tienda
        FROM Temporal
        INNER JOIN 
        Ciudad
        ON 
        ciudad_empleado = Ciudad.ciudad
        INNER JOIN 
        Tienda
        ON 
        tienda_empleado = Tienda.nombre;

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

        INSERT INTO PELICULA (titulo, descripcion, clasificacion, ano_lanzamiento, duracion, cantidad_dia_renta, costo_renta, costo_mal_estado)
        SELECT DISTINCT nombre_pelicula, descripcion_pelicula, clasificacion , ano_lanzamiento, duracion, dias_renta, costo_renta, 
        costo_por_dano
        FROM TEMPORAL
        WHERE NOMBRE_PELICULA IS NOT NULL;


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


        INSERT 
        INTO Pelicula_actor (id_pelicula, id_actor)
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

        INSERT INTO Pelicula_idioma (id_pelicula, id_idioma)
        SELECT DISTINCT id_pelicula, id_idioma
        FROM Temporal
        INNER JOIN
        Idioma
        ON lenguaje_pelicula = idioma
        INNER JOIN 
        Pelicula
        ON nombre_pelicula = titulo;


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
        commit;
    '''
    cur.execute(consulta2)
    cur.close()
    con.close()
    return "Modelo cargado con éxito"

@app.route("/eliminarTemporal")
def eliminarTemporal():
    con = psycopg2.connect(
    host = "localhost",
    database = "practica",
    user = "user1",
    password = "1234"
    )
    consulta = '''
        TRUNCATE Temporal;
        commit;
    '''
    cur = con.cursor()
    cur.execute(consulta)
    cur.close()
    con.close()
    return "Se elimino la tabla temporal con éxito"

@app.route("/eliminarModelo")
def eliminarModelo():
    con = psycopg2.connect(
    host = "localhost",
    database = "practica",
    user = "user1",
    password = "1234"
    )
    consulta = '''
        DROP TABLE Pais CASCADE;
        DROP TABLE Idioma CASCADE;
        DROP TABLE Categoria CASCADE;
        DROP TABLE Actor CASCADE;
        DROP TABLE Tienda CASCADE;
        DROP TABLE Ciudad CASCADE;
        DROP TABLE Cliente CASCADE;
        DROP TABLE Empleado CASCADE;
        DROP TABLE Pelicula CASCADE;
        DROP TABLE Renta CASCADE;
        DROP TABLE Pelicula_idioma CASCADE;
        DROP TABLE Tienda_pelicula CASCADE;
        DROP TABLE Pelicula_categoria CASCADE;
        DROP TABLE Pelicula_actor CASCADE;
        commit;
    '''
    cur = con.cursor()
    cur.execute(consulta)
    cur.close()
    con.close()
    return "Se eliminó el modelo con éxito"

@app.route("/consulta1")
def consulta1():
    con = psycopg2.connect(
    host = "localhost",
    database = "practica",
    user = "user1",
    password = "1234"
    )
    cur = con.cursor()
    consulta = '''
        WITH peli AS (SELECT id_pelicula FROM Pelicula
        WHERE titulo = 'SUGAR WONKA')
        SELECT SUM(copias) AS copias FROM tienda_pelicula, peli
        WHERE tienda_pelicula.id_pelicula = peli.id_pelicula;
    '''
    cur.execute(consulta)
    rows = cur.fetchall()
    cur.close()
    con.close()
    resultado = "<Table border=1><tr><td><b>COPIAS</b></td></tr>" 
    resultado = resultado + "<tr><td>"+ str(rows[0][0])+"</td></tr>"
    resultado = resultado + '</Table>'
    return resultado

@app.route("/consulta2")
def consulta2():
    con = psycopg2.connect(
    host = "localhost",
    database = "practica",
    user = "user1",
    password = "1234"
    )
    cur = con.cursor()
    consulta = '''
       SELECT Cliente.nombre, Cliente.apellido, 
       TRUNC(SUM(Renta.cantidad_pagar)::DECIMAL,2) AS PAGO
       FROM  Renta, Cliente
       WHERE  REnta.id_cliente = Cliente.id_cliente
       GROUP BY Cliente.nombre, Cliente.apellido
       HAVING COUNT(*) >= 40;
    '''
    cur.execute(consulta)
    rows = cur.fetchall()
    cur.close()
    con.close()
    resultado = "<Table border=1><tr><td><b>NOMBRE</b></td><td><b>APELLIDO</b></td><td><b>PAGO</b></td></tr>" 
    for i in rows:
        resultado = resultado +'<tr><td>'+str(i[0]) + '</td><td>'+ str(i[1]) + '</td><td>'+ str(i[2]) + '</td></tr>' 
    resultado = resultado + '</Table>'
    return resultado


@app.route("/consulta3")
def consulta3():
    con = psycopg2.connect(
    host = "localhost",
    database = "practica",
    user = "user1",
    password = "1234"
    )
    cur = con.cursor()
    consulta = '''
        SELECT nombre || ' ' || apellido AS ACTORES FROM 
        Actor WHERE Actor.apellido LIKE '%son%'
        ORDER BY Actor.nombre ASC ;
    '''
    cur.execute(consulta)
    rows = cur.fetchall()
    cur.close()
    con.close()
    resultado = "<Table border=1><tr><td><b>ACTORES</b></td></tr>" 
    for i in rows:
        resultado = resultado + '<tr><td>' + str(i[0]) + '</td></tr>'
    resultado = resultado + '</Table>'
    return resultado


@app.route("/consulta4")
def consulta4():
    con = psycopg2.connect(
    host = "localhost",
    database = "practica",
    user = "user1",
    password = "1234"
    )
    cur = con.cursor()
    consulta = '''
        SELECT DISTINCT Actor.nombre, Actor.apellido, 
        Pelicula.ano_lanzamiento
        FROM Actor, Pelicula, Pelicula_actor 
        WHERE Pelicula.descripcion LIKE '%Crocodile%'
        AND Pelicula.descripcion LIKE '%Shark%'
        AND Pelicula_actor.id_actor = Actor.id_actor 
        AND Pelicula_actor.id_pelicula = Pelicula.id_pelicula
        ORDER BY Actor.apellido ASC;
    '''
    cur.execute(consulta)
    rows = cur.fetchall()
    cur.close()
    con.close()
    resultado = "<Table border=1><tr><td><b>NOMBRE</b></td><td><b>APELLIDO</b></td><td><b>AÑO_LANZAMIENTO</b></td></tr>" 
    for i in rows:
        resultado = resultado + '<tr><td>' +str(i[0]) + '</td><td>' + str(i[1]) + '</td><td>' + str(i[2]) + '</td></tr>' 
    resultado = resultado + '</Table>'
    return resultado

@app.route("/consulta5")
def consulta5():
    con = psycopg2.connect(
    host = "localhost",
    database = "practica",
    user = "user1",
    password = "1234"
    )
    cur = con.cursor()
    consulta = '''
        WITH rentas AS (SELECT Cliente.nombre, Cliente.apellido,
        Pais.pais, COUNT(*)
        FROM  Renta, Cliente, Pais, Ciudad
        WHERE  Renta.id_cliente = Cliente.id_cliente
        AND Ciudad.id_ciudad = Cliente.id_ciudad
        AND Ciudad.id_pais = Pais.id_pais
        GROUP BY Cliente.nombre, Cliente.apellido, Pais.pais),

        maxi As (SELECT * FROM rentas WHERE count = (
            SELECT MAX (count)
            FROM rentas
        )),

        total AS (SELECT SUM(rentas.count) FROM
        rentas, maxi WHERE rentas.pais = maxi.pais
        )
        SELECT rentas.pais, rentas.nombre, 
        TRUNC((maxi.count/total.sum)*100,2) AS Porcentaje
        FROM total, maxi, rentas 
        WHERE rentas.nombre = maxi.nombre;
    '''
    cur.execute(consulta)
    rows = cur.fetchall()
    cur.close()
    con.close()
    resultado = "<Table border=1><tr><td><b>NOMBRE</b></td><td><b>APELLIDO</b></td><td><b>PORCENTAJE</b></td></tr>" 
    for i in rows:
        resultado = resultado + '<tr><td>' +str(i[0]) + '</td><td>' + str(i[1]) + '</td><td>' + str(i[2]) + '</td></tr>'
    resultado = resultado + '</Table>'
    return resultado

@app.route("/consulta6")
def consulta6():
    con = psycopg2.connect(
    host = "localhost",
    database = "practica",
    user = "user1",
    password = "1234"
    )
    cur = con.cursor()
    consulta = '''
        WITH total_pais AS (SELECT Pais.id_pais,Pais.pais,COUNT(*)::DECIMAL  
        FROM  Pais, Ciudad, Cliente
        WHERE Pais.id_pais = Ciudad.id_pais
        AND Cliente.id_ciudad = Ciudad.id_ciudad
        GROUP BY Pais.id_pais, Pais.pais),

        total_ciudad AS (SELECT Ciudad.id_pais, Ciudad.ciudad, COUNT(*)::DECIMAL
        FROM Ciudad, Cliente,  Pais
        WHERE Cliente.id_ciudad = Ciudad.id_ciudad
        AND Pais.id_pais = Ciudad.id_pais
        GROUP BY Ciudad.id_pais, Ciudad.ciudad)

        SELECT total_pais.pais, total_ciudad.ciudad,
        total_pais.count AS Total_clientes_pais, total_ciudad.count AS Total_clientes_ciudad, 
        TRUNC((total_ciudad.count/total_pais.count)*100,2) AS Porcentaje
        FROM total_pais, total_ciudad 
        WHERE total_pais.id_pais = total_ciudad.id_pais
        ORDER BY total_pais.pais ASC;
    '''
    cur.execute(consulta)
    rows = cur.fetchall()
    cur.close()
    con.close()
    resultado = "<Table border=1><tr><td><b>PAIS</b></td><td><b>CIUDAD</b></td><td><b>TOTAL_CLIENTES_PAIS</b></td><td><b>TOTAL_CLIENTES_CIUDAD</b></td><td><b>PORCENTAJE</b></td></tr>" 
    for i in rows:
        resultado = resultado + '<tr><td>' +str(i[0]) + '</td><td>' + str(i[1]) + '</td><td>' + str(i[2]) + '</td><td>' + str(i[3]) +  '</td><td>' + str(i[4]) +'</td></tr>'
    resultado = resultado + '</Table>'
    return resultado

@app.route("/consulta7")
def consulta7():
    con = psycopg2.connect(
    host = "localhost",
    database = "practica",
    user = "user1",
    password = "1234"
    )
    cur = con.cursor()
    consulta = '''
        WITH total_rentas AS (SELECT Pais.pais, Ciudad.ciudad, 
        count(*)
        FROM Pais, Renta, Ciudad, Cliente
        WHERE Cliente.id_ciudad = Ciudad.id_ciudad 
        AND Pais.id_pais = Ciudad.id_pais
        AND Renta.id_cliente = Cliente.id_cliente
        GROUP BY Pais.id_pais, Ciudad),

        total_pais AS (SELECT Pais.pais,COUNT(*)::DECIMAL  
        FROM  Pais, Cliente, Ciudad
        WHERE Cliente.id_ciudad = Ciudad.id_ciudad
        AND Pais.id_pais = Ciudad.id_pais
        GROUP BY Pais.pais)

        SELECT total_rentas.pais, total_rentas.ciudad, 
        TRUNC(((SUM(total_rentas.count)/total_pais.count)),2) 
        AS promedio
        FROM total_rentas, total_pais, Pais
        WHERE total_rentas.pais = Pais.pais 
        AND total_pais.pais = pais.pais
        GROUP BY total_rentas.pais, total_rentas.ciudad, total_pais.count 
        ORDER BY total_rentas.pais;
    '''
    cur.execute(consulta)
    rows = cur.fetchall()
    cur.close()
    con.close()
    resultado = "<Table border=1><tr><td><b>PAIS</b></td><td><b>CIUDAD</b></td><td><b>PROMEDIO</b></td></tr>" 
    for i in rows:
        resultado = resultado + '<tr><td>' +str(i[0]) + '</td><td>' + str(i[1]) + '</td><td>' + str(i[2]) + '</td></tr>' 
    resultado = resultado + '</table>'
    return resultado

@app.route("/consulta8")
def consulta8():
    con = psycopg2.connect(
    host = "localhost",
    database = "practica",
    user = "user1",
    password = "1234"
    )
    cur = con.cursor()
    consulta = '''
        WITH rentas AS (SELECT Pais.pais, Pais.id_pais, count(*)
        FROM Pais, Renta, Ciudad, Cliente
        WHERE Cliente.id_cliente = Renta.id_cliente 
        AND Cliente.id_ciudad = Ciudad.id_ciudad 
        AND Pais.id_pais = Ciudad.id_pais
        GROUP BY Pais.id_pais),

        categoria_sport AS (SELECT rentas.pais, count(*)
        FROM rentas, Renta, Ciudad, Cliente, Pelicula, 
        Categoria, Pelicula_categoria
        WHERE Cliente.id_cliente = Renta.id_cliente 
        AND Categoria.categoria = 'Sports'
        AND Pelicula_categoria.id_pelicula = Pelicula.id_pelicula 
        AND Pelicula_categoria.id_categoria = Categoria.id_categoria
        AND Renta.id_pelicula = Pelicula.id_pelicula
        AND rentas.id_pais = Ciudad.id_pais 
        AND Cliente.id_ciudad = Ciudad.id_ciudad 
        GROUP BY rentas.pais)

        SELECT rentas.pais, 
        TRUNC(((SUM(categoria_sport.count)/rentas.count)*100),2) 
        AS Porcentaje
        FROM rentas, categoria_sport, Pais
        WHERE rentas.pais = Pais.pais 
        AND categoria_sport.pais = pais.pais
        GROUP BY rentas.pais, categoria_sport.pais, 
        rentas.count, categoria_sport.count 
        ORDER BY rentas.pais ASC;
    '''
    cur.execute(consulta)
    rows = cur.fetchall()
    cur.close()
    con.close()
    resultado = "<Table border=1><tr><td><b>PAIS</b></td><td><b>PORCENTAJE</b></td></tr>" 
    for i in rows:
        resultado = resultado + '<tr><td>' +str(i[0]) + '</td><td>' + str(i[1]) + '</td></tr>' 
    resultado = resultado + '</table>'
    return resultado

@app.route("/consulta9")
def consulta9():
    con = psycopg2.connect(
    host = "localhost",
    database = "practica",
    user = "user1",
    password = "1234"
    )
    cur = con.cursor()
    consulta = '''
        WITH rentas AS (SELECT 
        Pais.pais, Ciudad.ciudad,COUNT(*)
        FROM  Renta, Cliente, Pais, Ciudad
        WHERE  Renta.id_cliente = Cliente.id_cliente
        AND Ciudad.id_ciudad = Cliente.id_ciudad
        AND Ciudad.id_pais = Pais.id_pais
        AND Pais.pais = 'United States'
        GROUP BY Pais.pais, Ciudad.ciudad),

        dayton AS (SELECT  rentas.count
        FROM rentas, Cliente
        WHERE rentas.ciudad = 'Dayton' )

        SELECT rentas.ciudad, rentas.count 
        FROM rentas, dayton
        GROUP BY rentas.ciudad, rentas.count, dayton.count 
        HAVING rentas.count > dayton.count
        ORDER BY rentas.ciudad;
    '''
    cur.execute(consulta)
    rows = cur.fetchall()
    cur.close()
    con.close()
    resultado = "<Table border=1><tr><td><b>CIUDAD</b></td><td><b>RENTAS</b></td></tr>" 
    for i in rows:
        resultado = resultado + '<tr><td>' +str(i[0]) + '</td><td>' + str(i[1]) + '</td></tr>' 
    resultado = resultado + '</table>'
    return resultado

@app.route("/consulta10")
def consulta10():
    con = psycopg2.connect(
    host = "localhost",
    database = "practica",
    user = "user1",
    password = "1234"
    )
    cur = con.cursor()
    consulta = '''
        WITH categoria_horror AS (SELECT Pais.pais, Ciudad.ciudad AS Ciudad, COUNT(*)
        FROM Pais, Renta, Ciudad, Cliente, Pelicula, Categoria, Pelicula_categoria
        WHERE Cliente.id_cliente = Renta.id_cliente 
        AND Renta.id_pelicula = Pelicula.id_pelicula
        AND Categoria.categoria = 'Horror'
        AND Pelicula_categoria.id_pelicula = Pelicula.id_pelicula 
        AND Pelicula_categoria.id_categoria = Categoria.id_categoria
        AND Pais.id_pais = Ciudad.id_pais 
        AND Cliente.id_ciudad = Ciudad.id_ciudad 
        GROUP BY Pais.id_pais, Ciudad),

        otras_categorias AS (SELECT Pais.pais, Ciudad.ciudad AS Ciudad, COUNT(*)
        FROM Pais, Renta, Ciudad, Cliente, Pelicula, Categoria, Pelicula_categoria
        WHERE Cliente.id_cliente = Renta.id_cliente 
        AND Renta.id_pelicula = Pelicula.id_pelicula
        AND Categoria.categoria <> 'Horror'
        AND Pelicula_categoria.id_pelicula = Pelicula.id_pelicula 
        AND Pelicula_categoria.id_categoria = Categoria.id_categoria
        AND Pais.id_pais = Ciudad.id_pais 
        AND Cliente.id_ciudad = Ciudad.id_ciudad 
        GROUP BY Pais.id_pais, Ciudad, Categoria.categoria),

        resultado AS (SELECT otras_categorias.ciudad, MAX(otras_categorias.count) 
        FROM otras_categorias
        GROUP BY otras_categorias.ciudad)

        SELECT categoria_horror.pais, categoria_horror.ciudad
        FROM resultado, categoria_horror
        WHERE resultado.ciudad = categoria_horror.ciudad 
        AND categoria_horror.count >= resultado.max 
        ORDER BY categoria_horror.pais asc;
    '''
    cur.execute(consulta)
    rows = cur.fetchall()
    cur.close()
    con.close()
    resultado = "<Table border=1><tr><td><b>PAIS</b></td><td><b>CIUDAD</b></td></tr>" 
    for i in rows:
        resultado = resultado + '<tr><td>' +str(i[0]) + '</td><td>' + str(i[1]) + '</td></tr>' 
    resultado = resultado + '</table>'
    return resultado




if __name__ == '__main__':
    app.run(debug=True)