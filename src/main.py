def calculate(expression: str) -> float:
    """
    Evalúa una expresión aritmética con operaciones básicas (suma, resta,
    multiplicación y división) y paréntesis. Además, maneja operadores unarios
    (por ejemplo, "-10 / 2") y distingue entre enteros y decimales para retornar
    el resultado sin decimales innecesarios.

    Parámetros:
      expression: str - La cadena con la expresión (ejemplo: "2 + 2").

    Retorna:
      float o int - El resultado de la evaluación. Si el resultado es un número
      entero, se retorna como int; de lo contrario se retorna como float.

    Lanza:
      SyntaxError si la sintaxis es incorrecta.
      ValueError si se encuentra un carácter inválido o la entrada está vacía.
      ZeroDivisionError si ocurre una división por cero.
    """
    s = expression.strip()
    if s == "":
        raise ValueError("Entrada vacía")

    i = 0  # Índice actual en la cadena

    def skip_whitespace():
        nonlocal i
        while i < len(s) and s[i].isspace():
            i += 1

    def parse_number():
        nonlocal i
        skip_whitespace()
        start = i
        # Recolecta dígitos y el punto decimal
        while i < len(s) and (s[i].isdigit() or s[i] == '.'):
            i += 1
        if start == i:
            raise SyntaxError("Sintaxis inválida: se esperaba un número.")
        num_str = s[start:i]
        if '.' in num_str:
            return float(num_str)
        else:
            return int(num_str)

    def parse_factor():
        nonlocal i
        skip_whitespace()
        # Manejo de operador unario + o -
        if i < len(s) and s[i] in "+-":
            op = s[i]
            i += 1
            factor_val = parse_factor()
            return factor_val if op == '+' else -factor_val
        skip_whitespace()
        # Manejo de paréntesis
        if i < len(s) and s[i] == "(":
            i += 1  # omite '('
            result = parse_expression()
            skip_whitespace()
            if i >= len(s) or s[i] != ")":
                raise SyntaxError("Sintaxis inválida: se esperaba ')'.")
            i += 1  # omite ')'
            return result
        else:
            return parse_number()

    def parse_term():
        nonlocal i
        result = parse_factor()
        while True:
            skip_whitespace()
            if i < len(s) and s[i] in "*/":
                op = s[i]
                i += 1
                right = parse_factor()
                if op == "*":
                    result *= right
                else:
                    result /= right
            else:
                break
        return result

    def parse_expression():
        nonlocal i
        result = parse_term()
        while True:
            skip_whitespace()
            if i < len(s) and s[i] in "+-":
                op = s[i]
                i += 1
                right = parse_term()
                if op == "+":
                    result += right
                else:
                    result -= right
            else:
                break
        return result

    result = parse_expression()
    skip_whitespace()
    if i != len(s):
        raise ValueError("Entrada inválida: quedan caracteres sin procesar.")

    # Redondea el resultado y convierte a entero si es numéricamente exacto
    if isinstance(result, float):
        rounded_result = round(result, 10)
        if rounded_result.is_integer():
            return int(rounded_result)
        else:
            return rounded_result
    return result


# Modo interactivo (opcional)
if __name__ == "__main__":
    print("Calculadora en línea de comandos")
    print('Ingrese una operación completa (ejemplo: 2 + 2) y presione Enter para calcular.')
    print("Si ingresa la letra 'c' se borrará la operación actual.")
    print("Escriba 'salir' para terminar el programa.\n")
    
    while True:
        entrada = input("Operación: ").strip()
        # Salir si se ingresa "salir"
        if entrada.lower() == "salir":
            print("Saliendo de la calculadora. ¡Hasta luego!")
            break
        # Borrar si se ingresa "c"
        if entrada.lower() == "c":
            print("Operación borrada.\n")
            continue
        try:
            resultado = calculate(entrada)
            print("Resultado:", resultado, "\n")
        except Exception as e:
            print("Error:", e, "\n")
