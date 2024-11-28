import pygame
import os
from openai import OpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import sys
from agent import Agent
import sounddevice as sd
import wavio
from logger import setup_logger
from dotenv import load_dotenv
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
setup_logger(logger)
load_dotenv()

import whisper
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

model = whisper.load_model("small")
audio_file = "output.wav"
RECORDING_TIME = 7
use_api = True

if use_api == True:
    client = OpenAI()

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
WIDTH, HEIGHT = 800, 600
ROOM_WIDTH = WIDTH / 2
ROOM_HEIGHT = HEIGHT / 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Smart House')

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (100, 100, 255)

bulb_image = pygame.image.load("imgs" + os.sep + "bulb.png") 
window_image = pygame.image.load("imgs" + os.sep + "window.png")  
bulb_image = pygame.transform.scale(bulb_image, (60, 60)) 
window_image = pygame.transform.scale(window_image, (60, 80)) 

# Definicja klasy Room
class Room:
    def __init__(self, name: str, description: str, color: tuple, x: int, y: int):
        self.name = name
        self.description = description
        self.color = color
        self.light_on = False
        self.window_open = False
        self.x = x
        self.y = y

    def get_info(self):
        return f"# room name: {self.name}, room description: {self.description} #"
    
    def draw_room(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, WIDTH // 2, HEIGHT // 2))
        if self.light_on:
            screen.blit(bulb_image, (self.x + ROOM_WIDTH * 3/4 - 20, self.y + ROOM_HEIGHT * 1/4 - 20))

        if self.window_open:
            screen.blit(window_image, (self.x + ROOM_WIDTH * 1/2 - 30, self.y + ROOM_HEIGHT * 1/2 - 30))


        pygame.draw.rect(screen, WHITE, (self.x, self.y, 140, 40))
        font = pygame.font.Font(None, 36)
        text = font.render(self.name, True, BLACK)
        screen.blit(text, (self.x, self.y))


# Utworzenie obiektów klasy Room
sypialnia = Room(name="sypialnia",
                 description="lewy górny róg, niebieskie ściany",
                 color=(200, 200, 255),
                 x=0,
                 y=0)

lazienka = Room(name="łazienka",
                description="prawy górny róg, czerwone ściany",
                color=(255, 200, 200),
                 x=WIDTH // 2,
                 y=0)

salon = Room(name="salon",
                description="lewy dolny róg, zielone ściany",
                color=(200, 255, 200),
                x=0,
                y=HEIGHT // 2)

kuchnia = Room(name="kuchnia",
                description="prawy dolny róg, szare ściany",
                color=(200, 200, 200),
                x=WIDTH // 2,
                y=HEIGHT // 2)

# lista wszystkich pokoi
rooms = [sypialnia, lazienka, salon, kuchnia]


# Definicja narzędzi Agenta
@tool
def switch_light(room_name: str, light_on: bool) -> None:
    """Switches light in given room. Both args are required!

    Args:
        room_name: name of the room where light will be switched
        light_on: boolean value, True for turning light on, False for turning light off
    """
    if room_name == "sypialnia":
        sypialnia.light_on = light_on
    elif room_name == "łazienka":
        lazienka.light_on = light_on
    elif room_name == "salon":
        salon.light_on = light_on
    elif room_name == "kuchnia":
        kuchnia.light_on = light_on


@tool
def set_window_state(room_name: str, window_state: bool) -> None:
    """Change state of open in given room. Both args are required!

    Args:
        room_name: name of the room where window state will be changed
        light_on: boolean value, True for opening window, False for closing window
    """
    if room_name == "sypialnia":
        sypialnia.window_open = window_state
    elif room_name == "łazienka":
        lazienka.window_open = window_state
    elif room_name == "salon":
        salon.window_open = window_state
    elif room_name == "kuchnia":
        kuchnia.window_open = window_state


def get_rooms_description() -> str:
    """Gets all room names and desrciption. Description contain room placement, walls colour."""
    ret_str = ''
    for r in rooms:
        ret_str += r.get_info()
    return ret_str

# Ustawienia nagrywania
samplerate = 44100
recorded_data = []

# Funkcja do nagrywania audio
def record_audio():
    logger.info("Recording started...")
    recorded_data = sd.rec(int(RECORDING_TIME * samplerate), samplerate=samplerate, channels=2)
    sd.wait()
    wavio.write("output.wav", recorded_data, samplerate, sampwidth=2)
    logger.info("Recording ended")


def transcribe_audio() -> str:
    logger.info("Transcryption started...")
    # use api transcryption or local model
    if use_api == True:
        file= open(audio_file, "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=file,
            language="pl"
        )
        res = "Transcryption result:" + transcription.text
    else:
        result = model.transcribe(audio_file, language="pl")
        res = "Transcryption result:" + result["text"]
    logger.info("Tanskryption ended")
    logger.info(res)
    return res


def main():
    # Utworzenie obiektu klasy Agent
    master_prompt = SystemMessage("Jesteś pomocnym systemem domu inteligentnego. Wykonuj polecenia użytkownika. Do wykonywania poleceń zastosuj dostępnych Ci narzędzi. Do zapalenia lub zgaszenia światła wykorzystaj narzędzie 'switch_light'. Do otwierania lub zamykania okien wykorzystaj narzędzie 'set_window_state'")
    tools = [switch_light, set_window_state]
    room_ai = Agent(tools=tools, master_prompt=master_prompt)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    record_audio()
                    res = transcribe_audio()

                    logger.info("Agent execution started...")
                    room_ai.execute_query(HumanMessage(res + "wiedząc, że: " + get_rooms_description()))
                    logger.info("Agent execution ended")
                else:
                    pass
        
        # wyczyszczenie ekranu
        screen.fill(BLACK)

        # na czarny ekran narysowywane są pokoje
        for r in rooms:
            r.draw_room()

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
