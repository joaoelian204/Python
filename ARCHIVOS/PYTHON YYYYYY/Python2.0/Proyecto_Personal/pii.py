from PIL import Image
import os

descargas = "/home/joaoelian/Descargas/"

if __name__ == "__main__":
    for filename in os.listdir(descargas):
        name, extension = os.path.splitext(filename)
        
        if extension.lower() in [".jpg", ".jpeg", ".png", ".avif", ".webp",".svg"]:
            imagenes = "/home/joaoelian/Imágenes/"
            try:
                os.rename(descargas + filename, imagenes + filename)
                print(f" - {name}: {extension}\n")
            except Exception as e:
                print(f"Error al procesar {filename}: {e}")

        if extension.lower() in [".mp3"]:
            Musica = "/home/joaoelian/Música/"
            try:
                os.rename(descargas + filename, Musica + filename)
                print(f" - {name}: {extension}\n")
            except:
                print(f"Tuvimos problemas con este archivo {filename}")
        
        if extension.lower() in [".pdf", ".docx", ".txt"]:
            Documentos = "/home/joaoelian/Documentos/DOCUMENTOS/"
            try:
                os.rename(descargas + filename, Documentos + filename)
                print(f" - {name}: {extension}\n")
            except:
                print(f"Tuvimos problemas con este archivo {filename}")
            
        if extension.lower() in [".mp4", ".mov", ".wmv", ".avi", ".webm"]:
            Video = "/home/joaoelian/Vídeos/"
            try:
                os.rename(descargas + filename,  Video + filename)
                print(f" - {name}: {extension}\n")
            except:
                print(f"Tuvimos problemas con este archivo {filename}")
        