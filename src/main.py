def menu_principal():
    print("\nBienvenido al Sistema de PAHRMA+")
    print("1. Gestión de Medicamentos")
    print("2. Gestión de Ventas")
    print("3. Reportes y Análisis")
    print("4. Salir")
    opcion = input("Seleccione una opción: ")
    return opcion

def gestion_medicamentos():
    # TODO logica de medicamentos 
    pass

def gestion_ventas():
    # TODO logica de ventas
    pass

def reportes_analisis():
    # TODO logica de medicamentos
    pass

def main():
    while True:
        opcion = menu_principal()
        
        if opcion == '1':
            gestion_medicamentos()
        elif opcion == '2':
            gestion_ventas()
        elif opcion == '3':
            reportes_analisis()
        elif opcion == '4':
            print("Gracias por usar el Sistema de POAHRMA+. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
