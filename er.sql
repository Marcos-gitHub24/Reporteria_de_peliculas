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