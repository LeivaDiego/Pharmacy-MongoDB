from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId
from gridfs import GridFS
from datetime import datetime
import os

uri = "mongodb+srv://lei21752:pux2912@cluster.xjohdzx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"

# Crear una instancia del cliente de MongoDB y conectarse ala DB
client = MongoClient(uri)

# Seleccionar la base de datos y la coleccion
db = client.farmacia

# Instanciar un GridFS
fs = GridFS(db)

#--------------------------------------------- Operaciones Auxiliares ---------------------------------------------
def print_doc(document, indent=0):
    for key, value in document.items():
        print(' ' * indent + str(key) + ':', end=' ')
        if isinstance(value, dict):
            print()  # Imprime una nueva línea antes de un subdocumento
            print_doc(value, indent + 4)  # Aumenta la indentación para subdocumentos
        elif isinstance(value, list):
            if value and isinstance(value[0], dict):
                print()  # Nueva línea para listas de documentos
                for item in value:
                    print_doc(item, indent + 4)  # Imprime cada subdocumento en la lista
            else:
                print(value)  # Imprime la lista tal cual si no contiene documentos
        else:
            print(value)  # Imprime el valor si es un tipo básico


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


#--------------------------------------------- Operaciones con medicamentos --------------------------------------
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


def buscar_medicamento_por_nombre_o_id(value):
    criterio = value
    medicamento = None
    
    try:
        # Intentar buscar por ObjectId
        medicamento = db.medicamentos.find_one({"_id": ObjectId(criterio)})
    except:
        # Si falla, es probablemente porque no es un ObjectId válido, entonces buscamos por nombre
        pass
    
    if medicamento is None:
        try:
            # Si aún no hemos encontrado el medicamento, intentamos buscar por nombre
            medicamento = db.medicamentos.find_one({"nombre": criterio})
        except:
            # Si falla, es probablemente porque no es un medicamento valido
            pass

    if medicamento:
        print("Medicamento encontrado:")
        print_doc(medicamento)
        return medicamento
    else:
        print("No se encontró el medicamento.")
        return None
    

def actualizar_medicamento():
    busqueda = input("Ingresa el ID o nombre del medicamento a actualizar: ").strip()
    medicamento = buscar_medicamento_por_nombre_o_id(busqueda)
    
    if not medicamento:
        return
    
    print("Deja el campo en blanco si no deseas cambiar el valor. Para listas, escribe 's' para cambiar, 'n' para mantener.")
    nuevos_valores = {}
    
    nombre = input(f"Nuevo nombre ({medicamento['nombre']}): ").strip()
    if nombre:
        nuevos_valores['nombre'] = nombre
    
    precio = input(f"Nuevo precio ({medicamento['precio']}): ").strip()
    if precio:
        nuevos_valores['precio'] = float(precio)
    
    fabricante = input(f"Nuevo fabricante ({medicamento['fabricante']}): ").strip()
    if fabricante:
        nuevos_valores['fabricante'] = fabricante
    
    presentacion = input(f"Nueva presentación ({medicamento['presentacion']}): ").strip()
    if presentacion:
        nuevos_valores['presentacion'] = presentacion
    
    # Solicitar cambio para listas y la imagen
    def solicitar_cambio_lista_o_imagen(mensaje):
        respuesta = input(mensaje).strip().lower()
        return respuesta == 's'

    if solicitar_cambio_lista_o_imagen("¿Cambiar composición? (s/n): "):
        composicion = solicitar_lista("Introduce la nueva composición: ")
        if composicion:
            nuevos_valores['detalles.composicion'] = composicion
    
    if solicitar_cambio_lista_o_imagen("¿Cambiar efectos secundarios? (s/n): "):
        efectos_secundarios = solicitar_lista("Introduce los nuevos efectos secundarios: ")
        if efectos_secundarios:
            nuevos_valores['detalles.efectos_secundarios'] = efectos_secundarios
    
    if solicitar_cambio_lista_o_imagen("¿Cambiar usos? (s/n): "):
        usos = solicitar_lista("Introduce los nuevos usos: ")
        if usos:
            nuevos_valores['detalles.usos'] = usos

    if solicitar_cambio_lista_o_imagen("¿Cambiar sustitutos? (s/n): "):
        sustitutos = solicitar_lista("Introduce los nuevos sustitutos: ")
        if sustitutos:
            nuevos_valores['sustitutos'] = sustitutos

    clase_terapeutica = input("Nueva clase Terapéutica: ").strip()
    if clase_terapeutica:
        nuevos_valores['clase_terapeutica'] = clase_terapeutica
        
    stock = input("Nueva cantidad de unidades disponibles (deja en blanco para mantener): ").strip()
    if stock:
        while not stock.isdigit() or int(stock) < 0:
            print("La cantidad en stock debe ser un número entero no negativo.")
            stock = input("Cantidad de unidades disponibles: ").strip()
        nuevos_valores['stock'] = int(stock)

    if solicitar_cambio_lista_o_imagen("¿Cambiar imagen? (s/n): "):
        imagen_id = solicitar_y_cargar_imagen()
        if imagen_id:
            nuevos_valores['imagen_id'] = imagen_id

    if nuevos_valores:
        db.medicamentos.update_one({"_id": medicamento['_id']}, {"$set": nuevos_valores})
        print("Medicamento actualizado exitosamente.")
    else:
        print("No se realizaron cambios en el medicamento.")


def eliminar_medicamento():
    busqueda = input("Ingresa el ID o nombre del medicamento a eliminar: ").strip()
    medicamento = buscar_medicamento_por_nombre_o_id(busqueda)
    
    if not medicamento:
        return

    # Mostrar detalles del medicamento antes de confirmar la eliminación
    print("Se encontró el siguiente medicamento para eliminar:")
    print_doc(medicamento)  # Asumiendo que tenemos una función `print_doc` para mostrar el medicamento
    
    confirmacion = input("¿Estás seguro que deseas eliminar este medicamento? (s/n): ").strip().lower()
    if confirmacion == 's':
        db.medicamentos.delete_one({"_id": medicamento['_id']})
        print("Medicamento eliminado exitosamente.")
    else:
        print("Operación cancelada. No se ha eliminado el medicamento.")


def listar_medicamentos():
    offset = 0  # Iniciar el offset en 0
    continuar = 's'  # Inicializar la variable para controlar el bucle
    print("¿Cómo deseas ordenar los medicamentos por stock?")
    orden = input("Escribe 'asc' para ascendente o 'desc' para descendente: ").strip().lower()
    if orden == 'asc':
        ordenamiento = ASCENDING
    elif orden == 'desc':
        ordenamiento = DESCENDING
    else:
        print("No se reconoció el ordenamiento. Mostrando resultados en orden ascendente por defecto.")
        ordenamiento = ASCENDING
    
    while continuar.lower() == 's':
        # Realizar la consulta con ordenamiento, límite y salto (offset)
        medicamentos = db.medicamentos.find().sort("stock", ordenamiento).skip(offset).limit(5)

        print("Listado de medicamentos:")
        for medicamento in medicamentos:
            print_doc(medicamento)  # Utilizando la función print_doc para mostrar cada medicamento
            print('-'*40)

        # Preguntar al usuario si desea ver los siguientes 5 medicamentos
        continuar = input("¿Deseas ver los siguientes 5 medicamentos? (s/n): ").strip()
        
        # Si el usuario desea continuar, incrementar el offset en 5
        if continuar.lower() == 's':
            offset += 5
        else:
            print("Finalizando listado de medicamentos.")

#--------------------------------------------- Operaciones con ventas ---------------------------------------------
def solicitar_metodo_pago():
    while True:
        print("Seleccione el método de pago:")
        print("1. Efectivo")
        print("2. Tarjeta")
        opcion = input("Ingrese el número correspondiente al método de pago: ").strip()
        
        if opcion == "1":
            return "efectivo"
        elif opcion == "2":
            return "tarjeta"
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

def registrar_venta():
    # Inicializar la venta
    venta = {
        "fecha_venta": datetime.now(),
        "items": [],
        "total_venta": 0,
        "metodo_pago": ""
    }

    while True:
        item = agregar_item_a_venta()
        if item: # Asegurarse de que item no es None
            venta["items"].append(item)  # Añadir el ítem a la lista de ítems de la venta

        mas_items = input("¿Deseas agregar otro ítem a la venta? (s/n): ").strip().lower()
        if mas_items != 's':
            break

    # Solicitar el método de pago
    venta["metodo_pago"] = solicitar_metodo_pago()

    # Calcular el total de la venta
    venta["total_venta"] = sum(item["subtotal"] for item in venta["items"])

    # Vista previa de la venta
    print("La venta es:")
    print_doc(venta)  # Mostrar la venta para fines de demostración


   # Confirmación para proceder
    confirmacion = input("¿Estás seguro de que deseas registrar esta venta? (s/n): ").strip().lower()
    if confirmacion == 's':
        db.ventas.insert_one(venta)
        print("Venta registrada con éxito.")
    else:
        print("Venta cancelada.")

def agregar_item_a_venta():

    criterio = input("Ingrese el nombre o ID del medicamento que desea vender: ").strip()
    medicamento = buscar_medicamento_por_nombre_o_id(criterio)

    while True:
        if medicamento:
            cantidad = int(input(f"Ingrese la cantidad de {medicamento['nombre']} que desea vender: "))
            if cantidad <= medicamento["stock"]:
                precio_unitario = medicamento["precio"]
                subtotal = cantidad * precio_unitario

                # Actualizar el stock en la base de datos
                nuevo_stock = medicamento["stock"] - cantidad
                db.medicamentos.update_one({"_id": medicamento["_id"]}, {"$set": {"stock": nuevo_stock}})

                print(f"{cantidad} unidades de {medicamento['nombre']} añadidas a la venta.")
                return {
                    "medicamento_id": medicamento["_id"],
                    "cantidad": cantidad,
                    "precio_unitario": precio_unitario,
                    "subtotal": subtotal
                }
            else:
                print(f"No hay suficiente stock para completar esta venta.")
                print(f"Stock disponible: {medicamento['stock']}")
        else:
            print("Medicamento no encontrado. Por favor, intente de nuevo.")

def solicitar_id_venta():
    id_venta = input("Por favor, ingresa el ID de la venta que deseas eliminar: ").strip()
    return id_venta

def eliminar_venta():
    id_venta = input("Ingresa el ID (factura) de la venta a eliminar: ").strip()

    # Buscar la venta por ID
    try:
        venta = db.ventas.find_one({"_id": ObjectId(id_venta)})
    except:
        pass

    if venta:
        print("Venta encontrada:")
        print_doc(venta)

        confirmacion = input("¿Estás seguro de que quieres eliminar esta venta? (s/n): ").strip().lower()
        if confirmacion == 's':
            # Eliminar la venta
            db.ventas.delete_one({"_id": id_venta})
            print("Venta eliminada con éxito.")
            # Actualizar el stock de los medicamentos
            for item in venta["items"]:
                db.medicamentos.update_one(
                    {"_id": item["medicamento_id"]},
                    {"$inc": {"stock": item["cantidad"]}}
                )
            print("Stock de medicamentos actualizado.")
        else:
            print("Operación cancelada.")
    else:
        print("No se encontró la venta con el ID proporcionado.")

