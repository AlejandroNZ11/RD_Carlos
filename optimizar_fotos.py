from PIL import Image
import os

# Carpeta actual donde están tus fotos
directorio_origen = "./"  
# Carpeta donde se guardarán las fotos livianas
directorio_destino = "./optimizadas/"

if not os.path.exists(directorio_destino):
    os.makedirs(directorio_destino)

print("Iniciando proceso completo (renombrado de originales y optimización)... 🚀")

# 1. Obtenemos y ordenamos todas las imágenes de la carpeta de origen
archivos_en_origen = os.listdir(directorio_origen)
imagenes = [f for f in archivos_en_origen if f.lower().endswith((".png", ".jpg", ".jpeg"))]

# Ordenamos alfabéticamente para que el proceso sea consistente
imagenes.sort()

contador = 1

for nombre_archivo in imagenes:
    ruta_actual = os.path.join(directorio_origen, nombre_archivo)
    
    # Evitamos procesar si por alguna razón es una carpeta
    if os.path.isdir(ruta_actual):
        continue    

    try:
        # Obtenemos la extensión original (.jpg, .png, etc.)
        extension = os.path.splitext(nombre_archivo)[1].lower()
        
        # Nuevo nombre para la foto original
        nuevo_nombre_original = f"ori_{contador}{extension}"
        nueva_ruta_original = os.path.join(directorio_origen, nuevo_nombre_original)
        
        # Renombramos el archivo original solo si el nombre es distinto
        if ruta_actual != nueva_ruta_original:
            # Si el archivo destino ya existe temporalmente, lo manejamos o renombramos
            if os.path.exists(nueva_ruta_original):
                os.remove(nueva_ruta_original)
            os.rename(ruta_actual, nueva_ruta_original)
        
        # 2. Abrimos la imagen (ya renombrada como ori_X) para optimizarla
        img = Image.open(nueva_ruta_original)
        
        # Reducir a 800px de ancho si es muy grande
        ancho_maximo = 800
        if img.size[0] > ancho_maximo:
            proporcion = (ancho_maximo / float(img.size[0]))
            alto_nuevo = int((float(img.size[1]) * float(proporcion)))
            img = img.resize((ancho_maximo, alto_nuevo), Image.Resampling.LANCZOS)
        
        # Convertir a RGB si es necesario para guardar como JPG
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Nombre y ruta para la foto optimizada en la carpeta destino
        nuevo_nombre_optimizado = f"ft{contador}.jpg"
        ruta_destino = os.path.join(directorio_destino, nuevo_nombre_optimizado)
        
        # Guardar optimizada
        img.save(ruta_destino, "JPEG", optimize=True, quality=60)
        
        print(f"✅ Original: {nombre_archivo} ➡️ {nuevo_nombre_original} | Web: {nuevo_nombre_optimizado}")
        
        contador += 1
        
    except Exception as e:
        print(f"❌ Error con {nombre_archivo}: {e}")

print("¡Proceso finalizado! Todas las originales fueron renombradas y optimizadas.")
