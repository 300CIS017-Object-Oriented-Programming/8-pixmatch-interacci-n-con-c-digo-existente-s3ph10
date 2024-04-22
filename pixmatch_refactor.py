import streamlit as st
import os
import time as tm
import random
import base64
import json
from PIL import Image
from streamlit_autorefresh import st_autorefresh

# Configuración de la página Streamlit
st.set_page_config(
    page_title="PixMatch",  # Título de la página
    page_icon="🕹️",  # Icono de la página
    layout="wide",  # Diseño de la página
    initial_sidebar_state="expanded"  # Estado inicial de la barra lateral
)

# Determinación de la ruta base del archivo
vDrive = os.path.splitdrive(os.getcwd())[0]
if vDrive == "C:":
    vpth = "./"  # Disco local del desarrollador
else:
    vpth = "./"

# Definición de estilos HTML para usar en la aplicación
sbe = """<span style='font-size: 140px;
                      border-radius: 7px;
                      text-align: center;
                      display:inline;
                      padding-top: 3px;
                      padding-bottom: 3px;
                      padding-left: 0.4em;
                      padding-right: 0.4em;
                      '>
                      |fill_variable|
                      </span>"""

pressed_emoji = """<span style='font-size: 24px;
                                border-radius: 7px;
                                text-align: center;
                                display:inline;
                                padding-top: 3px;
                                padding-bottom: 3px;
                                padding-left: 0.2em;
                                padding-right: 0.2em;
                                '>
                                |fill_variable|
                                </span>"""

horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'><br>"  # Línea divisoria delgada
purple_btn_colour = """
                        <style>
                            div.stButton > button:first-child {background-color: #4b0082; color:#ffffff;}
                            div.stButton > button:hover {background-color: RGB(0,112,192); color:#ffffff;}
                            div.stButton > button:focus {background-color: RGB(47,117,181); color:#ffffff;}
                        </style>
                    """

# Inicialización de variables de estado de la sesión
mystate = st.session_state
if "expired_cells" not in mystate: mystate.expired_cells = []  # Celdas expiradas
if "myscore" not in mystate: mystate.myscore = 0  # Puntuación del jugador
if "plyrbtns" not in mystate: mystate.plyrbtns = {}  # Botones del jugador
if "sidebar_emoji" not in mystate: mystate.sidebar_emoji = ''  # Emoji en la barra lateral
if "emoji_bank" not in mystate: mystate.emoji_bank = []  # Banco de emojis
if "GameDetails" not in mystate: mystate.GameDetails = ['Medium', 6, 7, '']  # Detalles del juego: nivel de dificultad, intervalo de generación, celdas totales por fila o columna, nombre del jugador

#//////////////////////////////////////documentado

# common functions
def ReduceGapFromPageTop(wch_section='main page'):
    """
    ReduceGapFromPageTop(wch_section='main page')

    Ajusta el espacio en blanco en la parte superior de la página Streamlit según la sección especificada.

    Parámetros:
    - wch_section (str, opcional): Determina la sección de la página donde se ajustará el espacio en blanco.
                                    Puede ser 'main page', 'sidebar' o 'all'. Por defecto es 'main page'.

    Detalles:
    - Si wch_section es 'main page', se agrega un espacio en blanco en la parte superior del contenedor principal.
    - Si wch_section es 'sidebar', se ajusta el espacio en blanco en la parte superior del contenedor de la barra lateral.
    - Si wch_section es 'all', se ajusta el espacio en blanco en ambas secciones de la página.

    Ejemplos:
    >>> ReduceGapFromPageTop('main page')  # Ajusta el espacio en blanco en la parte superior del contenedor principal.
    >>> ReduceGapFromPageTop('sidebar')    # Ajusta el espacio en blanco en la parte superior del contenedor de la barra lateral.
    >>> ReduceGapFromPageTop('all')        # Ajusta el espacio en blanco en ambas secciones de la página.
    """
    if wch_section == 'main page':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)
    elif wch_section == 'sidebar':
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)
    elif wch_section == 'all':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)


def Leaderboard(what_to_do):
    """
    Leaderboard(what_to_do)

    Realiza operaciones en el archivo del tablero de clasificación según la acción especificada.

    Parámetros:
    - what_to_do (str): La acción que se debe realizar en el tablero de clasificación. Puede ser 'create', 'write' o 'read'.

    Detalles:
    - Si what_to_do es 'create', crea un archivo de tablero de clasificación vacío si no existe.
    - Si what_to_do es 'write', escribe la puntuación más alta del jugador en el archivo de tablero de clasificación.
    - Si what_to_do es 'read', lee el archivo de tablero de clasificación y muestra las puntuaciones más altas en la interfaz.

    """
    if what_to_do == 'create':
        # Crear un archivo de tablero de clasificación si no existe y el nombre del jugador está proporcionado
        if mystate.GameDetails[3] != '':
            if not os.path.isfile(vpth + 'leaderboard.json'):
                tmpdict = {}
                json.dump(tmpdict, open(vpth + 'leaderboard.json', 'w'))  # write file

    elif what_to_do == 'write':
        # Escribir la puntuación más alta del jugador en el archivo de tablero de clasificación si el nombre del jugador está proporcionado
        if mystate.GameDetails[3] != '':
            if os.path.isfile(vpth + 'leaderboard.json'):
                leaderboard = json.load(open(vpth + 'leaderboard.json'))  # read file
                leaderboard_dict_lngth = len(leaderboard)

                leaderboard[str(leaderboard_dict_lngth + 1)] = {'NameCountry': mystate.GameDetails[3],
                                                                'HighestScore': mystate.myscore}
                leaderboard = dict(
                    sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # sort desc

                if len(leaderboard) > 3:
                    for i in range(len(leaderboard) - 3): leaderboard.popitem()  # rmv last kdict ey

                json.dump(leaderboard, open(vpth + 'leaderboard.json', 'w'))  # write file

    elif what_to_do == 'read':
        # Leer el archivo de tablero de clasificación y mostrar las puntuaciones más altas en la interfaz
        if mystate.GameDetails[3] != '':
            if os.path.isfile(vpth + 'leaderboard.json'):
                leaderboard = json.load(open(vpth + 'leaderboard.json'))  # read file

                leaderboard = dict(
                    sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # sort desc

                sc0, sc1, sc2, sc3 = st.columns((2, 3, 3, 3))
                rknt = 0
                for vkey in leaderboard.keys():
                    if leaderboard[vkey]['NameCountry'] != '':
                        rknt += 1
                        if rknt == 1:
                            sc0.write('🏆 Past Winners:')
                            sc1.write(
                                f"🥇 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 2:
                            sc2.write(
                                f"🥈 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 3:
                            sc3.write(
                                f"🥈 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")




def InitialPage():
    """
    Configura y muestra la página inicial del juego.

    La página inicial incluye instrucciones y reglas del juego, así como una imagen de ayuda.

    """
    with st.sidebar:
        # Configuración de la barra lateral
        st.subheader("🖼️ Pix Match:")  # Título del juego en la barra lateral
        st.markdown(horizontal_bar, True)  # Línea horizontal para separar visualmente

        # Carga y muestra la imagen de la barra lateral
        sidebarlogo = Image.open('sidebarlogo.jpg').resize((300, 390))
        st.image(sidebarlogo, use_column_width='auto')

    # Sección principal de la página
    # Instrucciones y reglas del juego
    hlp_dtl = f"""<span style="font-size: 26px;">
        <ol>
            <li style="font-size:15px";>Game play opens with (a) a sidebar picture and (b) a N x N grid of picture buttons, where N=6:Easy, N=7:Medium, N=8:Hard.</li>
            <li style="font-size:15px";>You need to match the sidebar picture with a grid picture button, by pressing the (matching) button (as quickly as possible).</li>
            <li style="font-size:15px";>Each correct picture match will earn you <strong>+N</strong> points (where N=5:Easy, N=3:Medium, N=1:Hard); each incorrect picture match will earn you <strong>-1</strong> point.</li>
            <li style="font-size:15px";>The sidebar picture and the grid pictures will dynamically regenerate after a fixed seconds interval (Easy=8, Medium=6, Hard=5). Each regeneration will have a penalty of <strong>-1</strong> point</li>
            <li style="font-size:15px";>Each of the grid buttons can only be pressed once during the entire game.</li>
            <li style="font-size:15px";>The game completes when all the grid buttons are pressed.</li>
            <li style="font-size:15px";>At the end of the game, if you have a positive score, you will have <strong>won</strong>; otherwise, you will have <strong>lost</strong>.</li>
        </ol>
        </span>"""

    # Divide la pantalla principal en dos columnas
    sc1, sc2 = st.columns(2)

    # Selecciona aleatoriamente una imagen de ayuda
    random.seed()
    GameHelpImg = vpth + random.choice(["MainImg1.jpg", "MainImg2.jpg", "MainImg3.jpg", "MainImg4.jpg"])
    GameHelpImg = Image.open(GameHelpImg).resize((550, 550))

    # Muestra la imagen de ayuda en la segunda columna
    sc2.image(GameHelpImg, use_column_width='auto')

    # Muestra las instrucciones y reglas del juego en la primera columna
    sc1.subheader('Rules | Playing Instructions:')
    sc1.markdown(horizontal_bar, True)
    sc1.markdown(hlp_dtl, unsafe_allow_html=True)

    # Línea horizontal en la parte inferior de la pantalla
    st.markdown(horizontal_bar, True)

    # Información del autor y contacto
    author_dtl = "<strong>Happy Playing: 😎 Shawn Pereira: shawnpereira1969@gmail.com</strong>"
    st.markdown(author_dtl, unsafe_allow_html=True)


def ReadPictureFile(wch_fl):
    """
    Lee un archivo de imagen y lo codifica en base64 para su visualización en Streamlit.

    Parameters:
        wch_fl (str): La ruta del archivo de imagen.

    Returns:
        str: La representación de la imagen en base64.

    """
    try:
        # Construye la ruta completa del archivo de imagen
        pxfl = f"{vpth}{wch_fl}"

        # Lee el archivo de imagen en modo binario ('rb'), lo convierte a base64 y lo decodifica
        image_base64 = base64.b64encode(open(pxfl, 'rb').read()).decode()

        # Devuelve la representación en base64 de la imagen
        return image_base64

    except:
        # En caso de error (por ejemplo, si el archivo no existe o no se puede leer), devuelve una cadena vacía
        return ""


def PressedCheck(vcell):
    """
    Verifica si se ha presionado un botón de la celda especificada y actualiza el estado del juego en consecuencia.

    Parameters:
        vcell (int): El índice de la celda del botón presionado.

    Returns:
        None

    """
    # Verifica si el botón de la celda ya ha sido presionado
    if mystate.plyrbtns[vcell]['isPressed'] == False:
        # Marca el botón como presionado y agrega la celda a las celdas expiradas
        mystate.plyrbtns[vcell]['isPressed'] = True
        mystate.expired_cells.append(vcell)

        # Comprueba si el emoji del botón coincide con el emoji de la barra lateral
        if mystate.plyrbtns[vcell]['eMoji'] == mystate.sidebar_emoji:
            # Si coinciden, marca la respuesta como verdadera, suma puntos al puntaje del jugador
            # y otorga puntos adicionales según la dificultad del juego
            mystate.plyrbtns[vcell]['isTrueFalse'] = True
            mystate.myscore += 5

            if mystate.GameDetails[0] == 'Easy':
                mystate.myscore += 5
            elif mystate.GameDetails[0] == 'Medium':
                mystate.myscore += 3
            elif mystate.GameDetails[0] == 'Hard':
                mystate.myscore += 1

        else:
            # Si no coinciden, marca la respuesta como falsa y resta un punto al puntaje del jugador
            mystate.plyrbtns[vcell]['isTrueFalse'] = False
            mystate.myscore -= 1


def ResetBoard():
    """
    Restablece el tablero del juego asignando nuevos emojis a los botones de las celdas y seleccionando un nuevo emoji para la barra lateral.

    Parameters:
        None

    Returns:
        None

    """
    total_cells_per_row_or_col = mystate.GameDetails[2]

    # Selecciona un emoji aleatorio para la barra lateral
    sidebar_emoji_no = random.randint(1, len(mystate.emoji_bank)) - 1
    mystate.sidebar_emoji = mystate.emoji_bank[sidebar_emoji_no]

    # Verifica si el emoji de la barra lateral está presente en algún botón de celda
    sidebar_emoji_in_list = False
    for vcell in range(1, ((total_cells_per_row_or_col ** 2) + 1)):
        rndm_no = random.randint(1, len(mystate.emoji_bank)) - 1
        if mystate.plyrbtns[vcell]['isPressed'] == False:
            vemoji = mystate.emoji_bank[rndm_no]
            mystate.plyrbtns[vcell]['eMoji'] = vemoji
            if vemoji == mystate.sidebar_emoji:
                sidebar_emoji_in_list = True

    # Si el emoji de la barra lateral no está en ningún botón, agréguelo aleatoriamente
    if sidebar_emoji_in_list == False:
        tlst = [x for x in range(1, ((total_cells_per_row_or_col ** 2) + 1))]
        flst = [x for x in tlst if x not in mystate.expired_cells]
        if len(flst) > 0:
            lptr = random.randint(0, (len(flst) - 1))
            lptr = flst[lptr]
            mystate.plyrbtns[lptr]['eMoji'] = mystate.sidebar_emoji



def PreNewGame():
    """
    Prepara el juego para una nueva partida, inicializando valores y emojis según la dificultad del juego.

    Parameters:
        None

    Returns:
        None

    """
    total_cells_per_row_or_col = mystate.GameDetails[2]
    mystate.expired_cells = []
    mystate.myscore = 0

    # Definición de grupos de emojis según la dificultad del juego
    foxes = ['😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
    emojis = ['😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛',
              '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩',
              '🥺', '😢', '😠', '😳', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😧', '😮', '😲', '🥱',
              '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤒']
    humans = ['👶', '👧', '🧒', '👦', '👩', '🧑', '👨', '👩‍🦱', '👨‍🦱', '👩‍🦰', '‍👨', '👱', '👩', '👱', '👩‍', '👨‍🦳', '👩‍🦲', '👵', '🧓',
              '👴', '👲', '👳']
    foods = ['🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅', '🍆', '🥑', '🥦', '🥬',
             '🥒', '🌽', '🥕', '🧄', '🧅', '🥔', '🍠', '🥐', '🥯', '🍞', '🥖', '🥨', '🧀', '🥚', '🍳', '🧈', '🥞', '🧇', '🥓', '🥩', '🍗',
             '🍖', '🦴', '🌭', '🍔', '🍟', '🍕']
    clocks = ['🕓', '🕒', '🕑', '🕘', '🕛', '🕚', '🕖', '🕙', '🕔', '🕤', '🕠', '🕕', '🕣', '🕞', '🕟', '🕜', '🕢', '🕦']
    hands = ['🤚', '🖐', '✋', '🖖', '👌', '🤏', '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '🖕', '👇', '☝️', '👍', '👎', '✊', '👊',
             '🤛', '🤜', '👏', '🙌', '🤲', '🤝', '🤚🏻', '🖐🏻', '✋🏻', '🖖🏻', '👌🏻', '🤏🏻', '✌🏻', '🤞🏻', '🤟🏻', '🤘🏻', '🤙🏻', '👈🏻',
             '👉🏻', '👆🏻', '🖕🏻', '👇🏻', '☝🏻', '👍🏻', '👎🏻', '✊🏻', '👊🏻', '🤛🏻', '🤜🏻', '👏🏻', '🙌🏻', '🤚🏽', '🖐🏽', '✋🏽', '🖖🏽',
             '👌🏽', '🤏🏽', '✌🏽', '🤞🏽', '🤟🏽', '🤘🏽', '🤙🏽', '👈🏽', '👉🏽', '👆🏽', '🖕🏽', '👇🏽', '☝🏽', '👍🏽', '👎🏽', '✊🏽', '👊🏽',
             '🤛🏽', '🤜🏽', '👏🏽', '🙌🏽']
    animals = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐽', '🐸', '🐵', '🙈', '🙉', '🙊', '🐒', '🐔',
               '🐧', '🐦', '🐤', '🐣', '🐥', '🦆', '🦅', '🦉', '🦇', '🐺', '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦟', '🦗',
               '🦂', '🐢', '🐍', '🦎', '🦖', '🦕', '🐙', '🦑', '🦐', '🦞', '🦀', '🐡', '🐠', '🐟', '🐬', '🐳', '🐋', '🦈', '🐊', '🐅', '🐆',
               '🦓', '🦍', '🦧', '🐘', '🦛', '🦏', '🐪', '🐫', '🦒', '🦘', '🐃', '🐂', '🐄', '🐎', '🐖', '🐏', '🐑', '🦙', '🐐', '🦌', '🐕',
               '🐩', '🦮', '🐕‍🦺', '🐈', '🐓', '🦃', '🦚', '🦜', '🦢', '🦩', '🐇', '🦝', '🦨', '🦦', '🦥', '🐁', '🐀', '🦔']
    vehicles = ['🚗', '🚕', '🚙', '🚌', '🚎', '🚓', '🚑', '🚒', '🚐', '🚚', '🚛', '🚜', '🦯', '🦽', '🦼', '🛴', '🚲', '🛵', '🛺', '🚔', '🚍',
                '🚘', '🚖', '🚡', '🚠', '🚟', '🚃', '🚋', '🚞', '🚝', '🚄', '🚅', '🚈', '🚂', '🚆', '🚇', '🚊', '🚉', '✈️', '🛫', '🛬',
                '💺', '🚀', '🛸', '🚁', '🛶', '⛵️', '🚤', '🛳', '⛴', '🚢']
    houses = ['🏠', '🏡', '🏘', '🏚', '🏗', '🏭', '🏢', '🏬', '🏣', '🏤', '🏥', '🏦', '🏨', '🏪', '🏫', '🏩', '💒', '🏛', '⛪️', '🕌', '🕍',
              '🛕']
    purple_signs = ['☮️', '✝️', '☪️', '☸️', '✡️', '🔯', '🕎', '☯️', '☦️', '🛐', '⛎', '♈️', '♉️', '♊️', '♋️', '♌️', '♍️',
                    '♎️', '♏️', '♐️', '♑️', '♒️', '♓️', '🆔', '🈳']
    red_signs = ['🈶', '🈚️', '🈸', '🈺', '🈷️', '✴️', '🉐', '㊙️', '㊗️', '🈴', '🈵', '🈹', '🈲', '🅰️', '🅱️', '🆎', '🆑', '🅾️', '🆘',
                 '🚼', '🛑', '⛔️', '📛', '🚫', '🚷', '🚯', '🚳', '🚱', '🔞', '📵', '🚭']
    blue_signs = ['🚾', '♿️', '🅿️', '🈂️', '🛂', '🛃', '🛄', '🛅', '🚹', '🚺', '🚻', '🚮', '🎦', '📶', '🈁', '🔣', '🔤', '🔡', '🔠', '🆖',
                  '🆗', '🆙', '🆒', '🆕', '🆓', '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟',
                  '🔢', '⏏️', '▶️', '⏸', '⏯', '⏹', '⏺', '⏭', '⏮', '⏩', '⏪', '⏫', '⏬', '◀️', '🔼', '🔽', '➡️', '⬅️', '⬆️',
                  '⬇️', '↗️', '↘️', '↙️', '↖️', '↪️', '↩️', '⤴️', '⤵️', '🔀', '🔁', '🔂', '🔄', '🔃', '➿', '🔚', '🔙', '🔛',
                  '🔝', '🔜']
    moon = ['🌕', '🌔', '🌓', '🌗', '🌒', '🌖', '🌑', '🌜', '🌛', '🌙']

    random.seed()
    # Selección de emojis según la dificultad
    if mystate.GameDetails[0] == 'Easy':
        wch_bank = random.choice(['foods', 'moon', 'animals'])
        mystate.emoji_bank = locals()[wch_bank]

    elif mystate.GameDetails[0] == 'Medium':
        wch_bank = random.choice(
            ['foxes', 'emojis', 'humans', 'vehicles', 'houses', 'hands', 'purple_signs', 'red_signs', 'blue_signs'])
        mystate.emoji_bank = locals()[wch_bank]

    elif mystate.GameDetails[0] == 'Hard':
        wch_bank = random.choice(
            ['foxes', 'emojis', 'humans', 'foods', 'clocks', 'hands', 'animals', 'vehicles', 'houses', 'purple_signs',
             'red_signs', 'blue_signs', 'moon'])
        mystate.emoji_bank = locals()[wch_bank]

    mystate.plyrbtns = {}
    # Inicialización de botones del juego
    for vcell in range(1, ((total_cells_per_row_or_col ** 2) + 1)):
        mystate.plyrbtns[vcell] = {'isPressed': False, 'isTrueFalse': False, 'eMoji': ''}



def ScoreEmoji():
    """
    Assigns an emoji based on the player's score.

    Returns:
        str: Emoji representing the player's score.
    """
    # Casos para puntajes negativos
    if mystate.myscore == 0:
        return '😐'  # Puntaje neutro
    elif -5 <= mystate.myscore <= -1:
        return '😏'  # Puntaje negativo leve
    elif -10 <= mystate.myscore <= -6:
        return '☹️'  # Puntaje negativo moderado
    elif mystate.myscore <= -11:
        return '😖'  # Puntaje negativo grave
    # Casos para puntajes positivos
    elif 1 <= mystate.myscore <= 5:
        return '🙂'  # Puntaje positivo leve
    elif 6 <= mystate.myscore <= 10:
        return '😊'  # Puntaje positivo moderado
    elif mystate.myscore > 10:
        return '😁'  # Puntaje positivo alto


def NewGame():
    # Reiniciar el tablero
    ResetBoard()

    # Obtener el número total de celdas por fila o columna
    total_cells_per_row_or_col = mystate.GameDetails[2]

    # Reducir el espacio desde la parte superior de la página (sidebar)
    ReduceGapFromPageTop('sidebar')

    # Configuración de la barra lateral
    with st.sidebar:
        # Mostrar el título del juego en la barra lateral
        st.subheader(f"🖼️ Pix Match: {mystate.GameDetails[0]}")
        st.markdown(horizontal_bar, True)

        # Mostrar emoji en la barra lateral
        st.markdown(sbe.replace('|fill_variable|', mystate.sidebar_emoji), True)

        # Configurar temporizador automático de actualización
        aftimer = st_autorefresh(interval=(mystate.GameDetails[1] * 1000), key="aftmr")
        if aftimer > 0:
            mystate.myscore -= 1

        # Mostrar información sobre el puntaje y celdas pendientes en la barra lateral
        st.info(
            f"{ScoreEmoji()} Score: {mystate.myscore} | Pending: {(total_cells_per_row_or_col ** 2) - len(mystate.expired_cells)}")

        st.markdown(horizontal_bar, True)

        # Botón para regresar a la página principal
        if st.button(f"🔙 Return to Main Page", use_container_width=True):
            mystate.runpage = Main
            st.rerun()

    # Leer la tabla de clasificación
    Leaderboard('read')

    # Mostrar encabezado para las posiciones de las imágenes
    st.subheader("Picture Positions:")
    st.markdown(horizontal_bar, True)

    # Establecer valores predeterminados del tablero
    st.markdown("<style> div[class^='css-1vbkxwb'] > p { font-size: 1.5rem; } </style> ",
                unsafe_allow_html=True)  # hacer que la cara del botón sea grande

    # Crear columnas para el tablero de imágenes
    for i in range(1, (total_cells_per_row_or_col + 1)):
        tlst = ([1] * total_cells_per_row_or_col) + [2]  # 2 = padding del lado derecho
        globals()['cols' + str(i)] = st.columns(tlst)

    # Recorrer cada celda del tablero
    for vcell in range(1, (total_cells_per_row_or_col ** 2) + 1):
        # Determinar la referencia de la columna y el desplazamiento
        if 1 <= vcell <= (total_cells_per_row_or_col * 1):
            arr_ref = '1'
            mval = 0
        elif ((total_cells_per_row_or_col * 1) + 1) <= vcell <= (total_cells_per_row_or_col * 2):
            arr_ref = '2'
            mval = (total_cells_per_row_or_col * 1)
        elif ((total_cells_per_row_or_col * 2) + 1) <= vcell <= (total_cells_per_row_or_col * 3):
            arr_ref = '3'
            mval = (total_cells_per_row_or_col * 2)
        # Resto de los bloques elif para los otros rangos de celdas... no te saltes cosas porfa
        elif ((total_cells_per_row_or_col * 3) + 1) <= vcell <= (total_cells_per_row_or_col * 4):
            arr_ref = '4'
            mval = (total_cells_per_row_or_col * 3)
        elif ((total_cells_per_row_or_col * 4) + 1) <= vcell <= (total_cells_per_row_or_col * 5):
            arr_ref = '5'
            mval = (total_cells_per_row_or_col * 4)
        elif ((total_cells_per_row_or_col * 5) + 1) <= vcell <= (total_cells_per_row_or_col * 6):
            arr_ref = '6'
            mval = (total_cells_per_row_or_col * 5)
        elif ((total_cells_per_row_or_col * 6) + 1) <= vcell <= (total_cells_per_row_or_col * 7):
            arr_ref = '7'
            mval = (total_cells_per_row_or_col * 6)
        elif ((total_cells_per_row_or_col * 7) + 1) <= vcell <= (total_cells_per_row_or_col * 8):
            arr_ref = '8'
            mval = (total_cells_per_row_or_col * 7)
        elif ((total_cells_per_row_or_col * 8) + 1) <= vcell <= (total_cells_per_row_or_col * 9):
            arr_ref = '9'
            mval = (total_cells_per_row_or_col * 8)
        elif ((total_cells_per_row_or_col * 9) + 1) <= vcell <= (total_cells_per_row_or_col * 10):
            arr_ref = '10'
            mval = (total_cells_per_row_or_col * 9)

        # Limpiar la celda actual del tablero
        globals()['cols' + arr_ref][vcell - mval] = globals()['cols' + arr_ref][vcell - mval].empty()

        # Verificar si la celda ha sido presionada por el jugador
        if mystate.plyrbtns[vcell]['isPressed'] == True:
            # Mostrar emoji correspondiente en la celda según si la respuesta es verdadera o falsa
            if mystate.plyrbtns[vcell]['isTrueFalse'] == True:
                globals()['cols' + arr_ref][vcell - mval].markdown(pressed_emoji.replace('|fill_variable|', '✅️'), True)
            elif mystate.plyrbtns[vcell]['isTrueFalse'] == False:
                globals()['cols' + arr_ref][vcell - mval].markdown(pressed_emoji.replace('|fill_variable|', '❌'), True)
        else:
            # Mostrar emoji en la celda
            vemoji = mystate.plyrbtns[vcell]['eMoji']
            globals()['cols' + arr_ref][vcell - mval].button(vemoji, on_click=PressedCheck, args=(vcell,),
                                                             key=f"B{vcell}")

    st.caption('')  # relleno vertical
    st.markdown(horizontal_bar, True)

    # Verificar si se alcanzó el límite de errores permitidos
    max_errors = (total_cells_per_row_or_col ** 2) // 2 + 1
    if mystate.myscore < -max_errors:
        # Mostrar mensaje de juego terminado
        st.error(
            "Game Over! You have reached the maximum number of errors. Please return to the main page to start a new game.")

        # Escribir en la tabla de clasificación
        Leaderboard('write')

        # Mostrar animaciones según el puntaje del jugador
        if mystate.myscore > 0:
            st.balloons()
        elif mystate.myscore <= 0:
            st.snow()

        # Esperar unos segundos antes de volver a la página principal
        tm.sleep(5)
        mystate.runpage = Main
        st.rerun()


def Main():
    """
       Página principal del juego Pix Match.

       Esta función muestra los controles de la barra lateral, donde el jugador puede seleccionar la dificultad del juego y proporcionar su nombre y país opcionalmente.
       También incluye un botón para iniciar un nuevo juego con la dificultad seleccionada.
       Si el jugador hace clic en el botón "New Game", se prepara el juego con la configuración seleccionada y se inicia la página de juego.

       Returns:
           None
       """
    st.markdown('<style>[data-testid="stSidebar"] > div:first-child {width: 310px;}</style>',
                unsafe_allow_html=True, )  # reduce sidebar width
    st.markdown(purple_btn_colour, unsafe_allow_html=True)

    InitialPage()
    with st.sidebar:
        # Controles de barra lateral: Es una entrada de informacion que permite al jugador sleccionar la dificultad y proporcionar un texto
        mystate.GameDetails[0] = st.radio('Difficulty Level:', options=('Easy', 'Medium', 'Hard'), index=1,
                                          horizontal=True, )
        mystate.GameDetails[3] = st.text_input("Player Name, Country", placeholder='Shawn Pereira, India',
                                               help='Optional input only for Leaderboard')

        if st.button(f"🕹️ New Game", use_container_width=True):

            if mystate.GameDetails[0] == 'Easy':
                mystate.GameDetails[1] = 8  # secs interval
                mystate.GameDetails[2] = 6  # total_cells_per_row_or_col

            elif mystate.GameDetails[0] == 'Medium':
                mystate.GameDetails[1] = 6  # secs interval
                mystate.GameDetails[2] = 7  # total_cells_per_row_or_col

            elif mystate.GameDetails[0] == 'Hard':
                mystate.GameDetails[1] = 5  # secs interval
                mystate.GameDetails[2] = 8  # total_cells_per_row_or_col

            Leaderboard('create')

            PreNewGame()
            mystate.runpage = NewGame
            st.rerun()

        st.markdown(horizontal_bar, True)


if 'runpage' not in mystate: mystate.runpage = Main
mystate.runpage()