import json
import random
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

#Leer el token desde archivo .txt
def leer_token(ruta_archivo: str) -> str:
    with open(ruta_archivo, 'r') as archivo:
        token = archivo.readline().strip()
    return token


# Define el tablero
tablero = ['La Goleta', 'Comunidad','Churripena','Inviertes en Student Coin','Urbano','Feria de la Viñuela', 'Silbato de Luismi','Suerte','Gafas de Juanki', 'El bigote de Jesús', 'Cárcel:Solo visitas', 'Ballesta de Guille', 'Vermont Avenue', 'Connecticut Avenue']

# Lee la lista de propiedades desde un archivo JSON
with open('propiedades.json') as f:
    propiedades = json.load(f)

# Define el comando para imprimir las propiedades
@bot.command()
async def lista_propiedades(ctx):
    for propiedad, atributos in propiedades.items():
        mensaje = f"{propiedad}: precio={atributos['precio']}, alquiler={atributos['alquiler']}, apartamentos={atributos['apartamentos']}, hoteles={atributos['hoteles']}, hipoteca={atributos['hipoteca']}"
        await ctx.send(mensaje)


# Define la clase jugador
class Jugador:
    def __init__(self, nombre, dinero, posicion,vidas):
        self.nombre = nombre
        self.dinero = dinero
        self.posicion = posicion
        self.vidas = vidas

#Estado partida

partida_en_curso = False

# Define la lista de jugadores
jugadores = []

# Agrega los jugadores
def incluir_usuario(usuario, lista):
    if usuario not in lista:
        jugadores.append(Jugador(usuario.name, 1500, 0,0))
        return True
    else:
        return False

@bot.command()
async def registro(ctx): #Registro de jugadores
    global partida_en_curso

    if partida_en_curso:
        await ctx.send('La partida ya ha comenzado')
    else:
        if len(jugadores) < 6:
            usuario = ctx.author
            if incluir_usuario(usuario, jugadores):
                await ctx.send(f'{usuario.name} ha sido registrado en la lista.')
            else:
                await ctx.send(f'{usuario.name} ya estaba en la lista.')
        else:
            await ctx.send('Partida completa. Número de jugadores máximos alcanzado.')

@bot.command()
async def lista(ctx):
    mensaje = 'Los jugadores son:\n'
    for jugador in jugadores:
        mensaje += f'- {jugador.nombre}\n'
    await ctx.send(mensaje)

@bot.command()
async def comenzar_partida(ctx):
    global partida_en_curso

    # Verificar si ya hay una partida en curso
    if partida_en_curso:
        # La partida ya ha comenzado
        if ctx.author in usuarios:
            await ctx.send(f'{ctx.author.name}, la partida ya ha comenzado.')
    else:
        # Verificar si hay suficientes jugadores para comenzar la partida
        if len(jugadores) < 1:
            await ctx.send('No hay suficientes jugadores para comenzar la partida.')
        else:
            # Barajar aleatoriamente la lista de jugadores
            random.shuffle(jugadores)

            # Comenzar una nueva partida
            partida_en_curso = True
            mensaje = '¡La partida ha comenzado!\n\n'
            mensaje += 'El orden de turno de los jugadores es:\n'
            for i, usuario in enumerate(jugadores):
                mensaje += f'{i+1}. {usuario.nombre}\n'
            await ctx.send(mensaje)



# Define el comando para mover a un jugador
@bot.command()
async def mover(ctx, jugador, casillas):
    jugador = next((x for x in jugadores if x.nombre == jugador), None)
    if jugador is None:
        await ctx.send('Jugador no encontrado')
        return
    jugador.posicion += int(casillas) % len(tablero)
    await ctx.send(f'{jugador.nombre} se ha movido a {tablero[jugador.posicion]}')
    propiedad_actual = tablero[jugador.posicion]
    if propiedad_actual in propiedades:
        propiedad = propiedades[propiedad_actual]
        if propiedad['precio'] <= jugador.dinero:
            await ctx.send(f'{jugador.nombre} ha comprado {propiedad_actual}')
            jugador.dinero -= propiedad['precio']
        else:
            await ctx.send(f'{jugador.nombre} no tiene suficiente dinero para comprar {propiedad_actual}')

token = leer_token('token.txt')
bot.run(token)

