import tkinter as tk
from tkinter import ttk
import threading
import random
import time


class Carrera:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Carrera de vehículos")
        self.ventana.geometry("1050x850")
        self.ventana.config(bg="white")

        self.carrera_iniciada = False
        self.cerrando = False
        self.reiniciando = False

        self.numero_vueltas = 1
        self.vehiculo_apostado = 1
        self.factor_velocidad = 1.0

        self.salida = 110
        self.meta = 880

        self.posiciones = [self.salida] * 10
        self.vueltas = [0] * 10
        self.tiempos = [None] * 10

        self.hilos = []
        self.imagenes = []
        self.vehiculos = []
        self.etiquetas_vueltas = []

        self.lock = threading.Lock()
        self.detener = threading.Event()
        self.salida_carrera = threading.Event()

        self.crear_interfaz()

        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.ventana.after(30, self.actualizar_pantalla)

    def crear_interfaz(self):
        tk.Label(
            self.ventana,
            text="Carrera de vehículos",
            font=("Arial", 22),
            bg="white"
        ).place(x=340, y=10)

        self.crear_pista()

        tk.Label(
            self.ventana,
            text="Apostar por vehículo:",
            bg="white"
        ).place(x=20, y=520)

        self.entrada_apuesta = tk.Entry(self.ventana, width=5)
        self.entrada_apuesta.place(x=155, y=520)
        self.entrada_apuesta.insert(0, "1")

        tk.Label(
            self.ventana,
            text="Rondas:",
            bg="white"
        ).place(x=220, y=520)

        self.entrada_vueltas = tk.Entry(self.ventana, width=5)
        self.entrada_vueltas.place(x=280, y=520)
        self.entrada_vueltas.insert(0, "1")

        tk.Label(
            self.ventana,
            text="Velocidad general:",
            bg="white"
        ).place(x=350, y=520)

        self.slider = tk.Scale(
            self.ventana,
            from_=0.5,
            to=3.0,
            resolution=0.1,
            orient="horizontal",
            length=180,
            command=self.cambiar_velocidad
        )
        self.slider.set(1.0)
        self.slider.place(x=470, y=495)

        self.boton_iniciar = tk.Button(
            self.ventana,
            text="Iniciar",
            command=self.iniciar_carrera,
            width=12
        )
        self.boton_iniciar.place(x=690, y=515)

        self.boton_reiniciar = tk.Button(
            self.ventana,
            text="Reiniciar",
            command=self.reiniciar_carrera,
            width=12
        )
        self.boton_reiniciar.place(x=810, y=515)

        self.mensaje = tk.Label(
            self.ventana,
            text="Una ronda equivale a una ida y una vuelta.",
            font=("Arial", 11),
            bg="white"
        )
        self.mensaje.place(x=20, y=565)

        self.resultados = ttk.Treeview(
            self.ventana,
            columns=("puesto", "vehiculo", "tiempo"),
            show="headings",
            height=10
        )

        self.resultados.heading("puesto", text="Puesto")
        self.resultados.heading("vehiculo", text="Vehículo")
        self.resultados.heading("tiempo", text="Tiempo real (s)")

        self.resultados.column("puesto", width=100, anchor="center")
        self.resultados.column("vehiculo", width=150, anchor="center")
        self.resultados.column("tiempo", width=180, anchor="center")

        self.resultados.place(x=300, y=605)

    def crear_pista(self):
        archivos = [
            "carritoblanco.png",
            "carritoazul.png",
            "carritoamarillo.png",
            "carritorojo.png",
            "carritobeage.png",
            "carritonegro.png",
            "carritoverde.png",
            "carritonaranja.png",
            "carritomorado.png",
            "carritoneon.png"
        ]

        tk.Label(
            self.ventana, text="SALIDA", bg="white"
        ).place(x=self.salida, y=50)

        tk.Label(
            self.ventana, text="META", bg="white"
        ).place(x=self.meta, y=50)

        for i in range(10):
            y = 80 + i * 42

            tk.Label(
                self.ventana,
                text=f"Carro {i + 1}",
                bg="white"
            ).place(x=10, y=y + 5)

            linea = tk.Frame(self.ventana, bg="gray")
            linea.place(
                x=self.salida,
                y=y + 34,
                width=self.meta - self.salida + 65,
                height=2
            )

            imagen = tk.PhotoImage(file=archivos[i])

            # Reducir imágenes grandes sin instalar otras librerías.
            factor = max(
                1,
                (imagen.width() + 59) // 60,
                (imagen.height() + 29) // 30
            )
            imagen = imagen.subsample(factor, factor)

            self.imagenes.append(imagen)

            vehiculo = tk.Label(
                self.ventana,
                image=imagen,
                bg="white",
                borderwidth=0
            )
            vehiculo.place(x=self.salida, y=y)
            self.vehiculos.append(vehiculo)

            etiqueta = tk.Label(
                self.ventana,
                text="0 rondas",
                bg="white"
            )
            etiqueta.place(x=955, y=y + 5)
            self.etiquetas_vueltas.append(etiqueta)

    def cambiar_velocidad(self, valor):
        with self.lock:
            self.factor_velocidad = float(valor)

    def iniciar_carrera(self):
        if self.carrera_iniciada or self.reiniciando:
            return

        try:
            apuesta = int(self.entrada_apuesta.get())
            rondas = int(self.entrada_vueltas.get())

            if apuesta < 1 or apuesta > 10:
                self.mensaje.config(
                    text="El vehículo debe estar entre 1 y 10."
                )
                return

            if rondas <= 0:
                self.mensaje.config(
                    text="Las rondas deben ser mayores que cero."
                )
                return

        except ValueError:
            self.mensaje.config(
                text="Ingrese números enteros válidos."
            )
            return

        self.vehiculo_apostado = apuesta
        self.numero_vueltas = rondas

        self.limpiar_datos()

        self.detener.clear()
        self.salida_carrera.clear()
        self.carrera_iniciada = True

        self.boton_iniciar.config(state="disabled")
        self.entrada_apuesta.config(state="disabled")
        self.entrada_vueltas.config(state="disabled")

        self.mensaje.config(text="La carrera ha comenzado.")

        self.hilos = []

        for i in range(10):
            hilo = threading.Thread(
                target=self.mover_vehiculo,
                args=(i,),
                name=f"Carro-{i + 1}"
            )
            self.hilos.append(hilo)
            hilo.start()

        # Todos usan el mismo instante inicial.
        self.tiempo_inicio = time.perf_counter()
        self.salida_carrera.set()

    def mover_vehiculo(self, numero):
        self.salida_carrera.wait()

        posicion = float(self.salida)
        direccion = 1
        rondas_completadas = 0
        velocidad = random.randint(100, 180)

        tiempo_anterior = self.tiempo_inicio

        while not self.detener.is_set():
            ahora = time.perf_counter()
            intervalo = ahora - tiempo_anterior
            tiempo_anterior = ahora

            with self.lock:
                factor = self.factor_velocidad

            movimiento = velocidad * intervalo * factor
            posicion = posicion + movimiento * direccion

            if direccion == 1 and posicion >= self.meta:
                posicion = float(self.meta)
                direccion = -1
                velocidad = random.randint(100, 180)

            elif direccion == -1 and posicion <= self.salida:
                posicion = float(self.salida)
                direccion = 1

                rondas_completadas += 1
                velocidad = random.randint(100, 180)

            with self.lock:
                self.posiciones[numero] = posicion
                self.vueltas[numero] = rondas_completadas

                if rondas_completadas >= self.numero_vueltas:
                    self.tiempos[numero] = (
                        ahora - self.tiempo_inicio
                    )
                    return

            # Esperar sin consumir continuamente el procesador.
            # También permite reaccionar al reinicio o al cierre.
            self.detener.wait(0.02)

    def actualizar_pantalla(self):
        if self.cerrando:
            return

        with self.lock:
            posiciones = self.posiciones.copy()
            vueltas = self.vueltas.copy()
            tiempos = self.tiempos.copy()

        for i in range(10):
            self.vehiculos[i].place(x=int(posiciones[i]))

            self.etiquetas_vueltas[i].config(
                text=f"{vueltas[i]} rondas"
            )

        if self.carrera_iniciada and not self.reiniciando:
            if all(tiempo is not None for tiempo in tiempos):
                self.finalizar_carrera(tiempos)

        self.ventana.after(30, self.actualizar_pantalla)

    def finalizar_carrera(self, tiempos):
        # Esperar sin bloquear la ventana si algún hilo aún sale.
        if any(hilo.is_alive() for hilo in self.hilos):
            return

        self.carrera_iniciada = False

        clasificacion = []

        for i in range(10):
            clasificacion.append((tiempos[i], i + 1))

        clasificacion.sort()

        for puesto, resultado in enumerate(clasificacion, start=1):
            tiempo, vehiculo = resultado

            self.resultados.insert(
                "",
                "end",
                values=(puesto, vehiculo, f"{tiempo:.3f}")
            )

        ganador = clasificacion[0][1]

        if ganador == self.vehiculo_apostado:
            texto = f"¡Ganaste la apuesta! Ganó el carro {ganador}."
        else:
            texto = (
                f"No ganaste la apuesta. Ganó el carro {ganador}."
            )

        self.mensaje.config(text=texto)

        self.boton_iniciar.config(state="normal")
        self.entrada_apuesta.config(state="normal")
        self.entrada_vueltas.config(state="normal")

    def limpiar_datos(self):
        with self.lock:
            self.posiciones = [self.salida] * 10
            self.vueltas = [0] * 10
            self.tiempos = [None] * 10

        for fila in self.resultados.get_children():
            self.resultados.delete(fila)

    def reiniciar_carrera(self):
        if self.reiniciando:
            return

        self.reiniciando = True
        self.detener.set()

        self.boton_iniciar.config(state="disabled")
        self.boton_reiniciar.config(state="disabled")

        self.mensaje.config(text="Reiniciando...")
        self.esperar_reinicio()

    def esperar_reinicio(self):
        if any(hilo.is_alive() for hilo in self.hilos):
            self.ventana.after(30, self.esperar_reinicio)
            return

        self.carrera_iniciada = False
        self.reiniciando = False
        self.hilos = []

        self.limpiar_datos()

        self.entrada_apuesta.config(state="normal")
        self.entrada_vueltas.config(state="normal")
        self.boton_iniciar.config(state="normal")
        self.boton_reiniciar.config(state="normal")

        self.mensaje.config(
            text="Seleccione su apuesta y el número de rondas."
        )

    def cerrar(self):
        self.cerrando = True
        self.detener.set()
        self.esperar_cierre()

    def esperar_cierre(self):
        if any(hilo.is_alive() for hilo in self.hilos):
            self.ventana.after(30, self.esperar_cierre)
        else:
            self.ventana.destroy()


if __name__ == "__main__":
    ventana = tk.Tk()
    objeto = Carrera(ventana)
    ventana.mainloop()