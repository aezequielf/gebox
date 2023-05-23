from datetime import datetime, timedelta

def genera_semana():
    # Obtenemos la fecha actual
    fecha_actual = datetime.now().date()

    # Calculamos el día de inicio de la semana (domingo)
    dia_inicio_semana = fecha_actual - timedelta(days=fecha_actual.weekday())

    # Creamos una lista con los días de la semana
    dias_semana = [dia_inicio_semana + timedelta(days=i) for i in range(7)]

    # Puedes pasar esta lista a tu plantilla para mostrar los días de la semana
    return dias_semana

def dia_num2let(dia:int):
    if dia == 0:
        return "Lunes"
    if dia == 1:
        return "Martes"
    if dia == 2:
        return "Miercoles"
    if dia == 3:
        return "Jueves"
    if dia == 4:
        return "Viernes"
    if dia == 5:
        return "Sabado"
    if dia == 6:
        return "Domingo"
    return "dia deconocido"

def dia_ab2com(dia:str):
    if dia == 'lu':
        return "Lunes"
    if dia == 'ma':
        return "Martes"
    if dia == 'mi':
        return "Miercoles"
    if dia == 'ju':
        return "Jueves"
    if dia == 'vi':
        return "Viernes"
    if dia == 'sa':
        return "Sabado"
    if dia == 'do':
        return "Domingo"
    return "dia deconocido"

def dia_ab2num(dia:str):
    if dia == 'lu':
        return 0
    if dia == 'ma':
        return 1
    if dia == 'mi':
        return 2
    if dia == 'ju':
        return 3
    if dia == 'vi':
        return 4
    if dia == 'sa':
        return 5
    if dia == 'do':
        return 6
    return "dia deconocido"

def dia_num2ab(dia:int):
    if dia == 0:
        return "lu"
    if dia == 1:
        return "ma"
    if dia == 2:
        return "mi"
    if dia == 3:
        return "ju"
    if dia == 4:
        return "vi"
    if dia == 5:
        return "sa"
    if dia == 6:
        return "do"
    return "dia deconocido"