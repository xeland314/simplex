# Simplex

## Ejemplo de uso práctico

Supongamos que tienes una empresa que produce dos productos, A y B. Cada unidad de producto A que produces te genera una ganancia de $3 y cada unidad de producto B te genera una ganancia de $4. Quieres maximizar tus ganancias totales.

Sin embargo, tienes algunas restricciones en la producción. Cada unidad de producto A requiere 2 horas de trabajo y cada unidad de producto B requiere 3 horas de trabajo. Tienes un total de 100 horas de trabajo disponibles. Además, cada unidad de producto A requiere 1 kg de materia prima y cada unidad de producto B requiere 2 kg de materia prima. Tienes un total de 80 kg de materia prima disponibles.

Este problema se puede formular como un problema de programación lineal con la siguiente función objetivo y restricciones:

```
Maximizar: 3A + 4B
Sujeto a:
    2A + 3B <= 100
    A + 2B <= 80
    A >= 0
    B >= 0
```

Donde `A` y `B` representan el número de unidades producidas de los productos A y B, respectivamente.

Para resolver este problema utilizando el programa en Python que te proporcioné anteriormente, puedes ingresar los siguientes valores cuando se te soliciten:

- Número de variables: `2`
- Coeficientes de la función objetivo: `3` y `4`
- Maximizar o minimizar: `1` (maximizar)
- Número de restricciones: `2`
- Restricción 1:
    - Coeficientes: `2` y `3`
    - Desigualdad: `<=`
    - Valor de `b`: `100`
- Restricción 2:
    - Coeficientes: `1` y `2`
    - Desigualdad: `<=`
    - Valor de `b`: `80`

Después de ingresar estos valores, el programa resolverá el problema y te mostrará la solución óptima. En este caso, la solución óptima es producir 20 unidades del producto A y 30 unidades del producto B para obtener una ganancia máxima de $180.

- Número de variables: `2`
- Coeficientes de la función objetivo: `4` y `1`
- Maximizar o minimizar: `0` (minimizar)
- Número de restricciones: `3`
- Restricción 1:
    - Coeficientes: `3` y `1`
    - Desigualdad: `=`
    - Valor de `b`: `3`
- Restricción 2:
    - Coeficientes: `4` y `3`
    - Desigualdad: `>=`
    - Valor de `b`: `6`
- Restricción 3:
    - Coeficientes: `1` y `2`
    - Desigualdad: `<=`
    - Valor de `b`: `4`


Claro, aquí está el problema en el formato que solicitaste:

- Número de variables: `4`
- Coeficientes de la función objetivo: `2`, `4`, `4` y `-3`
- Maximizar o minimizar: `1` (maximizar)
- Número de restricciones: `2`
- Restricción 1:
    - Coeficientes: `1`, `1`, `1` y `0`
    - Desigualdad: `=`
    - Valor de `b`: `4`
- Restricción 2:
    - Coeficientes: `1`, `4`, `0` y `1`
    - Desigualdad: `=`
    - Valor de `b`: `8`
