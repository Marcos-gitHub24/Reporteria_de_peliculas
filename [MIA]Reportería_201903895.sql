-- CONSULTA 1 --

WITH peli AS (SELECT id_pelicula FROM Pelicula
WHERE titulo = 'SUGAR WONKA')
SELECT SUM(copias) AS copias FROM tienda_pelicula, peli
WHERE tienda_pelicula.id_pelicula = peli.id_pelicula;

--CONSULTA 2 --

SELECT Cliente.nombre, Cliente.apellido, 
TRUNC(SUM(Renta.cantidad_pagar)::DECIMAL,2) AS PAGO
FROM  Renta, Cliente
WHERE  REnta.id_cliente = Cliente.id_cliente
GROUP BY Cliente.nombre, Cliente.apellido
HAVING COUNT(*) >= 40;

--CONSULTA 3 --

SELECT nombre || ' ' || apellido AS ACTORES FROM 
Actor WHERE Actor.apellido LIKE '%son%'
ORDER BY Actor.nombre ASC ;

--CONSULTA 4 --

SELECT Actor.nombre, Actor.apellido, 
Pelicula.ano_lanzamiento
FROM Actor, Pelicula, Pelicula_actor 
WHERE Pelicula.descripcion LIKE '%Crocodile%'
AND Pelicula.descripcion LIKE '%Shark%'
AND Pelicula_actor.id_actor = Actor.id_actor 
AND Pelicula_actor.id_pelicula = Pelicula.id_pelicula
ORDER BY Actor.apellido ASC;

--- CONSULTA 5 --

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

-- CONSULTA 6 --
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

-- CONSULTA 7 --

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

--CONSULTA 8--

WITH rentas AS (SELECT Pais.pais, Pais.id_pais, count(*)
FROM Cliente, Ciudad, Pais, Renta  
WHERE Cliente.id_cliente = Renta.id_cliente 
AND Cliente.id_ciudad = Ciudad.id_ciudad 
AND Pais.id_pais = Ciudad.id_pais
GROUP BY Pais.id_pais),

categoria_sport AS (SELECT rentas.pais, count(*)
FROM  Cliente, Ciudad, Renta ,Pelicula, rentas, 
Categoria, Pelicula_categoria
WHERE Cliente.id_cliente = Renta.id_cliente 
AND Categoria.categoria = 'Sports'
AND Pelicula_categoria.id_pelicula = Pelicula.id_pelicula 
AND Pelicula_categoria.id_categoria = Categoria.id_categoria
AND Renta.id_pelicula = Pelicula.id_pelicula
AND rentas.id_pais = Ciudad.id_pais 
AND Cliente.id_ciudad = Ciudad.id_ciudad 
GROUP BY rentas.pais)

SELECT rentas.pais, TRUNC(((SUM(categoria_sport.count)/rentas.count)*100),2) 
AS Porcentaje
FROM rentas, categoria_sport, Pais
WHERE rentas.pais = Pais.pais 
AND categoria_sport.pais = pais.pais
GROUP BY rentas.pais, categoria_sport.pais, 
rentas.count, categoria_sport.count 
ORDER BY rentas.pais ASC;

-- CONSULTA 9 --

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

--CONSULTA 10--

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