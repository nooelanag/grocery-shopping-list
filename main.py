# main.py
from database import crear_base_datos
from funciones_recetas import guardar_receta, ver_recetas, gestionar_recetas
from lista_compra import lista_compra

def menu_principal():
    crear_base_datos()  # Asegura que la base de datos esté creada al iniciar el programa
    while True:
        print("\nMenú Principal")
        print("1. Guardar receta")
        print("2. Ver recetas")
        print("3. Lista de la Compra")
        print("4. Gestionar recetas")
        print("5. Salir")
        
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            guardar_receta()
        elif opcion == "2":
            ver_recetas()
        elif opcion == "3":
            lista_compra()
        elif opcion == "4":
            gestionar_recetas()
        elif opcion == "5":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    menu_principal()
