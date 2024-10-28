# Proyecto_IA_Smart-horses

# Smart Horses Game

Smart Horses es un juego de estrategia en el que dos jugadores controlan caballos en un tablero de ajedrez, con el objetivo de obtener la mayor cantidad de puntos.

## Reglas del Juego

- El juego se juega entre dos jugadores, uno controla el caballo blanco y el otro el caballo negro.
- En el tablero hay 10 casillas que otorgan de 1 a 10 puntos al primer caballo que las alcance.
- Además, hay 4 casillas marcadas con el símbolo 'x2' que permiten duplicar la puntuación de la casilla alcanzada.
- Los símbolos 'x2' no son acumulables, es decir, solo se puede aplicar uno por caballo.
- El juego termina cuando no quedan más casillas con puntos.
- El jugador con la mayor cantidad de puntos al final del juego es declarado el ganador.

## Niveles de Dificultad

El juego ofrece tres niveles de dificultad:

1. **Principiante**: El árbol minimax tiene una profundidad de búsqueda de 2.
2. **Amateur**: El árbol minimax tiene una profundidad de búsqueda de 4.
3. **Experto**: El árbol minimax tiene una profundidad de búsqueda de 6.

## Implementación de las IA's

Para este proyecto, se deben crear dos agentes de Inteligencia Artificial (IA) con diferentes funciones de utilidad heurística:

1. **IA1 (Maximizar puntos)**: Esta IA se enfocará en maximizar la cantidad de puntos que puede obtener. Considerará factores como la distancia a las casillas de puntos, la posibilidad de alcanzar casillas 'x2' y el control del centro del tablero.

2. **IA2 (Minimizar puntos del oponente)**: Esta IA se enfocará en minimizar los puntos que puede obtener el oponente. Considerará factores como el bloqueo de las casillas de puntos del oponente, la cercanía a las casillas 'x2' del oponente y el control de las casillas centrales.

## Enfrentamientos y Evaluación

Se deben realizar 10 enfrentamientos entre las dos IA's para cada combinación de niveles de dificultad, siempre iniciando la IA1. Los resultados se deben registrar en una tabla con el siguiente formato:

IA2
Principiante | Amateur | Experto
-------------|---------|--------
IA1
Principiante | [x, y, z] | 
Amateur      |         |
Experto      |         |

Donde `x`, `y` y `z` representan las victorias de IA1, victorias de IA2 y empates, respectivamente.

Basado en los resultados obtenidos, se debe seleccionar la IA más efectiva para incluirla en el juego final.

## Entregables

1. **Código Fuente**: El código fuente completo del juego Smart Horses.
2. **Informe Técnico**: Un informe que incluya:
   - Definición y explicación detallada de las funciones de utilidad heurística de IA1 e IA2.
   - La tabla con los resultados de los enfrentamientos entre las IA's.
   - El análisis de los resultados y la selección de la IA más efectiva.
3. **Video Demostrativo**: Un video que muestre 10 enfrentamientos entre las dos IA's.

¡Que disfrutes desarrollando este interesante proyecto de Inteligencia Artificial!
