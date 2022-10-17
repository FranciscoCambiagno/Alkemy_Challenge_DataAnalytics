CREATE TABLE cant_indices(
    id integer NOT NULL,
    categoria character(100),
    cant_registros integer,
    fecha_carga date NOT NULL,
    CONSTRAINT cant_indices_pkey PRIMARY KEY (id)
);