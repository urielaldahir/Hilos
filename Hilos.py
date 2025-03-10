import tkinter as tk
from tkinter import messagebox, ttk
import math
import pickle
import threading

# Guardar el estado en un archivo
def save_state(entry, history):
    state = {
        "entry": entry,
        "history": history
    }
    with open("calculator_state.pkl", "wb") as f:
        pickle.dump(state, f)

# Cargar el estado desde un archivo
def load_state():
    try:
        with open("calculator_state.pkl", "rb") as f:
            state = pickle.load(f)
            return state["entry"], state["history"]
    except FileNotFoundError:
        return "", ""

# Almacenar el número original antes de la conversión
original_number = None

# Función para realizar cálculos en un hilo
def calculate_expression(expression):
    try:
        # Reemplazar operadores y realizar el cálculo
        result = eval(expression, {"sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log10, "ln": math.log,
                                   "sqrt": math.sqrt, "pi": math.pi, "e": math.e, "factorial": math.factorial,
                                   "deg": math.degrees})
        # Actualizar la interfaz gráfica con el resultado
        entry_var.set(str(result))
        history_var.set(history_var.get() + expression + " = " + str(result) + "\n")
    except Exception as e:
        messagebox.showerror("Error", "Expresión inválida")

# Función de conversión de números
def convert_number():
    global original_number
    conversion_type = conversion_var.get()

    try:
        # Si el número original no está almacenado, guardar el valor actual
        if original_number is None:
            original_number = entry_var.get()

        # Si se selecciona "Decimal", restaurar el número original
        if conversion_type == "Decimal":
            entry_var.set(original_number)
            return

        # Convertir a entero desde el valor original
        num = int(original_number)

        # Realizar la conversión
        if conversion_type == "Binario":
            result = bin(num)[2:]
        elif conversion_type == "Octal":
            result = oct(num)[2:]
        elif conversion_type == "Hexadecimal":
            result = hex(num)[2:].upper()
        else:
            result = str(num)

        entry_var.set(result)

    except ValueError:
        messagebox.showerror("Error", "Ingrese un número válido para convertir")

# Función al hacer clic en un botón
def on_click(button_text):
    global new_result, original_number
    if button_text == "AC":
        entry_var.set("")
        history_var.set("")
        original_number = None  # Resetear número original
        new_result = False
    elif button_text == "←":
        entry_var.set(entry_var.get()[:-1])
    elif button_text == "=":
        expression = entry_var.get().replace("×", "*").replace("÷", "/").replace("^", "**")
        if expression and not expression.endswith("=") and "=" not in history_var.get().split("\n")[-1]:
            # Crear un hilo para calcular la expresión
            calculation_thread = threading.Thread(target=calculate_expression, args=(expression,))
            calculation_thread.start()
            new_result = True
    else:
        if new_result:
            if button_text.isdigit() or button_text in ["sin", "cos", "tan", "lg", "ln", "deg", "sqrt", "x^y"]:
                entry_var.set("")
            new_result = False

        current_text = entry_var.get()
        if button_text in ["sin", "cos", "tan", "lg", "ln", "deg"]:
            entry_var.set(current_text + button_text + "(")
        elif button_text == "x^y":
            if current_text and current_text[-1].isdigit():
                entry_var.set(current_text + "^")
        elif button_text.isdigit():
            if current_text and current_text[-1] == "0" and (len(current_text) == 1 or not current_text[-2].isdigit()):
                entry_var.set(current_text[:-1] + button_text)
            else:
                entry_var.set(current_text + button_text)
        else:
            entry_var.set(current_text + button_text)

# Crear la ventana principal
root = tk.Tk()
root.title("Calculadora Científica")
root.geometry("400x650")
root.configure(bg="#2E2E2E")

# Cargar el estado anterior
entry_text, history_text = load_state()

entry_var = tk.StringVar(value=entry_text)
entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 20), justify="right", bd=10, relief=tk.GROOVE,
                 bg="#A4A4A4", fg="black")
entry.pack(fill="both")

# Área de historial
history_var = tk.StringVar(value=history_text)
history_label = tk.Label(root, textvariable=history_var, font=("Arial", 12), justify="left", anchor="w", height=5,
                         bg="#6E6E6E", fg="white")
history_label.pack(fill="both")

new_result = False

# Dropdown para conversiones
conversion_var = tk.StringVar(value="Decimal")

conversion_menu = ttk.Combobox(root, textvariable=conversion_var, values=["Decimal", "Binario", "Octal", "Hexadecimal"], state="readonly")
conversion_menu.pack(fill="both", padx=10, pady=5)
convert_button = tk.Button(root, text="Convertir", command=convert_number, bg="#424242", fg="white")
convert_button.pack(fill="both", padx=10, pady=5)

# Crear botones
buttons = [
    ("2nd", "deg", "sin", "cos", "tan"),
    ("x^y", "lg", "ln", "(", ")"),
    ("sqrt", "AC", "←", "%", "÷"),
    ("x!", "7", "8", "9", "×"),
    ("1/x", "4", "5", "6", "-"),
    ("pi", "1", "2", "3", "+"),
    ("e", "0", ".", "=", "")
]

frame = tk.Frame(root, bg="#2E2E2E")
frame.pack(expand=True, fill="both")

for row_values in buttons:
    row_frame = tk.Frame(frame, bg="#2E2E2E")
    row_frame.pack(expand=True, fill="both")
    for value in row_values:
        if value:
            button = tk.Button(row_frame, text=value, font=("Arial", 15), command=lambda v=value: on_click(v), width=5,
                               height=2, bg="#424242", fg="white", activebackground="#585858", activeforeground="white")
            button.pack(side="left", expand=True, fill="both")

# Guardar el estado al cerrar la ventana
def on_close():
    save_state(entry_var.get(), history_var.get())
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
