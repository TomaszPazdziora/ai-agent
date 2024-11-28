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

    instructions = "You are a helpful programming assistant. Your task is to create templates for programming projects. The user will provide you with instructions. You should create each of the files mentioned by the user and fill them with code that works according to the user's description. Use the 'write_to_file' tool to create the file and write the content to the created file. After completing the task, present the generated project file structure."
    
    query = "Create a website for me. I would like you to do it in Python. Use the Flask framework to write the application's backend. Create home, about and careers pages. The frontend should be written in HTML and CSS. I would like the page to have several buttons, input fields, and checkboxes. Place the entire project in a folder called 'web'. I like shrek."
    
    logger.info(f"User input: {query}")
    coder = Agent(tools=tools, master_prompt=instructions)
    coder.execute_query(query=query)
