import cv2
import mss
import numpy as np
import pyaudio
import wave
import threading
import time
import os
import tkinter as tk
from tkinter import ttk, messagebox
from pydub.utils import make_chunks
import io
import pyautogui
from pydub import AudioSegment
AudioSegment.ffmpeg = "/usr/bin/ffmpeg"

# Cargar la imagen del cursor (asegúrate de tener una imagen de cursor, como "cursor.png")
cursor_img = cv2.imread('cursor/cursor.png', cv2.IMREAD_UNCHANGED)  # Lee la imagen del cursor
cursor_img_resized = cv2.resize(cursor_img, (28, 28)) # 32 32

# Configuración inicial
default_monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
filename_video = "grabacion_video.mp4"
filename_audio = "grabacion_audio.mp3"
output_file = "grabacion_final.mp4"
fps = 20.0

# Configuración de audio
audio_format = pyaudio.paInt16
channels = 2
rate = 44100
chunk = 1024

# Variables globales
recording = False
paused = False
selected_area = default_monitor

# Función para seleccionar un área personalizada
def seleccionar_area():
    """Permite al usuario seleccionar un área personalizada para grabar."""
    global selected_area

    def dibujar_rectangulo(event):
        """Inicia el rectángulo."""
        nonlocal x_start, y_start
        x_start, y_start = event.x, event.y

    def finalizar_rectangulo(event):
        """Finaliza el rectángulo."""
        nonlocal x_start, y_start
        x_end, y_end = event.x, event.y
        selected_area = {
            "top": min(y_start, y_end),
            "left": min(x_start, x_end),
            "width": abs(x_end - x_start),
            "height": abs(y_end - y_start),
        }
        print(f"Área seleccionada: {selected_area}")
        root.destroy()

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)
    root.configure(bg="black")
    label = tk.Label(root, text="Haz clic y arrastra para seleccionar el área", bg="white", fg="black")
    label.pack()

    x_start, y_start = 0, 0
    root.bind("<Button-1>", dibujar_rectangulo)
    root.bind("<ButtonRelease-1>", finalizar_rectangulo)
    root.mainloop()

# Función para grabar audio
def grabar_audio():
    """Graba audio desde el micrófono."""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    os.environ["PYTHONWARNINGS"] = "ignore:ALSA"
    frames = []

    print("Grabando audio...")
    while recording:
        if not paused:
            data = stream.read(chunk)
            frames.append(data)

    print("Finalizando grabación de audio...")
    stream.stop_stream()
    stream.close()

    # Guardar como MP3 utilizando pydub
    audio_data = b"".join(frames)
    audio_segment = AudioSegment.from_raw(
        io.BytesIO(audio_data),
        sample_width=audio.get_sample_size(audio_format),
        frame_rate=rate,
        channels=channels,
    )
    audio_segment.export(filename_audio.replace(".mp3", ".wav"), format="wav")
    print(f"Audio guardado como MP3: {filename_audio.replace('.wav', '.mp3')}")

    audio.terminate()

# Función para grabar video (con cursor redimensionado)
def grabar_video():
    """Graba video desde la pantalla y muestra el cursor real."""
    global recording, paused
    sct = mss.mss()
    video_out = cv2.VideoWriter(
        filename_video, cv2.VideoWriter_fourcc(*"mp4v"), fps, (selected_area["width"], selected_area["height"])
    )

    print("Grabando pantalla...")
    while recording:
        if not paused:
            img = np.array(sct.grab(selected_area))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            # Obtener posición del cursor
            cursor_pos = pyautogui.position()

            # Calcular la posición relativa del cursor dentro del área seleccionada
            relative_x = cursor_pos.x - selected_area["left"]
            relative_y = cursor_pos.y - selected_area["top"]

            # Asegurarse de que el cursor esté dentro del área de grabación
            if 0 <= relative_x < selected_area["width"] and 0 <= relative_y < selected_area["height"]:
                cursor_h, cursor_w = cursor_img_resized.shape[:2]

                # Dibujar el cursor sobre el frame (superponiéndolo)
                cursor_x = relative_x - cursor_w // 2
                cursor_y = relative_y - cursor_h // 2

                # Asegurarse de que el cursor no se salga del área de grabación
                if 0 <= cursor_x < selected_area["width"] - cursor_w and 0 <= cursor_y < selected_area["height"] - cursor_h:
                    # Obtener la parte del frame donde se dibujará el cursor
                    roi = frame[cursor_y:cursor_y+cursor_h, cursor_x:cursor_x+cursor_w]

                    # Aplicar la imagen del cursor sobre el frame usando la transparencia (canal alfa)
                    if cursor_img_resized.shape[2] == 4:  # Si la imagen del cursor tiene transparencia
                        alpha_mask = cursor_img_resized[:, :, 3] / 255.0
                        for c in range(0, 3):
                            roi[:, :, c] = roi[:, :, c] * (1 - alpha_mask) + cursor_img_resized[:, :, c] * alpha_mask
                    else:  # Si no tiene transparencia
                        frame[cursor_y:cursor_y+cursor_h, cursor_x:cursor_x+cursor_w] = cursor_img_resized

            video_out.write(frame)
        time.sleep(0.01)

    video_out.release()

# Controladores para la interfaz gráfica
def iniciar_grabacion():
    global recording, paused
    if recording:
        messagebox.showwarning("Advertencia", "La grabación ya está en curso.")
        return

    recording = True
    paused = False
    audio_thread = threading.Thread(target=grabar_audio)
    video_thread = threading.Thread(target=grabar_video)

    audio_thread.start()
    video_thread.start()
    status_label.config(text="Grabando...", foreground="green")

def pausar_grabacion():
    global paused
    if not recording:
        messagebox.showwarning("Advertencia", "No hay una grabación en curso.")
        return

    paused = not paused
    status_label.config(
        text="Grabación pausada" if paused else "Grabando...", foreground="orange" if paused else "green"
    )

def detener_grabacion():
    global recording
    if not recording:
        messagebox.showwarning("Advertencia", "No hay una grabación en curso.")
        return

    recording = False
    status_label.config(text="Grabación detenida", foreground="red")

    # Combinar audio y video
    print("Combinando audio y video...")
    os.system(f"ffmpeg -y -i {filename_video} -i {filename_audio.replace('.mp3', '.wav')} -c:v copy -c:a aac {output_file}")
    print(f"Grabación finalizada: {output_file}")
    messagebox.showinfo("Grabación completa", f"El archivo final se guardó como {output_file}")

def seleccionar_area_interfaz():
    seleccionar_area()
    messagebox.showinfo("Área seleccionada", f"Área seleccionada: {selected_area}")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Grabador de Pantalla")
root.geometry("400x300")

# Etiquetas y botones
status_label = ttk.Label(root, text="Listo para grabar", font=("Arial", 14), foreground="blue")
status_label.pack(pady=20)

btn_iniciar = ttk.Button(root, text="Iniciar Grabación", command=iniciar_grabacion)
btn_iniciar.pack(pady=5)

btn_pausar = ttk.Button(root, text="Pausar/Reanudar Grabación", command=pausar_grabacion)
btn_pausar.pack(pady=5)

btn_detener = ttk.Button(root, text="Detener Grabación", command=detener_grabacion)
btn_detener.pack(pady=5)

btn_seleccionar_area = ttk.Button(root, text="Seleccionar Área", command=seleccionar_area_interfaz)
btn_seleccionar_area.pack(pady=5)

# Iniciar la aplicación
root.mainloop()
