# Taller 2: Motor de Inferencia para Fraude Bancario

## Objetivo

Aplicar encadenamiento hacia adelante para deducir si una transaccion bancaria debe bloquearse. El motor revisa las reglas repetidamente y agrega a la memoria cada conclusion nueva.

## Como ejecutar la aplicacion

La forma mas sencilla es abrir con doble clic el archivo **Ejecutar motor de fraude.bat**. Se abrira una ventana de Windows con los controles de la transaccion y el resultado del analisis.

Tambien puede iniciarse desde PowerShell:

Se necesita Python 3. Ejecutar desde esta carpeta:

```text
python motor_fraude.py
```

Si Windows tiene el lanzador `py` configurado:

```text
py motor_fraude.py
```

La aplicacion usa Tkinter, una biblioteca incluida normalmente con Python, por lo que no requiere instalar paquetes externos.

## Hechos iniciales

- `monto = 6500`
- `pais_extranjero = True`
- `hora_inusual = True`
- `cliente_desconoce = True`
- `monto_alto = monto > 5000`, por lo que vale `True`

## Reglas

- **R1:** Si `monto_alto` es verdadero, entonces `transaccion_inusual` es verdadero.
- **R2:** Si `transaccion_inusual` y `pais_extranjero` son verdaderos, entonces `riesgo_alto` es verdadero.
- **R3:** Si `riesgo_alto` y `cliente_desconoce` son verdaderos, entonces `bloquear_tarjeta` es verdadero.
- **R4:** Si `hora_inusual` y `transaccion_inusual` son verdaderos, entonces `generar_alerta` es verdadero.

En cada regla, `all()` comprueba que todas las condiciones se cumplan. Esto representa la operacion logica AND.

## Traza esperada

```text
R1 -> transaccion_inusual = True
R2 -> riesgo_alto = True
R3 -> bloquear_tarjeta = True
R4 -> generar_alerta = True

Resultado:
Bloquear Tarjeta
```

## Conclusion

El motor llega a `bloquear_tarjeta = True` mediante varias aplicaciones de Modus Ponens:

1. El monto es mayor que 5000, por lo que la transaccion es inusual.
2. La transaccion inusual ocurre en un pais extranjero, por lo que el riesgo es alto.
3. El cliente desconoce la operacion y el riesgo es alto, por lo que se bloquea la tarjeta.
4. La hora inusual genera una alerta adicional.
