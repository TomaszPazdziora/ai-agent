import os
from langchain_core.tools import tool
from logger import setup_logger
from dotenv import load_dotenv
import logging
import os
from agent import Agent


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
setup_logger(logger)
load_dotenv()


@tool
def write_to_file(content: str, file_path: str) -> None:
    """Writes content to a specified file. Both args are required!

    Args:
        content: Text that will be passed to given file
        file_path: Relative path to file
    """
    if os.sep in file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)


if __name__ == "__main__":
    tools = [write_to_file]

    # query = "Create example C project in test directory. You shoud create a main.c file two examples .c/.h files and a Makefile with build and execution instructions."

    instructions = "Jesteś pomocnym asystentem programisty. Twoim zadaniem jest tworzenie szablonów projektów programistycznych. Użytkownik będzie podawać Ci instrukcje. Powinieneś stworzyć każdy z plików podanych przez użytkownika oraz wypełnić go kodem działającym zgodnie z opisem użytkownika. Do tworzenia plików, wpisywania zawartości do plików oraz odczytywania zawartości z plików wykorzystaj powierzone Ci narzędzia. Po wykonaniu zadania opisz jakie pliki utworzyłeś oraz streść bardzo krótko co się w nich znajduje. W następnym kroku przedstaw strukturę utworzonego projektu. Oraz utwórz plik readme.md w którym opiszesz w jaki sposób uruchomić projekt."
    
    query = "Stwórz mi stronę internetową. Chciałbym żebyś zrobił to w pythonie. Wykorzystaj framework Flask do napisania backendu aplikacji. Stwórz główną stronę i parę odnośników do innych zakładek. Frontend powinien być napisany w htmlu i css. Chciałbym aby strona miała kilka przycisków, pól do wypełnienia oraz checkboxów. Cały projekt umieść w folderze 'web'"
    
    logger.info(f"User input: {query}")
    coder = Agent(tools=tools, master_prompt=instructions)
    coder.execute_query(query=query)
