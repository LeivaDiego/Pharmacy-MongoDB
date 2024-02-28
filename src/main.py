import ui
import bi

def main():
    while True:
        opcion = ui.menu_principal()
        
        if opcion == '1':
            ui.gestion_medicamentos()
        elif opcion == '2':
            ui.gestion_ventas()
        elif opcion == '3':
            ui.reportes_analisis()
        elif opcion == '4':
            bi.abrir_mongo_charts()
        elif opcion == '5':
            print("Gracias por usar el Sistema de Gestión de la Farmacia. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()