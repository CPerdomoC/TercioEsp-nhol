CREATE TABLE jugadores (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  equipo VARCHAR(50) NOT NULL,
  dorsal INTEGER,
  pais VARCHAR(50),
  edad INTEGER,
  valor_mercado VARCHAR(50),
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert the required specific player
INSERT INTO jugadores (nombre, equipo, dorsal, pais, edad, valor_mercado)
VALUES ('Christhian Perdomo Casanova', 'Valencia CF', 23, 'Uruguay', 24, '15.000.000 €');
