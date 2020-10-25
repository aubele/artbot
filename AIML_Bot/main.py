import aiml
import os

if __name__ == "__main__":
    kernel = aiml.Kernel()

    # Later you probably want brain files
    """if os.path.isfile("bot_brain.brn"):
        kernel.bootstrap(brainFile="bot_brain.brn")
    else:
        kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
        kernel.saveBrain("bot_brain.brn")"""
    kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")

    # At the start set the greetings topic
    kernel.setPredicate("topic", "greet")

    while True:
        message = input("Enter your message >> ")
        if message == "quit" or message == "exit":
            exit()
        elif message == "save":
            kernel.saveBrain("bot_brain.brn")
        else:
            bot_response = kernel.respond(message)
            print(bot_response)
