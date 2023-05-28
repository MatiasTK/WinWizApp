import asyncio
import os
import configparser
import math

from rich.console import Console
from rich.markdown import Markdown

from pywizlight import wizlight, PilotBuilder, discovery

SALIR = 13
OPCION_SIN_ELEGIR = 0
OPCION_ENCENDER = 1
OPCION_APAGAR = 2
OPCION_CAMBIAR_BRILLO = 3
OPCION_BLANCO_CALIDO = 4
OPCION_BLANCO_FRIO = 5
OPCION_LUZ_DIA = 6
OPCION_LUZ_NOCTURNA = 7
OPCION_ACOGEDOR = 8
OPCION_CONCENTRACION = 9
OPCION_RELAX = 10
OPCION_HORA_TELE = 11
OPCION_COLOR_CUSTOM = 12

OPCION_ROJO = 1
OPCION_VERDE = 2
OPCION_AZUL = 3
OPCION_ROSA = 4
OPCION_RGB_CUSTOM = 5

LOGO = r"""
 __      __              ______
/\ \  __/\ \  __        /\  _  \
\ \ \/\ \ \ \/\_\  ____ \ \ \L\ \  _____   _____
 \ \ \ \ \ \ \/\ \/\_ ,`\\ \  __ \/\ '__`\/\ '__`\
  \ \ \_/ \_\ \ \ \/_/  /_\ \ \/\ \ \ \L\ \ \ \L\ \
   \ `\___x___/\ \_\/\____\\ \_\ \_\ \ ,__/\ \ ,__/
    '\/__//__/  \/_/\/____/ \/_/\/_/\ \ \/  \ \ \/
                                     \ \_\   \ \_\
                                      \/_/    \/_/
by @MatiasTK
"""

config = configparser.ConfigParser()

console = Console()


async def encender_luces(light):
    print("Encendiendo luces...\n")
    await light.turn_on()


async def apagar_luces(light):
    print("Apagando luces...\n")
    await light.turn_off()


async def cambiar_brillo(light):
    opcion_brillo = int(input("Elige un valor del brillo de 1 a 10: "))

    print(f"Cambiando brillo a nivel {opcion_brillo}...\n")
    await light.turn_on(PilotBuilder(brightness=math.floor(255 / 10 * opcion_brillo)))


async def color_blanco_calido(light):
    print("Poniendo color blanco calido...\n")
    await light.turn_on(PilotBuilder(warm_white=255))


async def color_blanco_frio(light):
    print("Poniendo color blanco frio...\n")
    await light.turn_on(PilotBuilder(cold_white=255))


async def color_luz_dia(light):
    print("Poniendo color luz de dia...\n")
    await light.turn_on(PilotBuilder(warm_white=255, cold_white=255))


async def luz_nocturna(light):
    print("Poniendo luz nocturna...\n")
    await light.turn_on(PilotBuilder(scene=14))


async def acogedor(light):
    print("Poniendo luz en modo acogedor...\n")
    await light.turn_on(PilotBuilder(scene=6))


async def concentracion(light):
    print("Poniendo luz en modo concentracion...\n")
    await light.turn_on(PilotBuilder(scene=15))


async def relax(light):
    print("Poniendo luz en modo relax...\n")
    await light.turn_on(PilotBuilder(scene=16))


async def hora_tele(light):
    print("Poniendo luz en modo hora de la TV...\n")
    await light.turn_on(PilotBuilder(scene=18))


def imprimir_markdown(texto):
    console.print(Markdown(texto))


async def color_custom(light):

    opcion_color = OPCION_SIN_ELEGIR

    print("Elige un color:")
    imprimir_markdown("1. Rojo")
    imprimir_markdown("2. Verde")
    imprimir_markdown("3. Azul")
    imprimir_markdown("4. Rosa")
    imprimir_markdown("5. RGB Custom")
    imprimir_markdown("6. Volver")

    opcion_color = int(input("\nOpcion: "))

    if opcion_color == OPCION_ROJO:
        print("Poniendo luz en color rojo...\n")
        await light.turn_on(PilotBuilder(rgb=(255, 0, 0)))
    elif opcion_color == OPCION_VERDE:
        print("Poniendo luz en color verde...\n")
        await light.turn_on(PilotBuilder(rgb=(0, 255, 0)))
    elif opcion_color == OPCION_AZUL:
        print("Poniendo luz en color azul...\n")
        await light.turn_on(PilotBuilder(rgb=(0, 0, 255)))
    elif opcion_color == OPCION_ROSA:
        print("Poniendo luz en color rosa...\n")
        await light.turn_on(PilotBuilder(rgb=(255, 0, 255)))
    elif opcion_color == OPCION_RGB_CUSTOM:
        rgb = input("Ingrese valores RGB(separados por ','): ")
        rojo, verde, azul = rgb.split(",")
        print("Poniendo luz en color RGB custom...\n")
        await light.turn_on(PilotBuilder(rgb=(int(rojo), int(verde), int(azul))))


async def main():
    try:
        with open("configuracion.cfg", encoding="utf-8") as f:
            config.read_file(f)
    except FileNotFoundError:
        print("No se ha encontrado el archivo de configuracion.cfg, creando uno..")

        bulbs = await discovery.discover_lights(broadcast_space="192.168.1.255")
        print("Se determino que la IP de tu lampa es: ", bulbs[0].ip)
        config["DEFAULT"] = {"ip": bulbs[0].ip}

        with open("configuracion.cfg", "w", encoding="utf-8") as f:
            config.write(f)

    ip = config["DEFAULT"]["ip"]

    light = wizlight(ip)

    opcion = OPCION_SIN_ELEGIR

    while opcion != SALIR:
        os.system("cls")

        print(LOGO)

        if opcion == OPCION_ENCENDER:
            await encender_luces(light)
        elif opcion == OPCION_APAGAR:
            await apagar_luces(light)
        elif opcion == OPCION_CAMBIAR_BRILLO:
            await cambiar_brillo(light)
        elif opcion == OPCION_BLANCO_CALIDO:
            await color_blanco_calido(light)
        elif opcion == OPCION_BLANCO_FRIO:
            await color_blanco_frio(light)
        elif opcion == OPCION_LUZ_DIA:
            await color_luz_dia(light)
        elif opcion == OPCION_LUZ_NOCTURNA:
            await luz_nocturna(light)
        elif opcion == OPCION_ACOGEDOR:
            await acogedor(light)
        elif opcion == OPCION_CONCENTRACION:
            await concentracion(light)
        elif opcion == OPCION_RELAX:
            await relax(light)
        elif opcion == OPCION_HORA_TELE:
            await hora_tele(light)
        elif opcion == OPCION_COLOR_CUSTOM:
            await color_custom(light)

        imprimir_markdown("Elige una opción:")
        imprimir_markdown("1. Encender Luces")
        imprimir_markdown("2. Apagar Luces")
        imprimir_markdown("3. Cambiar Brillo")
        imprimir_markdown("4. Color Blanco Calido")
        imprimir_markdown("5. Color Blanco Frio")
        imprimir_markdown("6. Color Luz de Dia")
        imprimir_markdown("7. Luz Nocturna")
        imprimir_markdown("8. Acogedor")
        console.print("\n [yellow]9[/yellow] Concentracion")
        imprimir_markdown("10. Relax")
        imprimir_markdown("11. Hora de la tele")
        imprimir_markdown("12. Color Custom")
        imprimir_markdown("13. SALIR")

        opcion = int(input("\nOpcion: "))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
