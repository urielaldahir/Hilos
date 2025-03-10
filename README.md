# Hilos
Calculadora cientifica , la cual lleva implementada consigo un checkpoint para poder guardar su status si el usuario cierra la interfaz de manera intencional o no intencional.
Adicional ya también se le integró hilos, es una buena opción para evitar bloqueos en la GUI cuando el cálculo es pesado. Aunque ya que lo hago con TKinter puede llegar a fallar en cierto punto.

•	Función calculate_expression(expression)
o	Se encarga de evaluar la expresión matemática en un hilo separado.
o	Usa eval() con una lista de funciones matemáticas seguras.
o	Actualiza la interfaz con el resultado o muestra un error si la expresión es inválida.
•	Creación de un hilo en on_click(button_text)
o	Cuando el usuario presiona =, se crea un nuevo hilo con threading.Thread().
o	Este hilo llama a calculate_expression(expression), evitando que la interfaz de Tkinter se congele.
o	Se usa .start() para ejecutar el cálculo en segundo plano.

<img src="https://github.com/user-attachments/assets/24cf0198-8f5a-4850-9aaf-2ea8343cf65d" width="300" />


