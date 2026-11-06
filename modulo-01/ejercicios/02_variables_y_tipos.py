# =============================================================
# Ejercicio 02 – Variables y Tipos de Datos en Python
# =============================================================
# En Python no necesitas declarar el tipo de una variable:
# simplemente asígnale un valor y Python lo infiere solo.
# Los tipos más comunes son:
#   str   → cadena de texto   ("hola")
#   int   → número entero     (8)
#   float → número decimal    (0.25)
#   bool  → verdadero/falso   (True / False)
#   list  → lista de valores  (["a", "b", "c"])
# =============================================================

# ------------------------------------------------------------------
# 1. str – Cadena de texto
# ------------------------------------------------------------------
curso = "RAG-LAB"
descripcion = "Aprende a construir sistemas RAG con Python"

print("=== str (cadena de texto) ===")
print("Curso:", curso)
print("Descripción:", descripcion)
print("Tipo:", type(curso))          # <class 'str'>

# Operaciones útiles con strings
print("Mayúsculas:", curso.upper())              # RAG-LAB → ya está en mayúsculas
print("Longitud:", len(descripcion), "chars")
print("Contiene 'RAG':", "RAG" in descripcion)  # True

# ------------------------------------------------------------------
# 2. int – Número entero
# ------------------------------------------------------------------
duracion_horas = 8
num_modulos = 5
ejercicios_por_modulo = 4

print("\n=== int (número entero) ===")
print("Duración:", duracion_horas, "horas")
print("Módulos:", num_modulos)
print("Total de ejercicios:", num_modulos * ejercicios_por_modulo)
print("Tipo:", type(duracion_horas))   # <class 'int'>

# ------------------------------------------------------------------
# 3. float – Número decimal
# ------------------------------------------------------------------
avance = 0.25
precio_usd = 49.99
promedio_nota = 8.7

print("\n=== float (número decimal) ===")
print("Avance actual:", avance)
print("Avance en %:", avance * 100, "%")
print("Precio:", precio_usd, "USD")
print("Promedio:", promedio_nota)
print("Tipo:", type(avance))           # <class 'float'>

# ------------------------------------------------------------------
# 4. bool – Booleano (verdadero / falso)
# ------------------------------------------------------------------
entorno_listo = True
tiene_api_key = False
modulo_completado = duracion_horas == 8   # expresión que evalúa a True

print("\n=== bool (verdadero / falso) ===")
print("Entorno listo:", entorno_listo)
print("Tiene API key:", tiene_api_key)
print("Módulo completado:", modulo_completado)
print("Tipo:", type(entorno_listo))     # <class 'bool'>

# Los booleans también funcionan en condiciones:
if entorno_listo:
    print("✓ ¡El entorno está configurado correctamente!")
else:
    print("✗ Todavía falta configurar el entorno.")

# ------------------------------------------------------------------
# 5. list – Lista de valores
# ------------------------------------------------------------------
herramientas = ["Python", "PyCharm", "Git", "GitHub"]
numeros = [1, 2, 3, 4, 5]
mixta = ["RAG-LAB", 2024, True, 9.5]   # una lista puede mezclar tipos

print("\n=== list (lista) ===")
print("Herramientas:", herramientas)
print("Tipo:", type(herramientas))      # <class 'list'>
print("Número de herramientas:", len(herramientas))
print("Primera herramienta:", herramientas[0])   # índice 0 = primero
print("Última herramienta:", herramientas[-1])   # índice -1 = último

print("\nHerramientas del módulo:")
for herramienta in herramientas:
    print("  -", herramienta)

# Agregar y quitar elementos
herramientas.append("OpenRouter")
print("\nTras agregar OpenRouter:", herramientas)

herramientas.remove("PyCharm")
print("Tras quitar PyCharm:", herramientas)

# Suma de una lista de números
print("\nSuma de", numeros, "=", sum(numeros))

# ------------------------------------------------------------------
# 6. Conversión entre tipos (casting)
# ------------------------------------------------------------------
print("\n=== Conversión de tipos ===")
numero_texto = "42"
numero_entero = int(numero_texto)       # str → int
numero_decimal = float(numero_texto)    # str → float
de_vuelta_texto = str(numero_entero)    # int → str

print("'42' como int:", numero_entero, "→ tipo:", type(numero_entero))
print("'42' como float:", numero_decimal, "→ tipo:", type(numero_decimal))
print("42 como str:", de_vuelta_texto, "→ tipo:", type(de_vuelta_texto))

# ------------------------------------------------------------------
# 7. Resumen con f-strings (forma moderna de formatear texto)
# ------------------------------------------------------------------
print("\n=== Resumen con f-string ===")
print(f"Curso       : {curso}")
print(f"Duración    : {duracion_horas} horas")
print(f"Avance      : {avance * 100:.0f}%")   # :.0f = 0 decimales
print(f"Entorno OK  : {entorno_listo}")
print(f"Herramientas: {', '.join(herramientas)}")
