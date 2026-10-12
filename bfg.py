import math
import time


class Planeta:
    # Atributo de clase para el conteo global
    total_planetas = 0

    def __init__(self, nombre: str, distancia_sol_ua: float):
        """
        Constructor de la clase Planeta.
        :param nombre: Nombre del planeta.
        :param distancia_sol_ua: Distancia media al Sol en Unidades Astronómicas (UA).
        """
        self.nombre = nombre
        self.distancia_sol_ua = distancia_sol_ua

        # Incrementamos el contador de clase
        Planeta.total_planetas += 1
        print(f"✅ [Planeta] {self.nombre} ha sido registrado en la base de datos galáctica.")

    def __del__(self):
        """Destrucción del objeto Planeta."""
        # Se reduce el conteo al destruir la instancia
        Planeta.total_planetas -= 1

    @classmethod
    def obtener_total_planetas(cls) -> int:
        """Método de clase para obtener el conteo total de planetas registrados."""
        return cls.total_planetas

    def mostrar_info(self) -> None:
        """Método de instancia para mostrar los datos del planeta."""
        print(f"🪐 Planeta: {self.nombre} | Distancia al Sol: {self.distancia_sol_ua} UA")


class NaveEspacial:
    # Atributos de clase
    total_naves = 0
    VELOCIDAD_LUZ_KM_S = 299792.458  # Constante interna (ámbito de clase)
    UA_EN_KM = 149597870.7          # 1 UA en kilómetros

    def __init__(self, nombre: str, velocidad_max_km_s: float):
        """
        Constructor de la clase NaveEspacial.
        :param nombre: Nombre de la nave espacial.
        :param velocidad_max_km_s: Velocidad crucero en km/s.
        """
        # Atributos de instancia privados/protegidos mediante ámbito de variables
        self.nombre = nombre
        self.velocidad_max_km_s = velocidad_max_km_s
        self.destino_actual = None
        self.misiones = []          # Almacenará *args
        self.recursos = {}          # Almacenará **kwargs

        # Incrementamos el contador de clase
        NaveEspacial.total_naves += 1
        print(f"🚀 [Nave] {self.nombre} está lista para servicio.")

    def __del__(self):
        """Destrucción del objeto NaveEspacial."""
        NaveEspacial.total_naves -= 1

    @classmethod
    def obtener_total_naves(cls) -> int:
        """Método de clase para consultar el conteo total de naves en la flota."""
        return cls.total_naves

    def asignar_destino(self, planeta: Planeta, *misiones, **recursos) -> None:
        """
        Método de instancia que asigna un destino y recibe argumentos variables.
        :param planeta: Instancia de la clase Planeta.
        :param misiones: *args para recibir misiones adicionales.
        :param recursos: **kwargs para recibir recursos asignados a la nave.
        """
        self.destino_actual = planeta
        
        # Procesamiento de *args
        if misiones:
            self.misiones.extend(misiones)

        # Procesamiento de **kwargs
        if recursos:
            self.recursos.update(recursos)

        print(f"\n🗺️ Destino asignado a '{self.nombre}': {planeta.nombre}")
        if misiones:
            print(f"   📋 Misiones adicionales registradas ({len(misiones)}): {', '.join(misiones)}")
        if recursos:
            recursos_fmt = ", ".join([f"{k}: {v}" for k, v in recursos.items()])
            print(f"   📦 Recursos cargados: {recursos_fmt}")

    def calcular_tiempo_viaje(self, origen: Planeta) -> float | None:
        """
        Calcula el tiempo estimado de viaje entre un planeta de origen y el destino asignado.
        :param origen: Objeto de tipo Planeta.
        :return: Tiempo de viaje en días.
        """
        if not self.destino_actual:
            print(f"❌ La nave '{self.nombre}' no tiene un destino asignado actualmente.")
            return None

        # Ámbito local: Variables de cálculo dentro del método
        distancia_ua = abs(self.destino_actual.distancia_sol_ua - origen.distancia_sol_ua)
        distancia_km = distancia_ua * self.UA_EN_KM

        if self.velocidad_max_km_s <= 0:
            print("❌ La velocidad de la nave debe ser mayor a 0 km/s.")
            return None

        tiempo_segundos = distancia_km / self.velocidad_max_km_s
        tiempo_dias = tiempo_segundos / 86400  # Convertir segundos a días

        print(f"\n⏱️  --- CÁLCULO DE TRAYECTORIA ({self.nombre}) ---")
        print(f"   Origen: {origen.nombre} ({origen.distancia_sol_ua} UA)")
        print(f"   Destino: {self.destino_actual.nombre} ({self.destino_actual.distancia_sol_ua} UA)")
        print(f"   Distancia Relativa: {distancia_ua:.2f} UA ({distancia_km:,.2f} km)")
        print(f"   Tiempo estimado de viaje: {tiempo_dias:.2f} días terrestres.")

        return tiempo_dias

    def mostrar_info(self) -> None:
        """Muestra el estado general de la nave espacial."""
        destino_str = self.destino_actual.nombre if self.destino_actual else "Sin destino"
        print(f"🚀 Nave: {self.nombre}")
        print(f"   Velocidad Máxima: {self.velocidad_max_km_s:,} km/s")
        print(f"   Destino Actual: {destino_str}")
        print(f"   Misiones Asignadas: {self.misiones if self.misiones else 'Ninguna'}")
        print(f"   Inventario de Recursos: {self.recursos if self.recursos else 'Sin carga'}")


# ==========================================
# MENÚ INTERACTIVO Y ÁMBITO PRINCIPAL
# ==========================================

def mostrar_menu():
    print("\n" + "=" * 45)
    print("   🌌 SISTEMA DE VIAJES INTERPLANETARIOS 🌌")
    print("=" * 45)
    print("1. Registrar planeta")
    print("2. Registrar nave espacial")
    print("3. Asignar destino (con *args y **kwargs)")
    print("4. Calcular tiempo de viaje")
    print("5. Mostrar información del sistema")
    print("6. Salir")
    print("-" * 45)


def main():
    # Ámbito local de main(): diccionarios para guardar instancias activas
    planetas_db: dict[str, Planeta] = {}
    naves_db: dict[str, NaveEspacial] = {}

    # Instancias iniciales de prueba
    p_tierra = Planeta("Tierra", 1.0)
    p_marte = Planeta("Marte", 1.52)
    planetas_db[p_tierra.nombre.lower()] = p_tierra
    planetas_db[p_marte.nombre.lower()] = p_marte

    n_explorer = NaveEspacial("Apolo XXI", 50.0)
    naves_db[n_explorer.nombre.lower()] = n_explorer

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-6): ").strip()

        if opcion == "1":
            print("\n--- REGISTRAR PLANETA ---")
            nombre = input("Nombre del planeta: ").strip()
            if not nombre:
                print("❌ El nombre no puede estar vacío.")
                continue
            
            try:
                distancia = float(input("Distancia media al Sol (en UA, ej. Tierra=1.0, Júpiter=5.2): "))
                p = Planeta(nombre, distancia)
                planetas_db[nombre.lower()] = p
            except ValueError:
                print("❌ Error: Debes ingresar un número válido para la distancia.")

        elif opcion == "2":
            print("\n--- REGISTRAR NAVE ESPACIAL ---")
            nombre = input("Nombre de la nave: ").strip()
            if not nombre:
                print("❌ El nombre no puede estar vacío.")
                continue

            try:
                velocidad = float(input("Velocidad máxima (en km/s): "))
                n = NaveEspacial(nombre, velocidad)
                naves_db[nombre.lower()] = n
            except ValueError:
                print("❌ Error: Debes ingresar un número válido para la velocidad.")

        elif opcion == "3":
            print("\n--- ASIGNAR DESTINO A NAVE ---")
            if not naves_db or not planetas_db:
                print("❌ Se requiere al menos una nave y un planeta registrados.")
                continue

            nave_key = input("Nombre de la nave: ").strip().lower()
            if nave_key not in naves_db:
                print("❌ Nave no encontrada.")
                continue

            planeta_key = input("Nombre del planeta de destino: ").strip().lower()
            if planeta_key not in planetas_db:
                print("❌ Planeta no encontrado.")
                continue

            # Misiones (*args)
            misiones_raw = input("Ingresa misiones adicionales (separadas por coma) o Enter para omitir: ").strip()
            misiones = [m.strip() for m in misiones_raw.split(",")] if misiones_raw else []

            # Recursos (**kwargs)
            recursos = {}
            recursos_raw = input("Ingresa recursos (clave=valor separados por coma, ej. agua=500, oxigeno=100) o Enter: ").strip()
            if recursos_raw:
                for item in recursos_raw.split(","):
                    if "=" in item:
                        k, v = item.split("=", 1)
                        recursos[k.strip()] = v.strip()

            naves_db[nave_key].asignar_destino(
                planetas_db[planeta_key],
                *misiones,
                **recursos
            )

        elif opcion == "4":
            print("\n--- CALCULAR TIEMPO DE VIAJE ---")
            nave_key = input("Nombre de la nave: ").strip().lower()
            if nave_key not in naves_db:
                print("❌ Nave no encontrada.")
                continue

            origen_key = input("Nombre del planeta de origen: ").strip().lower()
            if origen_key not in planetas_db:
                print("❌ Planeta de origen no encontrado.")
                continue

            naves_db[nave_key].calcular_tiempo_viaje(planetas_db[origen_key])

        elif opcion == "5":
            print("\n" + "=" * 45)
            print("         📊 INFORMACIÓN GENERAL DEL SISTEMA")
            print("=" * 45)
            # Uso de Métodos de Clase
            print(f"Total de planetas en base de datos: {Planeta.obtener_total_planetas()}")
            print(f"Total de naves registradas en la flota: {NaveEspacial.obtener_total_naves()}")
            print("-" * 45)

            print("\n🪐 PLANETAS REGISTRADOS:")
            for p in planetas_db.values():
                p.mostrar_info()

            print("\n🚀 NAVES REGISTRADAS:")
            for n in naves_db.values():
                n.mostrar_info()
                print("-" * 20)

        elif opcion == "6":
            print("\nCerrando sistema de viajes interplanetarios... ¡Buen viaje!")
            break

        else:
            print("❌ Opción inválida. Intenta nuevamente.")


if __name__ == "__main__":
    main()