import db_manager as dbops

def menu_principal():
    print("\nBienvenido al Sistema de Gestión de la Farmacia")
    print("1. Gestión de Medicamentos")
    print("2. Gestión de Ventas")
    print("3. Reportes y Análisis")
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
            dbops.buscar_medicamento_por_nombre_o_id(search_value)
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
        print("4. Regresar al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            print("\nOpción Registrar Venta seleccionada.")
            dbops.registrar_venta()
        elif opcion == '2':
            print("\nOpción Eliminar Ventas seleccionada.")
            dbops.eliminar_venta()
        elif opcion == '3':
            print("\nOpción Filtrar Ventas seleccionada.")
        elif opcion == '4':
            break
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")

def reportes_analisis():
    while True:
        print("\nReportes y Análisis")
        print("1. Ventas por Periodo")
        print("2. Estado del Stock de Medicamentos")
        print("3. Regresar al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            print("Opción Ventas por Periodo seleccionada.")
        elif opcion == '2':
            print("Opción Estado del Stock de Medicamentos seleccionada.")
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
