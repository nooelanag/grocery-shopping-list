# lista_compra.py
import sqlite3
from collections import Counter

def lista_compra():
    lista_ingredientes = Counter()
    while True:
        opcion = input("Opciones: Desayuno, Comida, Cena, Imprimir o Volver: ").capitalize()
        while opcion not in ("Desayuno", "Comida", "Cena", "Imprimir", "Volver"):
            print("Opción inválida. Intenta nuevamente.")
            opcion = input("Opciones: Desayuno, Comida, Cena, Imprimir o Volver: ").capitalize()
        
        if opcion == "Imprimir":
            print("Lista de la Compra:")
            for ingrediente, cantidad in lista_ingredientes.items():
                print(f"{ingrediente}: X{cantidad}")
            
            # Exportar lista a un archivo de texto
            with open("lista_de_compra.txt", "w") as archivo:
                for ingrediente, cantidad in lista_ingredientes.items():
                    archivo.write(f"{ingrediente}: {cantidad} vez/veces\n")
            print("Lista exportada a 'lista_de_compra.txt'")
            break
        elif opcion in ["Desayuno", "Comida", "Cena"]:
            conexion = sqlite3.connect("recetas.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, ingredientes FROM recetas WHERE categoria = ?", (opcion,))
            recetas = cursor.fetchall()
            conexion.close()
            
            if not recetas:
                print(f"No hay recetas para {opcion}.")
                continue
            
            for receta in recetas:
                print(f"{receta[0]}: {receta[1]}")
            
            receta_id = int(input("Selecciona una receta por su número para añadir a la lista o 0 para volver: "))
            if receta_id == 0:
                continue
            else:
                while receta_id not in ([r[0] for r in recetas]):
                    print(f"La recta {receta_id} no se ha encontrado.")
                    receta_id = int(input("Selecciona una receta por su número para añadir a la lista: "))




            # Añadir ingredientes a la lista de compra
            seleccionada = next((r for r in recetas if r[0] == receta_id), None)
            if seleccionada:
                ingredientes = seleccionada[2].split(", ")
                lista_ingredientes.update(ingredientes)
                print(f"{seleccionada[1]} añadida a la lista de compra.")
        else:
            break
