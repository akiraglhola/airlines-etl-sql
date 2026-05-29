from db import get_connection
from etl import (
    load_estados,
    load_aerolineas,
    load_aeropuertos,
    load_distancias,
    load_vuelos,
)


DATA_DIR = "data"


def main() -> None:
    """Run the full ETL pipeline."""
    print("Connecting to database...")
    conn = get_connection()
    print("Connected.\n")

    print("Loading data...")
    load_estados(conn, f"{DATA_DIR}/tabla_estados.csv")
    load_aerolineas(conn, f"{DATA_DIR}/tabla_aerolineas.csv")
    load_aeropuertos(conn, f"{DATA_DIR}/tabla_aeropuertos.csv")
    load_distancias(conn, f"{DATA_DIR}/tabla_distancias.csv")
    load_vuelos(conn, f"{DATA_DIR}/tabla_vuelos.csv")

    conn.close()
    print("\nETL complete.")


if __name__ == "__main__":
    main()