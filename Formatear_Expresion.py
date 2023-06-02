def Formatear(expresion_reg):
    expresion_form = []
    print("\nLa expresion regular ingresada es: ", expresion_reg, "\n")
    todosOperadores = ['|', '?', '+', '*', '^']
    operadoresBinarios = ['|', '^']
    if len(expresion_reg) > 0:
        i = 0
        while i < len(expresion_reg):
            c1 = expresion_reg[i]
            if (i + 1) < len(expresion_reg):
                c2 = expresion_reg[i + 1]
                expresion_form.append(c1)
                if (c1 != '(') and (c2 != ')') and (c2 not in todosOperadores) and (c1 not in operadoresBinarios) and (c2 != '\\'):
                    expresion_form.append('.')
                elif (c1 == '\\'):
                    expresion_form.append(c2)
                    i += 1
            i += 1
        expresion_form.append(expresion_reg[len(expresion_reg) - 1])
        expresion_form_final = ''.join(expresion_form)
        print("La expresion regular formateada es: ", expresion_form_final, "\n")
        return expresion_form_final
    else:
        print("La Expresion Regular ingresada esta vacia\n")
        return None
