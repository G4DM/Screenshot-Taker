import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import img2pdf
import requests

def download_pdf(url, save_path):
    try:
        response = requests.get(url)
        with open(f"{save_path}/downloaded_pdf.pdf", "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error al descargar el PDF: {e}")
        return False

def take_full_page_screenshot():
    url = url_entry.get()
    save_path = path_entry.get()

    if not url:
        status_label.config(text="Ingrese una URL", fg="red")
        return

    if not save_path:
        status_label.config(text="Seleccione una ruta de almacenamiento", fg="red")
        return

    try:
        # Si la URL termina en ".pdf", intentar descargar el PDF directamente
        if url.lower().endswith(".pdf"):
            if not download_pdf(url, save_path):
                status_label.config(text="Error al descargar el PDF", fg="red")
                return

            url = f"file://{save_path}/downloaded_pdf.pdf"

        # La URL es una página web normal o un PDF descargado
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        
        # Obtener la altura de la página
        height = driver.execute_script("return document.body.scrollHeight")

        # Tomar capturas de pantalla desplazándose hacia abajo
        screenshots = []
        for i in range(0, height, 1000):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(0.5)  # Esperar un poco para que la página se cargue completamente
            screenshot_path = f"{save_path}/screenshot_{i}.png"
            driver.save_screenshot(screenshot_path)
            screenshots.append(screenshot_path)

        driver.quit()

        # Convertir las capturas de pantalla a PDF
        with open(f"{save_path}/full_page_screenshot.pdf", "wb") as f:
            f.write(img2pdf.convert(screenshots))

        status_label.config(text="Capturas de pantalla tomadas con éxito", fg="green")
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")

def clear_url():
    url_entry.delete(0, tk.END)

def select_path():
    save_path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, save_path)

# Crear la ventana principal
root = tk.Tk()
root.title("Captura de Pantalla de Página Completa")

# Crear y colocar los elementos de la interfaz
url_label = tk.Label(root, text="URL:")
url_label.grid(row=0, column=0, padx=5, pady=5)

url_entry = tk.Entry(root, width=40)
url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

clear_button = tk.Button(root, text="Limpiar URL", command=clear_url)
clear_button.grid(row=0, column=3, padx=5, pady=5)

path_label = tk.Label(root, text="Ruta de Almacenamiento:")
path_label.grid(row=1, column=0, padx=5, pady=5)

path_entry = tk.Entry(root, width=40)
path_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

path_button = tk.Button(root, text="Seleccionar Ruta", command=select_path)
path_button.grid(row=1, column=3, padx=5, pady=5)

capture_button = tk.Button(root, text="Tomar Captura de Pantalla de Página Completa", command=take_full_page_screenshot)
capture_button.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=3, column=0, columnspan=4)

# Ejecutar la aplicación
root.mainloop()
