import matplotlib.pyplot as plt
x=[1,2,3,4,5,6,7]
y=[1,2,3,4,5,6,7]
z=[2,4,6,7,2,7,9]
plt.plot(x,y,color='red',linewidth=3)
plt.plot(x,z,color='green',linestyle='--',marker='o')
plt.title("grafico simple")

plt.grid()
plt.xlabel("Tiempo")
plt.xlabel("voltaje")
plt.show()