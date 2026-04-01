import matplotlib.pyplot as plt
import numpy as np

# 1. Definir los datos (valores x e y)
x = np.linspace(0, 10, 100)  # Genera 100 puntos entre 0 y 10
y = np.sin(x)  # Calcula el seno de cada punto


# 2. Crear el gráfico
plt.figure(figsize=(8, 4))  # Opcional: ajustar el tamaño de la figura
plt.plot(
    x, y, label="Seno(x)", color="blue"
)  # Dibujar los datos con una etiqueta y color

# 3. Personalizar el gráfico
plt.title("Gráfico de la función Seno")  # Añadir título
plt.xlabel("Eje X")  # Etiqueta para el eje X
plt.ylabel("Eje Y")  # Etiqueta para el eje Y
plt.grid(True)  # Añadir rejilla
plt.legend()  # Mostrar la leyenda
plt.plot(x, y)
# plt.title("Gráfico en Termux")


# 4. Mostrar el gráfico
# Reemplaza plt.show() por savefig
plt.savefig("mi_grafico.png")
print("Gráfico guardado como 'mi_grafico.png'")
