# Wiz App

_Un simple script hecho en python para controlar las luces [WiZ](https://www.wizconnected.com/es-ar) del hogar._

## Previsualización

![Previsualización Wiz App](https://i.imgur.com/cDaKX0U.png)

## Instalación

- Descargar la aplicación empaquetada desde las releases.

## Building

- Instalar los requisitos con el siguiente comando:

```console
pip install -r requirements.txt
```

**Nota**: Requiere una version de Python `>= 3.7`.

- Usar la version con interfaz gráfica (Tkinter) o la version de consola (CLI).

## Como usar

Simplemente ejecutar el `.exe` o `.py`, esperar a que el programa detecte la ip de la bombilla y luego usar los botones para controlar la bombilla.

## Solución de problemas

En caso de que no se pueda detectar la bombilla, se puede ingresar la ip manualmente creando un archivo `configuracion.cfg` y poniendo la dirección ip.

**Ejemplo:**

```conf
[DEFAULT]
ip = 192.168.1.1
```

**Nota:** La dirección IP la podes encontrar en los ajustes de la lampara en la aplicación de WiZ de Android
