#!/bin/python3


import sys
import os
from comprobacion import comprobar
import hashlib


if not (len(sys.argv) == 3):
    print("ERROR: Numero de parametros incorrecto.")
    print("No se han proporcionado correctamente los parámetros. Uso: python3 Lab06Act1.py <archivo> <directorio>")
    exit(-1)


archivo = sys.argv[1]
directorio = sys.argv[2]


def find_files_with_conditions(directory, target_file):
    matching_files = []  # Almacenará los archivos que cumplen las condiciones
    longest_prefix = 0    # Almacena la longitud del prefijo de 0's más largo
    best_file = None      # Almacena el archivo con el resumen SHA-256 más largo de 0's


    for _, _, files in os.walk(directory, topdown=True):
        for file in files:
            full_path = os.path.join(directory, file)
           
            valid, _, prefix_length = comprobar(target_file, full_path)


            # Comprobar si el archivo cumple con las condiciones
            if valid:
                matching_files.append((full_path, prefix_length))
               
                # Calcular la longitud del prefijo de 0's
                if prefix_length > longest_prefix:
                    longest_prefix = prefix_length
                    best_file = full_path
                elif prefix_length == longest_prefix:
                    # En caso de empate, puedes elegir un criterio, por ejemplo, el archivo más nuevo
                    if os.path.getmtime(full_path) > os.path.getmtime(best_file):
                        best_file = full_path
   
    # Ordenar la lista de archivos según el prefijo de 0's de mayor a menor
    matching_files = sorted(matching_files, key=lambda x: x[1], reverse=True)
   
    return matching_files, best_file, longest_prefix


def main():
    matching_files, best_file, longest_prefix = find_files_with_conditions(directorio, archivo)


    print("Archivos que cumplen con las condiciones (ordenados por prefijo de 0's de mayor a menor):")
    for file, prefix_length in matching_files:
        print(f"- {file} (Longitud del prefijo de 0's en el hash: {prefix_length})")
   
    if best_file:
        print(f"El archivo con el resumen SHA-256 más largo de 0's es: {best_file}")
        print(f"Longitud del prefijo de 0's en el hash: {longest_prefix}")
    else:
        print("No se encontraron archivos que cumplan con las condiciones en el directorio.")


if __name__ == "__main__":
    main()