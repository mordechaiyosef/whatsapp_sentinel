import logging
import os

def get_logger(name):
    logger_instance = logging.getLogger(name)
    logger_instance.setLevel(logging.INFO)
    return logger_instance


logger = get_logger("whatsapp_sentinel")
GROUP_IDS = [
]
IM_A_BOT_MESSAGE = "Beep boop bop! 🤖 Just a bot here to keep things friendly. Let’s keep the chat fun and free of politics or heated debates. Peace and love, everyone! ✌️❤️"
DM_MESSAGE = "Hey there! 😊 Just a quick note from me, your friendly chat bot. Let's try to keep the group chat positive and avoid topics that might stir up strong feelings, like politics. Thanks for understanding!"
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY is empty, see README.md")
    exit(1)