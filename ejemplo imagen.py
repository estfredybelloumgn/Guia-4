import tkinter as tk


ventana=tk.Tk()
ventana.config()
ventana.title("Carrera")
ventana.grid()
ventana.geometry("1000x1200")
## carritos
imagen=tk.PhotoImage(file="carritoblanco.png")
obj1=tk.Label(ventana,image=imagen)
obj1.place(x=0,y=0)

imagen2=tk.PhotoImage(file="carritoazul.png")
obj2=tk.Label(ventana,image=imagen2)
obj2.place(x=0,y=80)

imagen3=tk.PhotoImage(file="carritoamarillo.png")
obj3=tk.Label(ventana,image=imagen3)
obj3.place(x=0,y=160)

imagen4=tk.PhotoImage(file="carritorojo.png")
obj4=tk.Label(ventana,image=imagen4)
obj4.place(x=0,y=240)

imagen5=tk.PhotoImage(file="carritobeage.png")
obj5=tk.Label(ventana,image=imagen5)
obj5.place(x=0,y=320)

imagen6=tk.PhotoImage(file="carritonegro.png")
obj6=tk.Label(ventana,image=imagen6)
obj6.place(x=0,y=400)

imagen7=tk.PhotoImage(file="carritoverde.png")
obj7=tk.Label(ventana,image=imagen7)
obj7.place(x=0,y=480)

imagen8=tk.PhotoImage(file="carritonaranja.png")
obj8=tk.Label(ventana,image=imagen8)
obj8.place(x=0,y=560)

imagen9=tk.PhotoImage(file="carritomorado.png")
obj9=tk.Label(ventana,image=imagen9)
obj9.place(x=0,y=640)

imagen10=tk.PhotoImage(file="carritoneon.png")
obj10=tk.Label(ventana,image=imagen10)
obj10.place(x=0,y=720)

## marcas inicio fin
imagen11=tk.PhotoImage(file="inicio.png")
obj11=tk.Label(ventana,image=imagen11)
obj11.place(x=95,y=0)

imagen12=tk.PhotoImage(file="fin.png")
obj12=tk.Label(ventana,image=imagen12)
obj12.place(x=960,y=0)

frame1=tk.Frame(ventana,bg='black')
frame1.place(x=0,y=800,width=1000,height=10)

frame2=tk.Frame(ventana,bg='yellow')
frame2.place(x=140,y=705,width=820,height=5)

frame3=tk.Frame(ventana,bg='yellow')
frame3.place(x=140,y=625,width=820,height=5)

frame4=tk.Frame(ventana,bg='yellow')
frame4.place(x=140,y=545,width=820,height=5)

frame5=tk.Frame(ventana,bg='yellow')
frame5.place(x=140,y=465,width=820,height=5)

frame6=tk.Frame(ventana,bg='yellow')
frame6.place(x=140,y=385,width=820,height=5)

frame7=tk.Frame(ventana,bg='yellow')
frame7.place(x=140,y=305,width=820,height=5)

frame8=tk.Frame(ventana,bg='yellow')
frame8.place(x=140,y=225,width=820,height=5)

frame9=tk.Frame(ventana,bg='yellow')
frame9.place(x=140,y=145,width=820,height=5)

frame10=tk.Frame(ventana,bg='yellow')
frame10.place(x=140,y=65,width=820,height=5)

boton1=tk.Button(text="Start",font=("arial",12),bg='green')
boton1.place(x=0,y=810,width=70,height=30)

boton2=tk.Button(text="Re start",font=("arial",12),bg='blue')
boton2.place(x=0,y=850,width=70,height=30)

ventana.mainloop()

