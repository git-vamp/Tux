import asyncio
import pyttsx3
from speech_recognition import Recognizer, Microphone
from typing import List
from command import CommandClassType, Command, CommandType, CommandEvent, CommandEventType
import json
import vosk
from logger import logger


class Assistant:
    def __init__(self):
        self.recognizer = Recognizer()
        self.command = Command()
        self.engine = pyttsx3.Engine()
        self.loaded_commands: List[CommandClassType] = self.command.load_commands()
        self.recognizer.vosk_model = vosk.Model("./model")

    def recognize(self):
        with Microphone() as source:
            logger.debug("Listening For Audio")
            audio_data = self.recognizer.record(source=source, duration=3)

        return self.recognizer.recognize_vosk(audio_data)

    def eventloop(self):
        while True:
            prompt = json.loads(self.recognize())
            args: List[str] = prompt.get("text").split(" ")
            logger.debug(f"keyword:{args[0]}, args:{args[1:]}")
            if len(args) != 0 and args[0] != "":
                logger.debug(self.loaded_commands)
                for loaded_command in self.loaded_commands:
                    command: List[CommandType] = [cmd for cmd in loaded_command.get("command_class").get_commands()
                                                  if cmd.get("keyword") == args[0]]
                    logger.debug(command)
                    if len(command) != 0:
                        command: CommandType = command[0]
                        args.remove(command.get("keyword"))
                        output = asyncio.run(command.get('func')(args))
                        yield CommandEvent(name=command.get('keyword'), args=args, output=output,
                                           type=CommandEventType.COMMAND)

                        self.engine.say(output)
                        self.engine.runAndWait()


if __name__ == "__main__":
    assistant = Assistant()
    events = assistant.eventloop()
    for event in events:
        logger.debug(event)
