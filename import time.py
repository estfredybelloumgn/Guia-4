import time 

class Cronometro:

    def __init__(self):
        self.start_time = None
    def start(self):
        self.start_time = time.time()
    def stop(self):
        if self.start_time is None:
            raise ValueError("El cronometro no ha sido iniciado.",)
            elapsed_time = time.time() - self.start_time
            self.start_time = None
return elapsed_time

# Uso
objeto = Cronometro()
objeto.start() #inicio el cronometro
time.sleep(2.5)
elapsed_time = objeto.stop() #esta funcion detiene el cronometro y
#devuelve la resta de tiempos
print(f"Tiempo de duracion: {(elapsed_time)*1000:.2f} milisegundos") #se
# muestra la duracion de la tarea en milisegundos
