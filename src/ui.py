import db_manager as dbops

def menu_principal():
    print("\nBienvenido al Sistema de Gestión de la Farmacia")
    print("1. Gestión de Medicamentos")
    print("2. Gestión de Ventas")
    print("3. Reportes y Análisis de Ventas")
    print("4. Salir")
    opcion = input("Seleccione una opción: ")
    return opcion

def gestion_medicamentos():
    while True:
        print("\nGestión de Medicamentos")
        print("1. Añadir Medicamento")
        print("2. Buscar Medicamento")
        print("3. Actualizar Medicamento")
        print("4. Eliminar Medicamento")
        print("5. Listar Medicamentos")
        print("6. Regresar al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            print("\nOpción Añadir Medicamento seleccionada.")
            dbops.agregar_medicamento()
        elif opcion == '2':
            print("\nOpción Buscar Medicamento seleccionada.")
            search_value = input("Ingrese el nombre o ID del medicamento que desea buscar: ")
            dbops.buscar_medicamento(search_value)
        elif opcion == '3':
            print("\nOpción Actualizar Medicamento seleccionada.")
            dbops.actualizar_medicamento()
        elif opcion == '4':
            print("\nOpción Eliminar Medicamento seleccionada.")
            dbops.eliminar_medicamento()
        elif opcion == '5':
            print("\nOpción Listar Medicamentos seleccionada.")
            dbops.listar_medicamentos()
        elif opcion == '6':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

def gestion_ventas():
    while True:
        print("\nGestión de Ventas")
        print("1. Registrar Venta")
        print("2. Eliminar Ventas")
        print("3. Filtrar Ventas")
        print("4. Buscar ventas")
        print("5. Regresar al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            print("\nOpción Registrar Venta seleccionada.")
            dbops.registrar_venta()
        elif opcion == '2':
            print("\nOpción Eliminar Ventas seleccionada.")
            dbops.eliminar_venta()
        elif opcion == '3':
            print("\nOpción Filtrar Ventas seleccionada.")
            dbops.filtrar_ventas()
        elif opcion == '4':
            print("\nOpción Buscar Ventas seleccionada.")
            dbops.buscar_venta()
        elif opcion == '5':
            break
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")

def reportes_ventas():
    while True:
        print("\nReportes y Análisis de Venta")
        print("1. Total de Ventas por Año")
        print("2. Top 10 medicamentos mas populares")
        print("3. Regresar al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            print("Opción Total Ventas por Año seleccionada.")
            dbops.total_ventas()
        elif opcion == '2':
            print("Opción Top 10 medicamentos mas populares seleccionada.")
            dbops.top_productos_vendidos()
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
