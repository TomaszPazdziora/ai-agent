# AI Agent
A simple AI agent project created for educational purposes. The file **agent.py** defines a class that can be easily utilized in other projects. 

### **code_generator.py** 
The code_generator script is designed to create a basic configuration for a larger project or to generate code for a simple, small project. The LLM is equipped with the ability to create files and write content into them, ensuring that the generated code is directly placed into the created files.


### **smart house.py**
Script demonstrates an example application of the AI agent in a smart home project. It uses the Pygame library to create a simple visualization. Pressing the 'r' button will start recording audio. The recorded audio is transcribed using the Whisper OpenAI model. The received text is then sent to the AI agent, which decides on appropriate actions in the smart building. It is possible to open/close windows and turn on/off lights in one of the four available rooms.

## Usagage
To run scripts described above it is necessary to setup virtual enviroment and install required packages.

### Enviroment setup
```bash
python3 -m venv .venv # for Linux/macOS/GitBash
# or 
py -m venv .venv # for Windows PowerShell
```

### Enviroment activation
```bash
source .venv/bin/activate # Linux
# or
.venv/Source/activate # PowerShell
```

### Packages installation
```bash
pip install -r requirements.txt
```