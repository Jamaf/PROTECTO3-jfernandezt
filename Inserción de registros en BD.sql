--Insercion de Tipos_Ingredientes
INSERT INTO public."Tipos_Ingredientes"(id, nombre)VALUES (1, 'Base');
INSERT INTO public."Tipos_Ingredientes"(id, nombre)VALUES (2, 'Complemento');

--Insercion de Tipos_Productos
INSERT INTO public."Tipos_Productos"(id, nombre)VALUES (1, 'Copa');
INSERT INTO public."Tipos_Productos"(id, nombre)VALUES (2, 'Malteada');

-- Inserción de ingredientes
INSERT INTO public."Ingredientes" (nombre, precio, calorias, inventario, es_vegetariano, id_tipo_ingrediente) VALUES
('Leche entera', 1.50, 60, 500.00, true, 1),
('Azúcar', 0.80, 400, 200.00, true, 1),
('Crema de leche', 2.50, 200, 150.00, true, 1),
('Extracto de vainilla', 3.00, 15, 50.00, true, 1),
('Chocolate en polvo', 2.20, 350, 100.00, true, 2),
('Fresas frescas', 1.80, 32, 300.00, true, 2),
('Banana', 1.20, 89, 150.00, true, 2),
('Mango', 1.50, 60, 120.00, true, 2),
('Jarabe de chocolate', 2.00, 290, 80.00, true, 2),
('Coco rallado', 1.00, 100, 75.00, true, 2),
('Miel', 2.50, 300, 40.00, true, 2),
('Menta fresca', 1.00, 5, 30.00, true, 2),
('Nueces', 3.50, 650, 60.00, false, 2),
('Caramelo líquido', 2.20, 330, 70.00, true, 2),
('Oreo trituradas', 1.80, 480, 90.00, false, 2),
('Galletas troceadas', 1.50, 450, 80.00, false, 2),
('Frutos secos mixtos', 4.00, 700, 50.00, false, 2),
('Granola', 2.50, 500, 100.00, true, 2),
('Chispas de chocolate', 2.80, 540, 60.00, true, 2),
('Sirope de fresa', 2.00, 250, 75.00, true, 2);

-- Inserción de productos
INSERT INTO public."Productos" (nombre, precio, tipo_vaso, volumen, id_tipo_producto) VALUES
('Copa de Fresa', 6.50, 'Copa de vidrio', 200, 1),
('Copa de Vainilla', 6.00, 'Copa de vidrio', 200, 1),
('Copa de Chocolate', 7.00, 'Copa de vidrio', 200, 1),
('Copa Tropical', 7.50, 'Copa de vidrio', 250, 1),
('Copa Oreo', 7.80, 'Copa de vidrio', 220, 1),
('Malteada de Fresa', 8.00, 'Vaso plástico', 300, 2),
('Malteada de Chocolate', 8.50, 'Vaso plástico', 300, 2),
('Malteada de Vainilla', 7.80, 'Vaso plástico', 300, 2),
('Malteada Tropical', 9.00, 'Vaso plástico', 350, 2),
('Malteada Oreo', 9.50, 'Vaso plástico', 350, 2);

-- Inserción de relaciones en Productos_Ingredientes
INSERT INTO public."Productos_Ingredientes" (id_producto, id_ingrediente) VALUES
(1, 1), (1, 2), (1, 3), (1, 6), (1, 20), -- Copa de Fresa
(2, 1), (2, 2), (2, 3), (2, 4), -- Copa de Vainilla
(3, 1), (3, 2), (3, 3), (3, 5), (3, 9), -- Copa de Chocolate
(4, 1), (4, 2), (4, 3), (4, 7), (4, 8), (4, 10), -- Copa Tropical
(5, 1), (5, 2), (5, 3), (5, 15), (5, 16), -- Copa Oreo
(6, 1), (6, 2), (6, 3), (6, 6), (6, 20), -- Malteada de Fresa
(7, 1), (7, 2), (7, 3), (7, 5), (7, 9), -- Malteada de Chocolate
(8, 1), (8, 2), (8, 3), (8, 4), -- Malteada de Vainilla
(9, 1), (9, 2), (9, 3), (9, 7), (9, 8), (9, 10), -- Malteada Tropical
(10, 1), (10, 2), (10, 3), (10, 15), (10, 16); -- Malteada Oreo


INSERT INTO public."Clientes"(id, nombre)VALUES (1, 'Leonardo da Vinci');
INSERT INTO public."Clientes"(id, nombre)VALUES (2, 'Vincent van Gogh');
INSERT INTO public."Clientes"(id, nombre)VALUES (3, 'Miguel Ángel');
INSERT INTO public."Clientes"(id, nombre)VALUES (4, 'Pablo Picasso');
INSERT INTO public."Clientes"(id, nombre)VALUES (5, 'Salvador Dalí');
INSERT INTO public."Clientes"(id, nombre)VALUES (6, 'Fernando Botero');

update public."Ingredientes"
set precio = precio * 1000

update public."Ingredientes"
set inventario = inventario / 10

update public."Productos"
set precio = precio * 2000

insert into public."Heladerias"(id, nombre)VALUES (1, 'Heladería Helarte');

insert into public."Heladerias_Productos"(id_heladeria, id_producto)VALUES (1, 1);
insert into public."Heladerias_Productos"(id_heladeria, id_producto)VALUES (1, 3);
insert into public."Heladerias_Productos"(id_heladeria, id_producto)VALUES (1, 8);
insert into public."Heladerias_Productos"(id_heladeria, id_producto)VALUES (1, 9);

select * from public."Tipos_Productos"

select * from public."Tipos_Ingredientes"

select * from public."Ingredientes"

select * from public."Productos"

select * from public."Productos_Ingredientes"

select * from public."Clientes"

select * from public."Heladerias_Productos"

select * from public."Ventas"

--Todos los productos
select 
	Prod.*
	,Ing.*
from public."Productos" as Prod
inner join public."Productos_Ingredientes" as PI
	on Prod.Id = PI.id_producto
inner join public."Ingredientes" as Ing
	on Ing.Id = PI.id_ingrediente
	
--los productos habilitados en la heladeria
select 
	Prod.*
	,Ing.*
from public."Productos" as Prod
inner join public."Productos_Ingredientes" as PI
	on Prod.Id = PI.id_producto
inner join public."Ingredientes" as Ing
	on Ing.Id = PI.id_ingrediente	
inner join public."Heladerias_Productos" as HP
	on Prod.Id = HP.id_producto





