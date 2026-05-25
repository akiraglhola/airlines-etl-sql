CREATE DATABASE IF NOT EXISTS airlines;

USE airlines;

CREATE TABLE IF NOT EXISTS estados (
    estado        CHAR(2)      NOT NULL,
    nombre_estado VARCHAR(255) NOT NULL,
    PRIMARY KEY (estado)
);

CREATE TABLE IF NOT EXISTS aerolineas (
    icao                CHAR(3)      NOT NULL,
    aerolinea           VARCHAR(255) NOT NULL,
    iata                CHAR(2),
    country             VARCHAR(255),
    founded             INT,
    started_operations  INT,
    air_group           VARCHAR(255),
    base                VARCHAR(255),
    fleet_size          INT,
    average_fleet_age   FLOAT,
    official_site       VARCHAR(255),
    PRIMARY KEY (icao)
);

CREATE TABLE IF NOT EXISTS aeropuertos (
    codigo_aeropuerto CHAR(3)      NOT NULL,
    nombre_aeropuerto VARCHAR(255),
    ciudad            VARCHAR(255),
    estado            CHAR(2),
    latitud           FLOAT,
    longitude         FLOAT,
    direccion         VARCHAR(255),
    PRIMARY KEY (codigo_aeropuerto),
    FOREIGN KEY (estado) REFERENCES estados (estado)
);

CREATE TABLE IF NOT EXISTS distancias (
    distancia_millas   FLOAT,
    aeropuerto_origen  CHAR(3) NOT NULL,
    aeropuerto_destino CHAR(3) NOT NULL,
    PRIMARY KEY (aeropuerto_origen, aeropuerto_destino),
    FOREIGN KEY (aeropuerto_origen)  REFERENCES aeropuertos (codigo_aeropuerto),
    FOREIGN KEY (aeropuerto_destino) REFERENCES aeropuertos (codigo_aeropuerto)
);

CREATE TABLE IF NOT EXISTS vuelos (
    aerolinea                      CHAR(3)  NOT NULL,
    fecha                          DATE     NOT NULL,
    numero_vuelo                   INT      NOT NULL,
    numero_cola                    VARCHAR(10),
    hora_salida_programada         TIME,
    hora_salida_real               TIME,
    duracion_programada_vuelo      INT,
    duracion_real                  INT,
    retraso_salida                 INT,
    hora_despegue                  TIME,
    tiempo_pista_salida            INT,
    tiempo_retraso_aerolinea       INT,
    tiempo_retraso_clima           INT,
    tiempo_retraso_sistema_aviacion INT,
    tiempo_retraso_seguridad       INT,
    retraso_llegada                INT,
    aeropuerto_origen              CHAR(3),
    hora_llegada_real              TIME,
    festivos                       TINYINT,
    aeropuerto_destino             CHAR(3),
    PRIMARY KEY (aerolinea, numero_vuelo, fecha),
    FOREIGN KEY (aerolinea)           REFERENCES aerolineas (icao),
    FOREIGN KEY (aeropuerto_origen)   REFERENCES aeropuertos (codigo_aeropuerto),
    FOREIGN KEY (aeropuerto_destino)  REFERENCES aeropuertos (codigo_aeropuerto)
);