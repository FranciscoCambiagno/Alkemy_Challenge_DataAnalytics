CREATE TABLE museos_cines_biblio(
    id integer NOT NULL,
    cod_localidad integer,
    id_provincia smallint,
    id_departamento integer,
    categoria character(50),
    provincia character(50),
    loclaidad character(50),
    nombre character(255),
    domicilio character(50),
    codigo_postal character(30),
    numero_de_telefono character(30),
    mail character(100),
    web character(255),
    fecha_carga date NOT NULL,
    CONSTRAINT museos_cines_biblio_pkey PRIMARY KEY (id)
);