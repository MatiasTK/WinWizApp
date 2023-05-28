""" Wiz App - Graphical Version """

import asyncio
import configparser
import math
import os
import sys

import customtkinter as tk
from async_tkinter_loop import async_handler, async_mainloop
from CTkColorPicker import AskColor
from customtkinter import CTk, CTkButton, CTkFont, CTkFrame, CTkLabel, CTkSlider
from pywizlight import PilotBuilder, discovery, wizlight

CONFIG = configparser.ConfigParser()

tk.set_appearance_mode("System")  # Modes: system (default), light, dark
tk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


@async_handler
async def update_slider(light, slider):
    """Set the default value for the slider"""
    state = await light.updateState()
    brightness = state.get_brightness()
    slider.set(math.floor(brightness / 255 * 10))


@async_handler
async def encender_luces(light):
    """Turn on the light"""
    await light.turn_on()


@async_handler
async def apagar_luces(light):
    """Turn off the light"""
    await light.turn_off()


@async_handler
async def cambiar_brillo(light, value):
    """Change the brightness of the light"""
    await light.turn_on(PilotBuilder(brightness=math.floor(255 / 10 * value)))


@async_handler
async def color_blanco_calido(light):
    """Sets the light to warm white"""
    await light.turn_on(PilotBuilder(warm_white=255))


@async_handler
async def color_blanco_frio(light):
    """Sets the light to cold white"""
    await light.turn_on(PilotBuilder(cold_white=255))


@async_handler
async def color_luz_dia(light):
    """Sets the light to white"""
    await light.turn_on(PilotBuilder(warm_white=255, cold_white=255))


@async_handler
async def luz_nocturna(light):
    """Sets the light to night light"""
    await light.turn_on(PilotBuilder(scene=14))


@async_handler
async def acogedor(light):
    """Sets the light to cozy"""
    await light.turn_on(PilotBuilder(scene=6))


@async_handler
async def concentracion(light):
    """Sets the light to focus"""
    await light.turn_on(PilotBuilder(scene=15))


@async_handler
async def colores_reales(light):
    """Sets the light to true colors"""
    await light.turn_on(PilotBuilder(scene=17))


@async_handler
async def relax(light):
    """Sets the light to relax"""
    await light.turn_on(PilotBuilder(scene=16))


@async_handler
async def hora_tele(light):
    """Sets the light to tv time"""
    await light.turn_on(PilotBuilder(scene=18))


@async_handler
async def color_rojo(light):
    """Sets the light to color red"""
    await light.turn_on(PilotBuilder(rgb=(255, 0, 0)))


@async_handler
async def color_verde(light):
    """Sets the light to color green"""
    await light.turn_on(PilotBuilder(rgb=(0, 255, 0)))


@async_handler
async def color_azul(light):
    """Sets the light to color blue"""
    await light.turn_on(PilotBuilder(rgb=(0, 0, 255)))


def hex_to_rgb(hexstr):
    """Converts a hex string to rgb tuple"""
    hexstr = hexstr.replace("#", "")
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hexstr[i : i + 2], 16)
        rgb.append(decimal)

    return tuple(rgb)


@async_handler
async def color_custom(light):
    """Sets the light to a custom color"""
    pick_color = AskColor(width=300)
    color = pick_color.get()
    red, green, blue, *_rest = hex_to_rgb(color)
    await light.turn_on(PilotBuilder(rgb=(red, green, blue)))


async def init_light():
    """Returns an initialized wizlight light"""
    try:
        with open("configuracion.cfg", encoding="utf-8") as file:
            CONFIG.read_file(file)
    except FileNotFoundError:
        print("No se ha encontrado el archivo de configuracion.cfg, creando uno..")

        bulbs = await discovery.discover_lights(broadcast_space="192.168.1.255")
        if len(bulbs) == 0:
            raise Exception(
                "No se pudo encontrar la ip de la lampara"
            ) from FileNotFoundError

        print("Se determino que la IP de tu lampara es: ", bulbs[0].ip)
        CONFIG["DEFAULT"] = {"ip": bulbs[0].ip}
        with open("configuracion.cfg", "w", encoding="utf-8") as file:
            CONFIG.write(file)

    light_ip = CONFIG["DEFAULT"]["ip"]

    return wizlight(light_ip)


class WizAppGUI:
    """Builds the UI"""

    def __init__(self, light):
        # build ui
        self.app = CTk(None)

        self.app.title("Wiz App")
        self.app.geometry("640x480")
        self.app.iconbitmap(resource_path(r"icons\monochrome_large.ico"))
        self.app.resizable(False, False)

        self.sidebar = CTkFrame(self.app)
        self.sidebar.configure(width=14)

        self.sidebar_title = CTkLabel(self.sidebar)
        self.sidebar_title.configure(
            font=CTkFont("Arial", 20, "bold", "roman", False, False), text="Wiz App"
        )
        self.sidebar_title.pack(expand="false", fill="x", padx=20, pady=20, side="top")

        self.sidebar_encender = CTkButton(self.sidebar)
        self.sidebar_encender.configure(
            text="Encender Luces", command=lambda: encender_luces(light)
        )
        self.sidebar_encender.pack(ipady=5, padx=20, pady=10, side="top")

        self.sidebar_apagar = CTkButton(self.sidebar)
        self.sidebar_apagar.configure(
            text="Apagar Luces", command=lambda: apagar_luces(light)
        )
        self.sidebar_apagar.pack(ipady=5, padx=20, pady=10, side="top")

        self.sidebar_brillo = CTkFrame(self.sidebar)
        self.sidebar_brillo.configure(fg_color="#333333")

        self.sidebar_brillo_title = CTkLabel(self.sidebar_brillo)
        self.sidebar_brillo_title.configure(text="Brillo")
        self.sidebar_brillo_title.pack(side="top")

        self.sidebar_brillo_slider = CTkSlider(self.sidebar_brillo)
        self.sidebar_brillo_slider.configure(
            from_=0,
            to=10,
            width=0,
            command=lambda value: cambiar_brillo(light, value),
        )
        update_slider(light, self.sidebar_brillo_slider)
        self.sidebar_brillo_slider.pack(fill="x", side="top")

        self.sidebar_brillo_creditos = CTkLabel(self.sidebar_brillo)
        self.sidebar_brillo_creditos.configure(
            font=CTkFont("Arial", 14, None, "italic", False, False),
            text="Creado por @MatiasTK",
        )
        self.sidebar_brillo_creditos.pack(anchor="s", pady=10, side="bottom")

        self.sidebar_brillo.pack(fill="x", side="bottom")

        self.sidebar_ip = CTkLabel(self.sidebar)
        self.sidebar_ip.configure(
            text=f"IP: {light.ip}",
            font=CTkFont("Arial", 13, "bold"),
        )
        self.sidebar_ip.pack(pady=10, side="bottom")

        self.sidebar.pack(fill="y", side="left")

        self.blancos = CTkLabel(self.app)
        self.blancos.configure(
            font=CTkFont("Arial", 15, "bold", "roman", False, False), text="Blancos"
        )
        self.blancos.pack(expand="true", side="top")

        self.blancos_opciones = CTkFrame(self.app)
        self.blancos_opciones.configure(fg_color="#2b2b2b", height=50)

        self.blancos_calido = CTkButton(self.blancos_opciones)
        self.blancos_calido.configure(
            text="Blanco calido", command=lambda: color_blanco_calido(light)
        )
        self.blancos_calido.pack(expand="true", ipady=5, side="left")

        self.blancos_neutro = CTkButton(self.blancos_opciones)
        self.blancos_neutro.configure(
            text="Blanco Neutro", command=lambda: color_luz_dia(light)
        )
        self.blancos_neutro.pack(expand="true", ipady=5, side="left")

        self.blancos_frio = CTkButton(self.blancos_opciones)
        self.blancos_frio.configure(
            text="Blanco Frio", command=lambda: color_blanco_frio(light)
        )
        self.blancos_frio.pack(expand="true", ipady=5, side="right")

        self.blancos_opciones.pack(expand="true", fill="x", padx=10, side="top")

        self.funcionales = CTkLabel(self.app)
        self.funcionales.configure(
            font=CTkFont("Arial", 15, "bold", "roman", False, False), text="Funcionales"
        )
        self.funcionales.pack(anchor="center", expand="true", padx=20, side="top")

        self.funcionales_opciones_top = CTkFrame(self.app)
        self.funcionales_opciones_top.configure(fg_color="#2b2b2b", height=50)

        self.funcionales_nocturna = CTkButton(self.funcionales_opciones_top)
        self.funcionales_nocturna.configure(
            text="Luz Nocturna", command=lambda: luz_nocturna(light)
        )
        self.funcionales_nocturna.pack(expand="true", ipady=5, side="left")

        self.funcionales_acogedor = CTkButton(self.funcionales_opciones_top)
        self.funcionales_acogedor.configure(
            text="Acogedor", command=lambda: acogedor(light)
        )
        self.funcionales_acogedor.pack(expand="true", ipady=5, side="left")

        self.funcionales_concentracion = CTkButton(self.funcionales_opciones_top)
        self.funcionales_concentracion.configure(
            text="Concentracion", command=lambda: concentracion(light)
        )
        self.funcionales_concentracion.pack(expand="true", ipady=5, side="right")

        self.funcionales_opciones_top.pack(expand="true", fill="x", padx=10, side="top")

        self.funcionales_opciones_bot = CTkFrame(self.app)
        self.funcionales_opciones_bot.configure(fg_color="#2b2b2b", height=50)

        self.funcionales_relax = CTkButton(self.funcionales_opciones_bot)
        self.funcionales_relax.configure(text="Relax", command=lambda: relax(light))
        self.funcionales_relax.pack(expand="true", ipady=5, side="left")

        self.funcionales_television = CTkButton(self.funcionales_opciones_bot)
        self.funcionales_television.configure(
            text="Hora de la television", command=lambda: hora_tele(light)
        )
        self.funcionales_television.pack(expand="true", ipady=5, side="left")

        self.funcionales_reales = CTkButton(self.funcionales_opciones_bot)
        self.funcionales_reales.configure(
            text="Colores Reales", command=lambda: colores_reales(light)
        )
        self.funcionales_reales.pack(expand="true", ipady=5, side="right")

        self.funcionales_opciones_bot.pack(expand="true", fill="x", padx=10, side="top")

        self.colores = CTkLabel(self.app)
        self.colores.configure(
            font=CTkFont("Arial", 15, "bold", "roman", False, False), text="Colores"
        )
        self.colores.pack(anchor="center", expand="true", padx=20, side="top")

        self.colores_opciones = CTkFrame(self.app)
        self.colores_opciones.configure(fg_color="#2b2b2b", height=50)

        self.colores_rojo = CTkButton(self.colores_opciones)
        self.colores_rojo.configure(text="Rojo", command=lambda: color_rojo(light))
        self.colores_rojo.pack(expand="true", fill="y", side="left")

        self.colores_azul = CTkButton(self.colores_opciones)
        self.colores_azul.configure(text="Azul", command=lambda: color_azul(light))
        self.colores_azul.pack(expand="true", ipady=5, side="left")

        self.colores_verde = CTkButton(self.colores_opciones)
        self.colores_verde.configure(text="Verde", command=lambda: color_verde(light))
        self.colores_verde.pack(expand="true", ipady=5, side="right")

        self.colores_opciones.pack(expand="true", fill="x", padx=10, side="top")

        self.colores_opcion_custom = CTkButton(self.app)
        self.colores_opcion_custom.configure(
            text="Custom", command=lambda: color_custom(light)
        )
        self.colores_opcion_custom.pack(
            expand="true", fill="x", ipady=5, padx=10, side="top"
        )

        # Main widget
        self.mainwindow = self.app

    def run(self):
        """Runs the UI in an async loop"""
        async_mainloop(self.app)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    light = loop.run_until_complete(init_light())

    app = WizAppGUI(light)
    app.run()
