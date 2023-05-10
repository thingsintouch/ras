# Cómo crear una nueva rama en Git, desarrollar una nueva característica, probarla e integrar los cambios en la rama principal

Aquí están los pasos para crear una nueva rama, desarrollar una nueva característica, probarla e integrar los cambios en la rama principal, utilizando comandos de línea de comando en Bash:

1. Abre una ventana de terminal y navega hasta el directorio raíz de tu repositorio de Git.

2. Verifica la rama principal ejecutando el siguiente comando:
    ```
    git checkout main
    ```

3. Crea una nueva rama para trabajar en la nueva característica ejecutando el siguiente comando:
    ```
    git branch nueva-caracteristica
    ```

4. Cambia a la nueva rama ejecutando el siguiente comando:
    ```
    git checkout nueva-caracteristica
    ```

5. Desarrolla la nueva característica escribiendo código, haciendo cambios y confirmando tu trabajo como lo harías normalmente.

6. Prueba la nueva característica para asegurarte de que funciona correctamente.

7. Cuando estés listo para integrar la nueva característica en la rama principal, cambia de vuelta a la rama principal ejecutando el siguiente comando:
    ```
    git checkout main
    ```

8. Fusiona los cambios de la rama nueva-caracteristica en la rama principal ejecutando el siguiente comando:
    ```
    git merge nueva-caracteristica
    ```

9. Resuelve cualquier conflicto que surja durante el proceso de fusión, si es necesario.

10. Prueba la rama principal con la nueva característica para asegurarte de que todo funciona correctamente.

11. Si todo parece estar bien, empuja los cambios a la rama principal ejecutando el siguiente comando:
    ```
    git push origin main
    ```

¡Y eso es todo! Has creado con éxito una nueva rama, desarrollado una nueva característica en ella, la has probado y has integrado los cambios en la rama principal.