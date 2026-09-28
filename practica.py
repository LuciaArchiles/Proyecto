import json

# Nombre del archivo JSON
nombre_archivo = "electrical_data.json"

try:
    # 1. Abrir y leer el archivo JSON
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    # 2. Acceder al nivel principal: 'grid_network'
    red = datos.get("grid_network", {})

    print("=== INFORMACIÓN DE LA RED ELÉCTRICA ===")
    print(f"Región: {red.get('region')}")
    print(f"Operador: {red.get('operator')}")
    print(f"Nivel de Voltaje: {red.get('voltage_level_kv')} kV")
    print(f"Última actualización: {red.get('timestamp')}\n")

    # 3. Recorrer las subestaciones dentro de 'substations'
    subestaciones = red.get("substations", [])
    for sub in subestaciones:
        print(f"--- Subestación: {sub.get('name')} (ID: {sub.get('id')}) ---")

        # Coordenadas (otro objeto anidado dentro de 'location')
        loc = sub.get("location", {})
        print(
            f"  Ubicación -> Lat: {loc.get('latitude')}, Lon: {loc.get('longitude')}, Altitud: {loc.get('elevation_m')} m"
        )

        # 4. Recorrer los transformadores de esta subestación
        print("  [Transformadores]:")
        for tx in sub.get("transformers", []):
            print(
                f"    - ID: {tx.get('id')} | Estado: {tx.get('status')} | Carga: {tx.get('load_percentage')}% | Temp: {tx.get('temperature_celsius')} °C"
            )

            # Mediciones técnicas (anidadas dentro de 'measurements')
            med = tx.get("measurements", {})
            print(
                f"      Mediciones -> Corriente: {med.get('current_amperes')} A | Potencia Activa: {med.get('active_power_mw')} MW"
            )

        # 5. Recorrer los alimentadores (feeders) de esta subestación
        print("  [Alimentadores]:")
        for fdr in sub.get("feeders", []):
            print(
                f"    - ID: {fdr.get('feeder_id')} | Estado: {fdr.get('status')} | Disparos (24h): {fdr.get('tripped_count_last_24h')}"
            )
        print()  # Espacio entre subestaciones

except FileNotFoundError:
    print(
        f"El archivo '{nombre_archivo}' no se encuentra en el directorio actual."
    )
except json.JSONDecodeError:
    print("Hubo un error al decodificar el archivo JSON (formato inválido).")

#acceder a un campo de json

temperatura_especifica = (
    datos.get("grid_network", {})
    .get("substations", [])[0]
    .get("transformers", [])[0]
    .get("temperature_celsius")
)

print(f"Temperatura exacta: {temperatura_especifica} °C")

