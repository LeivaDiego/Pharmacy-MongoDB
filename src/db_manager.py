from pymongo import MongoClient
from gridfs import GridFS
import os

uri = "mongodb+srv://lei21752:pux2912@cluster.xjohdzx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"

# Crear una instancia del cliente de MongoDB y conectarse ala DB
client = MongoClient(uri)

# Seleccionar la base de datos y la coleccion
db = client.farmacia

# Instanciar un GridFS
fs = GridFS(db)


def cargar_imagen_a_gridfs(ruta_imagen):
    if not os.path.isfile(ruta_imagen):
        print("El archivo especificado no existe.")
        return None
    with open(ruta_imagen, 'rb') as imagen:
        imagen_id = fs.put(imagen, filename=os.path.basename(ruta_imagen))
        return imagen_id


def solicitar_y_cargar_imagen():
    while True:
        ruta_imagen = input("Ruta a la imagen del medicamento (deja en blanco si no quieres subir imagen, escribe 'cancelar' para detener el proceso): ").strip()
        # Reemplazar \ por /
        ruta_imagen = ruta_imagen.replace("\\", "/")

        if ruta_imagen.lower() == 'cancelar':
            print("Cancelando carga de imagen.")
            return None
        elif ruta_imagen:
            imagen_id = cargar_imagen_a_gridfs(ruta_imagen)
            if imagen_id:
                print(f"Imagen cargada exitosamente. ID: {imagen_id}")
                return imagen_id
            else:
                print("No se pudo cargar la imagen. Asegúrate de que la ruta es correcta.")
        else:
            print("No se subirá ninguna imagen.")
            return None


def solicitar_lista(mensaje):
    """Función auxiliar para solicitar al usuario una lista de elementos."""
    print(mensaje)
    items = []
    item = input("Introduce un elemento (o deja en blanco y presiona enter para terminar): ")
    while item:
        items.append(item)
        item = input("Introduce otro elemento (o deja en blanco y presiona enter para terminar): ")
    return items


def agregar_medicamento():
    print("\nAgregar Nuevo Medicamento")
    
    nombre = input("Nombre del Medicamento: ").strip()
    while not nombre:
        print("El nombre del medicamento no puede estar vacío.")
        nombre = input("Nombre del Medicamento: ").strip()

    precio = input("Precio del Medicamento (por unidad): ").strip()
    while not precio.replace('.','',1).isdigit() or float(precio) <= 0:
        print("El precio debe ser un número positivo.")
        precio = input("Precio del Medicamento (por unidad): ").strip()
    precio = float(precio)

    fabricante = input("Nombre del Fabricante: ").strip()
    while not fabricante:
        print("El nombre del fabricante no puede estar vacío.")
        fabricante = input("Nombre del Fabricante: ").strip()

    presentacion = input("Presentación del Medicamento: ").strip()
    while not presentacion:
        print("La presentación no puede estar vacía.")
        presentacion = input("Presentación del Medicamento: ").strip()

    # Solicitar composición, efectos secundarios, usos y sustitutos como listas
    composicion = solicitar_lista("Introduce la composición del medicamento:")
    efectos_secundarios = solicitar_lista("Introduce los efectos secundarios del medicamento:")
    usos = solicitar_lista("Introduce los usos del medicamento:")
    sustitutos = solicitar_lista("Introduce los sustitutos del medicamento:")

    clase_terapeutica = input("Clase Terapéutica del Medicamento: ").strip()
    while not clase_terapeutica:
        print("La clase terapéutica no puede estar vacía.")
        clase_terapeutica = input("Clase Terapéutica del Medicamento: ").strip()

    stock = input("Cantidad de unidades disponibles: ").strip()
    while not stock.isdigit() or int(stock) < 0:
        print("La cantidad en stock debe ser un número entero no negativo.")
        stock = input("Cantidad de unidades disponibles: ").strip()
    stock = int(stock)

    imagen_id = solicitar_y_cargar_imagen()

    medicamento = {
        "nombre": nombre,
        "precio": precio,
        "fabricante": fabricante,
        "presentacion": presentacion,
        "detalles": {
            "composicion": composicion,
            "efectos_secundarios": efectos_secundarios,
            "usos": usos
        },
        "sustitutos": sustitutos,
        "clase_terapeutica": clase_terapeutica,
        "stock": stock,
        "imagen_id": imagen_id
    }

    # Insertar el documento en MongoDB
    medicamento_id = db.medicamentos.insert_one(medicamento).inserted_id
    print(f"Medicamento agregado exitosamente con ID: {medicamento_id}")
