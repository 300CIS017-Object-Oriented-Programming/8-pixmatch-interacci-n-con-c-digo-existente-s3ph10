# Requisitos Funcionales y Criterios de Aceptación

## 1. Configuración de Nivel de Dificultad

### Requisito:
El sistema debe permitir a los jugadores seleccionar el nivel de dificultad antes de comenzar el juego.

### Criterios de Aceptación:
- Opciones de dificultad fácil, medio y difícil disponibles para selección.
- La configuración de dificultad debe influir en la mecánica del juego, como la frecuencia de regeneración de imágenes y la puntuación.
- Tiempos de regeneración específicos:
  - Fácil: cada 8 segundos.
  - Medio: cada 6 segundos.
  - Difícil: cada 5 segundos.

## 2. Inicio de un Nuevo Juego

### Requisito:
El sistema debe permitir a los jugadores iniciar un nuevo juego una vez que se ha seleccionado el nivel de dificultad.

### Criterios de Aceptación:
- Al hacer clic en el botón "Nuevo Juego", se restablece el tablero con una nueva configuración de imágenes y se comienza el juego.

## 3. Visualización de la Puntuación

### Requisito:
El sistema debe mostrar la puntuación del jugador durante el juego.

### Criterios de Aceptación:
- La puntuación del jugador debe mostrarse en tiempo real durante el juego.
- La puntuación debe actualizarse según las acciones del jugador, como seleccionar imágenes correctas o incorrectas.

## 4. Finalización del Juego

### Requisito:
El sistema debe detectar cuándo se completa el juego.

### Criterios de Aceptación:
- El juego debe finalizar cuando se han emparejado todas las imágenes correctamente o cuando se alcanza un número máximo de intentos fallidos.
- Una vez que se alcanza el final del juego, se muestra una pantalla de fin de juego con la puntuación final del jugador y opciones para regresar al menú principal o iniciar un nuevo juego.

## 5. Lógica de Emparejamiento de Imágenes

### Requisito:
El sistema debe verificar si las imágenes seleccionadas por el jugador forman un par coincidente.

### Criterios de Aceptación:
- Cuando el jugador selecciona dos imágenes, el sistema debe compararlas para determinar si son iguales.
- Si las imágenes son iguales, se considera un emparejamiento correcto y se otorga una puntuación al jugador.
- Si las imágenes son diferentes, se indica al jugador que no son un par coincidente y se reduce la puntuación.
