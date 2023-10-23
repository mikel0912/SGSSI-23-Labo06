import hashlib
import secrets
import re

def calculate_sha256(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def comprobar_fila_condiciones(fila):
    patron = re.compile(r'[0-9a-f]{8}(\t|\s+)[0-9a-f]{2}(\t|\s+)100')
    return bool(patron.match(fila))

def main(file1, file2):
    # Leer el contenido del primer archivo
    with open(file1, 'r') as f1:
        content_file1 = f1.read()
    
    # Leer el contenido del segundo archivo
    with open(file2, 'r') as f2:
        content_file2 = f2.read()
        line_count = sum(1 for line in f2)
    
    numero_0s=0
    
    # Verificar si el segundo archivo comienza con el contenido del primero
    if content_file2.startswith(content_file1):
        # Calcular el resumen SHA-256 del segundo archivo
        sha256_hex = calculate_sha256(file2)
        
        # Verificar si comienza con una secuencia de 0's
        if sha256_hex.startswith("00"):
            numero_0s = len(sha256_hex)-len(sha256_hex.lstrip('0'))            
            
            lines1 = content_file1.splitlines()
            last_line1 = lines1[line_count-1]  # Última línea del segundo archivo
            # Verificar si el segundo archivo cumple con las características específicas
            lines2 = content_file2.splitlines()
            last_line2 = lines2[line_count-1]  # Última línea del segundo archivo
            penultima_linea2 = lines2[line_count-2]  # Penúltima línea del segundo archivo
            if comprobar_fila_condiciones(last_line2) and penultima_linea2==last_line1:
                return True, sha256_hex, numero_0s
    
    return False, None, numero_0s