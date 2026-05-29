import numpy as np
import pandas as pd
from mysql.connector.connection import MySQLConnection


BATCH_SIZE = 1000


def _replace_nan_with_none(df: pd.DataFrame) -> pd.DataFrame:
    """Replace all NaN values in a DataFrame with None.

    MySQL does not understand NumPy NaN, it needs Python None to insert NULL.

    Args:
        df: Input DataFrame potentially containing NaN values.

    Returns:
        DataFrame with NaN replaced by None.
    """
    return df.astype(object).where(pd.notna(df), other=None)


def _insert_batch(cursor, query: str, data: list) -> None:
    """Insert rows in batches using INSERT IGNORE.

    Args:
        cursor: Active MySQL cursor.
        query: Parameterized INSERT query string.
        data: List of tuples to insert.
    """
    for i in range(0, len(data), BATCH_SIZE):
        batch = data[i : i + BATCH_SIZE]
        cursor.executemany(query, batch)


def load_estados(conn: MySQLConnection, filepath: str) -> None:
    """Load estados table from CSV.

    Args:
        conn: Active MySQL connection.
        filepath: Path to tabla_estados.csv.
    """
    df = pd.read_csv(filepath).drop_duplicates()
    df = _replace_nan_with_none(df)

    query = "INSERT IGNORE INTO estados (estado, nombre_estado) VALUES (%s, %s)"
    data = df[["estado", "nombre_estado"]].values.tolist()

    cursor = conn.cursor()
    _insert_batch(cursor, query, data)
    conn.commit()
    cursor.close()
    print(f"  estados: {len(data)} rows processed")


def load_aerolineas(conn: MySQLConnection, filepath: str) -> None:
    """Load aerolineas table from CSV.

    Args:
        conn: Active MySQL connection.
        filepath: Path to tabla_aerolineas.csv.
    """
    df = pd.read_csv(filepath).drop_duplicates()
    df.columns = [
        "icao", "aerolinea", "iata", "country", "founded",
        "started_operations", "air_group", "base", "fleet_size",
        "average_fleet_age", "official_site",
    ]
    df = _replace_nan_with_none(df)

    query = """
        INSERT IGNORE INTO aerolineas
            (icao, aerolinea, iata, country, founded, started_operations,
             air_group, base, fleet_size, average_fleet_age, official_site)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = df.values.tolist()

    cursor = conn.cursor()
    _insert_batch(cursor, query, data)
    conn.commit()
    cursor.close()
    print(f"  aerolineas: {len(data)} rows processed")


def load_aeropuertos(conn: MySQLConnection, filepath: str) -> None:
    """Load aeropuertos table from CSV.

    Args:
        conn: Active MySQL connection.
        filepath: Path to tabla_aeropuertos.csv.
    """
    df = pd.read_csv(filepath).drop_duplicates()
    df.columns = [
        "codigo_aeropuerto", "nombre_aeropuerto", "ciudad",
        "estado", "latitud", "longitude", "direccion",
    ]
    df = _replace_nan_with_none(df)

    query = """
        INSERT IGNORE INTO aeropuertos
            (codigo_aeropuerto, nombre_aeropuerto, ciudad, estado,
             latitud, longitude, direccion)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    data = df.values.tolist()

    cursor = conn.cursor()
    _insert_batch(cursor, query, data)
    conn.commit()
    cursor.close()
    print(f"  aeropuertos: {len(data)} rows processed")


def load_distancias(conn: MySQLConnection, filepath: str) -> None:
    """Load distancias table from CSV, filtering invalid foreign keys.

    Rows referencing airports not present in the aeropuertos table are
    silently dropped to avoid FK constraint errors.

    Args:
        conn: Active MySQL connection.
        filepath: Path to tabla_distancias.csv.
    """
    df = pd.read_csv(filepath).drop_duplicates(
        subset=["aeropuerto_origen", "aeropuerto_destino"]
    )
    df = _replace_nan_with_none(df)

    cursor = conn.cursor()
    cursor.execute("SELECT codigo_aeropuerto FROM aeropuertos")
    aeropuertos_validos = {row[0] for row in cursor.fetchall()}

    df = df[
        df["aeropuerto_origen"].isin(aeropuertos_validos)
        & df["aeropuerto_destino"].isin(aeropuertos_validos)
    ]

    query = """
        INSERT IGNORE INTO distancias
            (distancia_millas, aeropuerto_origen, aeropuerto_destino)
        VALUES (%s, %s, %s)
    """
    data = df[["distancia_millas", "aeropuerto_origen", "aeropuerto_destino"]].values.tolist()

    _insert_batch(cursor, query, data)
    conn.commit()
    cursor.close()
    print(f"  distancias: {len(data)} rows processed")


def load_vuelos(conn: MySQLConnection, filepath: str) -> None:
    """Load vuelos table from CSV in batches.

    Args:
        conn: Active MySQL connection.
        filepath: Path to tabla_vuelos.csv.
    """
    df = pd.read_csv(filepath).drop_duplicates(
        subset=["aerolinea", "numero_vuelo", "fecha"]
    )
    df = _replace_nan_with_none(df)

    query = """
        INSERT IGNORE INTO vuelos
            (aerolinea, fecha, numero_vuelo, numero_cola,
             hora_salida_programada, hora_salida_real,
             duracion_programada_vuelo, duracion_real, retraso_salida,
             hora_despegue, tiempo_pista_salida, tiempo_retraso_aerolinea,
             tiempo_retraso_clima, tiempo_retraso_sistema_aviacion,
             tiempo_retraso_seguridad, retraso_llegada, aeropuerto_origen,
             hora_llegada_real, festivos, aeropuerto_destino)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = df.values.tolist()

    cursor = conn.cursor()
    _insert_batch(cursor, query, data)
    conn.commit()
    cursor.close()
    print(f"  vuelos: {len(data)} rows processed")