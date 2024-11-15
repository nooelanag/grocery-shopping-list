# funciones_recetas.py
import sqlite3

def guardar_receta():
    nombre = input("Introduce el nombre de la receta: ")
    ingredientes = input("Introduce los ingredientes (separados por comas): ")
    categoria = input("¿Es Desayuno, Comida o Cena? ").capitalize()
    while categoria not in ("Desayuno", "Comida", "Cena"):
        print("Opción inválida. Intenta nuevamente.")
        categoria = input("¿Es Desayuno, Comida o Cena? ").capitalize()
    rapida = input("¿Es rápida de hacer? (si/no): ").lower() == "si"

    conexion = sqlite3.connect("recetas.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO recetas (nombre, ingredientes, categoria, rapida) VALUES (?, ?, ?, ?)", 
                   (nombre, ingredientes, categoria, rapida))
    conexion.commit()
    conexion.close()
    print("Receta guardada correctamente.")

def ver_recetas():
    categoria = input("Elige una categoría para ver (Desayuno, Comida, Cena): ").capitalize()
    while categoria not in ("Desayuno", "Comida", "Cena"):
        print("Opción inválida. Intenta nuevamente.")
        categoria = input("Elige una categoría para ver (Desayuno, Comida, Cena): ").capitalize()

    conexion = sqlite3.connect("recetas.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM recetas WHERE categoria = ?", (categoria,))
    recetas = cursor.fetchall()
    
    if not recetas:
        print(f"No hay recetas para {categoria}.")
        return

    for receta in recetas:
        print(f"{receta[0]}: {receta[1]}")
    
    receta_id = int(input("Elige una receta por su número para ver los detalles o presiona 0 para volver: "))
    
    if receta_id == 0:
        return
    
    cursor.execute("SELECT nombre, ingredientes, rapida FROM recetas WHERE id = ?", (receta_id,))
    receta = cursor.fetchone()
    print(f"Nombre: {receta[0]}")
    print(f"Ingredientes: \n\t{receta[1]}")
    print("Es rápida de hacer." if receta[2] else "No es rápida de hacer.")
    conexion.close()

def gestionar_recetas():
    categoria = input("Elige una categoría para editar (Desayuno, Comida, Cena): ").capitalize()
    while categoria not in ("Desayuno", "Comida", "Cena"):
        print("Opción inválida. Intenta nuevamente.")
        categoria = input("Elige una categoría para editar (Desayuno, Comida, Cena): ").capitalize()
    
    conexion = sqlite3.connect("recetas.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM recetas WHERE categoria = ?", (categoria,))
    recetas = cursor.fetchall()

    if not recetas:
        print(f"No hay recetas para {categoria}.")
        return

    for receta in recetas:
        print(f"{receta[0]}: {receta[1]}")
    
    receta_id = int(input("Elige una receta por su número para editar/eliminar o presiona 0 para volver: "))
    if receta_id != 0:
        while receta_id not in ([r[0] for r in recetas]):
                print(f"La recta {receta_id} no se ha encontrado.")
                receta_id = int(input("Elige una receta por su número para editar/eliminar: "))
        cursor.execute("SELECT nombre, ingredientes, rapida FROM recetas WHERE id = ?", (receta_id,))
        receta = cursor.fetchone()
        decision = input(f"¿Desea eliminar o editar la receta \"{receta[0]}\"?: ").capitalize()
        while decision not in ("Editar", "Eliminar"):
            print("Opción inválida. Intenta nuevamente.")
            decision = input(f"¿Desea eliminar o editar la receta \"{receta[0]}\"?: ").capitalize()
    
        if decision == "Eliminar":
            decision = input(f"¿Estás seguro de que quieres eliminar la receta \"{receta[0]}\"? (Si/No):").capitalize()
            while decision != "Si" and decision != "No":
                print("Opción inválida. Intenta nuevamente.")
                decision = input(f"¿Estás seguro de que quieres eliminar la receta \"{receta[0]}\"? (Si/No): ").capitalize()
        
            if decision == "Si":
                cursor.execute("DELETE FROM recetas WHERE nombre = ?",(receta[0],))
                cursor.execute("UPDATE recetas SET id = id - 1 WHERE id > ?", (receta_id,))
                conexion.commit()
                conexion.close()
                print("Receta eliminada")
            else:
                print("Receta NO eliminada")


        
        else:
            decision = input(f"¿Estás seguro de que quieres editar la receta \"{receta[0]}\"? (Si/No): ").capitalize()
            while decision != "Si" and decision != "No":
                print("Opción inválida. Intenta nuevamente.")
                decision = input(f"¿Estás seguro de que quieres editar la receta \"{receta[0]}\"? (Si/No): ").capitalize()

            if decision == "Si":
                decision = input("¿Quieres editar el Nombre, los Ingredientes o la Categoria (desayuno, comida, cena)?: ").capitalize()
                while decision != "Nombre" and decision != "Ingredientes" and decision != "Categoria":
                    decision = input("Opción inválida. Intenta nuevamente. (Nombre/Ingredientes/Categoria): ").capitalize()
                if decision == "Nombre":
                    nombre = input("Introduzca el nuevo nombre: ")
                    decision = input(f"¿Estás seguro de que quieres cambiar {receta[0]} por {nombre}? (Si/No): ").capitalize()
                    while decision != "Si" and decision != "No":
                        decision = input(f"Opción invalida. Intenta de nuevo. ¿Estás seguro de que quieres cambiar \"{receta[0]}\" por \"{nombre}\"? (Si/No): ").capitalize()
                    if decision == "Si":
                        cursor.execute("UPDATE recetas SET nombre = ? WHERE nombre = ?", (nombre, receta[0]))
                        conexion.commit()
                        conexion.close()
                        print("Receta editada.")
                    else:
                        print("Cambio no realizado")
                elif decision == "Ingredientes":
                    ingredientes = input("Introduzca los ingredientes separados por una coma: ")
                    decision = input(f"¿Estás seguro de que quieres cambiar \n\t \"{receta[1]}\" \n por \n\t \"{ingredientes}\"?\n (Si/No): ").capitalize()
                    while decision != "Si" and decision != "No":
                        decision = input(f"Opción invalida. Intenta de nuevo. ¿Estás seguro de que quieres cambiar \"{receta[1]}\" \n por \n \"{ingredientes}\"? (Si/No): ").capitalize()
                    if decision == "Si":
                        cursor.execute("UPDATE recetas SET ingredientes = ? WHERE ingredientes = ?", (ingredientes, receta[1]))
                        conexion.commit()
                        conexion.close()
                        print("Receta editada.")
                    else:
                        print("Cambio no realizado")
                else:
                    categoria = input("Introduzca la nueva categoria: ").capitalize()
                    while categoria != "Desayuno" and categoria != "Comida" and categoria != "Cena":
                        categroia = input("Opción invalida. Intenta de nuevo. Introduzca la nueva categoria (Desayuno/Comida/Cena): ").capitalize()
                    decision = input(f"¿Estás seguro de que quieres cambiar a \"{categoria}\"? (Si/No): ").capitalize()
                    while decision != "Si" and decision != "No":
                        decision = input(f"Opción invalida. Intenta de nuevo. ¿Estás seguro de que quieres cambiar a \"{categoria}\"? (Si/No): ").capitalize()
                    if decision == "Si":
                        cursor.execute("UPDATE recetas SET categoria = ? WHERE nombre = ?", (categoria, receta[0]))
                        conexion.commit()
                        conexion.close()
                        print("Receta editada.")
                    else:
                        print("Cambio no realizado")
            else:
                print("Receta NO editada")
                    




    
                
