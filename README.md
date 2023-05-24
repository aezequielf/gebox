### Nombre del proyecto :::gebox::::
Gestion de Box (por ahora solo agenda ;-P)
Proyecto para gestionar agenda de clases de de gimnacio con límites de cupos.

Paso 1 
Generar las migraciones.
Paso 2 
Crear el superusuario
     Con esto debería quedar habilitado el registro de usuarios
Paso 3
Genarar los parametros de la agenda (dias y horas de los turnos disponibles), tener en cuenta que se cargan solo las dos primeras letras del día en español, y el horario se debe ingresar hora:minutos por más que sean 0, como por ejemplo 19:00.
Paso 4
Desde el admin de turnos generar primero 1 la primera vez para que habilite el acceso a las funciones. Se debe seleccionar si o si un turno porque el panel solicita un queryset de al menos 1 elemento, sino da error y no genera nada. 
  En este punto logueados al sistema la agenda debería ser ya accesible.