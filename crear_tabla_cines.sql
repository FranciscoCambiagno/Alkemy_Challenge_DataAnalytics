CREATE TABLE cines(
    id integer NOT NULL,
    provincia character(50),
    pantallas smallint,
    butacas integer,
    espacios_incaa smallint,
    fecha_carga date NOT NULL,
    CONSTRAINT cines_pkey PRIMARY KEY (id)
);