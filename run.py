import base64
import json
import mimetypes

import click
from WPP_Whatsapp import Create

import settings
from agent import get_chat_response, AgentResponse
from media_processing import process_media
from settings import logger, GROUP_IDS, IM_A_BOT_MESSAGE, DM_MESSAGE

logger.debug("Starting whatsapp_sentinel")
# start client with your session name
SESSION_NAME = "personal_assistant"


def start_client():
    # start client with your session name
    global client  # noqa
    creator = Create(session=SESSION_NAME)
    client = creator.start()
    # Now scan Whatsapp Qrcode in browser

    # check state of login
    if creator.state != 'CONNECTED':
        raise Exception(creator.state)
    return creator


def get_media(message_id) -> tuple[str | None, str | None]:
    try:
        media = client.downloadMedia(message_id)
    except Exception as e:
        # print the error type so it can be handled
        logger.error(e.__class__.__name__)
        logger.error(e)
        return None, None
    if not media:
        return None, None
    # Remove the "data:video/mp4;base64," prefix
    base64_data = media.split(',')[1]
    # Decode the Base64 string
    media_data = base64.b64decode(base64_data)

    # Specify the file path where you want to save the video
    mime_type = media.split(',')[0].split(";")[0].split(":")[1]
    file_extension = mimetypes.guess_extension(mime_type)
    if not file_extension:
        file_extension = f'.{mime_type.split("/")[1]}'

    file_path = f'media/{message_id}{file_extension}'

    # Write the binary data to the file
    with open(file_path, 'wb') as file:
        file.write(media_data)
    return file_path, base64_data


def process_target_chat(body, path, caption):
    logger.debug("Group message")
    # Add your code here
    new_media_path = None
    if path:
        new_media_path = process_media(path)
    if new_media_path:
        caption = caption or ""
        agent_response = get_chat_response(caption, new_media_path)
    else:
        agent_response = get_chat_response(body)
    logger.debug(agent_response)
    return agent_response


def maybe_reply_to_chat(chat_id, agent_response: AgentResponse, message):
    if agent_response.political:
        response = agent_response.output
        client.reply(chat_id, response, message.get("id"))
        logger.info(f"Replied with: {response}")
        client.sendText(chat_id, IM_A_BOT_MESSAGE)
        from_sender = message.get("author").split("@")[0]
        logger.info(f"from_sender: {from_sender}")
        client.sendText(from_sender, DM_MESSAGE)


def new_message(message):
    # Add your Code here
    if message:
        logger.debug("message")
        chat_id = message.get("from")
        body = message.get("body")
        logger.debug(f"chat_id: {chat_id}")
        caption = message.get("caption")
        if message.get("mediaKey"):
            path, _ = get_media(message.get("id"))
        else:
            path = None
        if path:
            logger.debug(f"media path: {path}")
        else:
            logger.debug(f"body: {body}")
        if caption:
            logger.debug(f"caption: {caption}")
        if chat_id in GROUP_IDS:
            agent_response = process_target_chat(body, path, caption)
            maybe_reply_to_chat(chat_id, agent_response, message)
        logger.debug("----------------------")


def save_groups():
    groups = client.getAllGroups()
    save_json = []
    for group in groups:
        group_dict = {"id": group["id"]["_serialized"],
                      "name": group["groupMetadata"]["subject"],
                      "desc": group["groupMetadata"]["desc"]}
        save_json.append(group_dict)
    with open("groups.json", "w") as f:
        json.dump(save_json, f, indent=4, ensure_ascii=False)
    logger.debug("Groups saved to groups.json")


@click.command()
@click.option("--groups")
def start(groups):
    creator = start_client()
    # Add Listen To New Message
    if groups:
        save_groups()
        creator.__exit__()
    else:
        if not GROUP_IDS:
            logger.error("GROUP_IDS is empty, see README.md")
            creator.__exit__()
        client.onMessage(new_message)


if __name__ == "__main__":
    start()
