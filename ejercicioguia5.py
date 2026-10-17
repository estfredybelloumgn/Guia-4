import random
import threading
import time
import tkinter as tk


class Carrera:

  def __init__(self, ventana):
    self.ventana = ventana
    self.ventana.title("Carrera de vehículos")
    self.ventana.geometry("1000x1200")
    self.ventana.config(bg="gold")

    self.carrera_iniciada = False
    self.carrera_terminada = False

    self.numero_vueltas = 1
    self.vehiculo_apostado = 1

    self.tiempos = [None] * 10
    self.vueltas = [0] * 10
    self.hilos = []

    self.crear_interfaz()

  def crear_interfaz(self):
    self.titulo = tk.Label(self.ventana, text="COPA PISTON !!PRIMERA EDICION¡¡", font=("Arial", 22), bg="gold")
    self.titulo.place(x=300, y=10)

    texto_apuesta = tk.Label(self.ventana, text="Vehículo apostado:", font=("Arial", 12), bg="gold")
    texto_apuesta.place(x=10, y=790)

    self.entrada_apuesta = tk.Entry(self.ventana, width=5, bg="blue")
    self.entrada_apuesta.place(x=150, y=790)
    self.entrada_apuesta.insert(0, "1")

    texto_vueltas = tk.Label(self.ventana, text="Número de vueltas:", font=("Arial", 12), bg="gold")
    texto_vueltas.place(x=250, y=790)

    self.entrada_vueltas = tk.Entry(self.ventana, width=5, bg="blue")
    self.entrada_vueltas.place(x=390, y=790)
    self.entrada_vueltas.insert(0, "1")

    texto_velocidad = tk.Label(self.ventana, text="Velocidad:", font=("Arial", 12), bg="gold")
    texto_velocidad.place(x=480, y=790)

    self.slider = tk.Scale(self.ventana, from_=1, to=10, orient="horizontal", length=150, bg="pink")
    self.slider.set("5")
    self.slider.place(x=560, y=790)

    self.boton_iniciar = tk.Button(self.ventana,text="Start",font=("Arial", 15),command=self.iniciar_carrera,bg="green",)
    self.boton_iniciar.place(x=750, y=790, width=100, height=40)

    self.boton_reiniciar = tk.Button(self.ventana,text="Reiniciar",font=("Arial", 15),command=self.reiniciar_carrera,bg="blue",)
    self.boton_reiniciar.place(x=860, y=790, width=110, height=40)

    self.mensaje = tk.Label(self.ventana, text="La carrera esta por iniciar", font=("Arial", 12), bg="gold")
    self.mensaje.place(x=750, y=860)

    self.resultados = tk.Label(self.ventana, text="Ranking", font=("Arial", 9), bg="gold", justify="left")
    self.resultados.place(x=10, y=820)

    self.crear_pista()

  def crear_pista(self):
    self.imagen1 = tk.PhotoImage(file="carritoblanco.png")
    self.imagen2 = tk.PhotoImage(file="carritoazul.png")
    self.imagen3 = tk.PhotoImage(file="carritoamarillo.png")
    self.imagen4 = tk.PhotoImage(file="carritorojo.png")
    self.imagen5 = tk.PhotoImage(file="carritobeage.png")
    self.imagen6 = tk.PhotoImage(file="carritonegro.png")
    self.imagen7 = tk.PhotoImage(file="carritoverde.png")
    self.imagen8 = tk.PhotoImage(file="carritonaranja.png")
    self.imagen9 = tk.PhotoImage(file="carritomorado.png")
    self.imagen10 = tk.PhotoImage(file="carritoneon.png")

    self.imagen_inicio = tk.PhotoImage(file="inicio.png")
    self.imagen_fin = tk.PhotoImage(file="fin.png")

    self.vehiculos = []
    y_pos = 0
    for img in [
        self.imagen1,
        self.imagen2,
        self.imagen3,
        self.imagen4,
        self.imagen5,
        self.imagen6,
        self.imagen7,
        self.imagen8,
        self.imagen9,
        self.imagen10,
    ]:
      v = tk.Label(self.ventana, image=img)
      v.place(x=0, y=y_pos)
      self.vehiculos.append(v)
      y_pos += 80

    self.marca_inicio = tk.Label(self.ventana, image=self.imagen_inicio)
    self.marca_inicio.place(x=95, y=0)

    self.marca_fin = tk.Label(self.ventana, image=self.imagen_fin)
    self.marca_fin.place(x=960, y=0)

    self.linea_principal = tk.Frame(self.ventana, bg="black")
    self.linea_principal.place(x=0, y=780, width=1000, height=10)

    for i in range(9):
      tk.Frame(self.ventana, bg="yellow").place(x=140, y=65 + (i * 80), width=820, height=5)

  def iniciar_carrera(self):
    if self.carrera_iniciada:
      return
    try:
      self.vehiculo_apostado = int(self.entrada_apuesta.get())
      self.numero_vueltas = int(self.entrada_vueltas.get())

      if not (1 <= self.vehiculo_apostado <= 10):
        self.mensaje.config(text="El vehículo debe estar entre 1 y 10")
        return
      if self.numero_vueltas <= 0:
        self.mensaje.config(text="Las vueltas deben ser mayores que cero")
        return
    except ValueError:
      self.mensaje.config(text="Ingrese números válidos")
      return

    self.carrera_iniciada = True
    self.carrera_terminada = False
    self.tiempos = [None] * 10
    self.vueltas = [0] * 10
    self.hilos = []

    self.tiempo_inicio = time.time()
    self.mensaje.config(text="La carrera ha comenzado", bg="green")
    self.resultados.config(text="")

    # Crear e iniciar un hilo independiente por cada vehículo (Requisito de la guía)
    for i in range(10):
      hilo = threading.Thread(target=self.ciclo_vehiculo, args=(i,))
      self.hilos.append(hilo)
      hilo.start()

  def ciclo_vehiculo(self, numero):
    vehiculo = self.vehiculos[numero]

    while not self.carrera_terminada:
      if self.vueltas[numero] >= self.numero_vueltas:
        break

      factor_velocidad = self.slider.get()
      avance = random.randint(2, 6) + int(factor_velocidad * 0.5)

      x_actual = vehiculo.winfo_x()
      nuevo_x = x_actual + avance

      if nuevo_x >= 900:
        nuevo_x = 0
        self.vueltas[numero] += 1

      vehiculo.place(x=nuevo_x)

      # Verificar si completó todas las vueltas
      if self.vueltas[numero] >= self.numero_vueltas:
        if self.tiempos[numero] is None:
          self.tiempos[numero] = time.time() - self.tiempo_inicio
          self.verificar_fin_carrera()
        break

      time.sleep(0.03)

  def verificar_fin_carrera(self):
    if all(t is not None for t in self.tiempos):
      self.carrera_terminada = True
      # Actualizar la interfaz desde el hilo principal de tkinter
      self.ventana.after(0, self.mostrar_resultados)

  def mostrar_resultados(self):
    resultados = sorted([(self.tiempos[i], i + 1) for i in range(10)], key=lambda x: x[0])

    texto = "RESULTADOS FINALES :\n"
    for posicion, (tiempo, vehiculo) in enumerate(resultados, start=1):
      texto += (f"{posicion}. Vehículo {vehiculo} - {round(tiempo, 2)} segundos\n")

    ganador = resultados[0][1]
    if ganador == self.vehiculo_apostado:
      texto += "¡Ganaste la apuesta!"
    else:
      texto += f"No ganaste. El ganador fue el vehículo {ganador}"

    self.resultados.config(text=texto)
    self.mensaje.config(text="La carrera terminó", bg="red")
    self.carrera_iniciada = False

  def reiniciar_carrera(self):
    self.carrera_terminada = True
    self.carrera_iniciada = False

    posiciones_y = [0, 80, 160, 240, 320, 400, 480, 560, 640, 720]
    for i in range(10):
      self.vehiculos[i].place(x=0, y=posiciones_y[i])

    self.mensaje.config(text="", bg="gold")
    self.resultados.config(text="")


if __name__ == "__main__":
  ventana = tk.Tk()
  app = Carrera(ventana)
  ventana.mainloop()