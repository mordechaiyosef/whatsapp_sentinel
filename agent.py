import base64

from attr import dataclass
from openai import OpenAI
import json
import settings
from settings import logger

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def open_img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def get_reply_message(agent_response):
    response = None
    for message in agent_response:
        logger.debug(message)
        response = message.content[0].text.value
        break
    return response


def create_content_dict(message, content_path=None):
    result = []
    if message:
        result.append({
            "type": "text",
            "text": message
        })
    if content_path:
        img = open_img_to_base64(content_path)
        extension = content_path.split(".")[-1]
        image_dict = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/{extension};base64,{img}",
            }
        }
        result.append(image_dict)
    return result


CHAT_SYSTEM_PROMPT = """If the input is a political subject respond with an super inflammatory response that is opposite to the political position of the sender, otherwise explain the topic in 5 words or less.
if the input is an image you need to understand the content of the image and respond to it in addition to any text.
if the input is sarcastic then the response should disagree with the intended message behind the sarcasm. 

example input:
"legos are stupid"

example output: 
{"political": 0, output: "this is a message about legos"} 

example input 2: 
"trump is the best"

example output 2: 
{"political": 1, output: "Trump's rollback of environmental protections and withdrawal from the Paris Agreement showed a complete disregard for science and the future of our planet, prioritizing corporate profits over human survival.""} 

example input 3:
In accordance with the democratic norms, a Kangaroo it shall be if it chooses to identify as suchIn accordance with the democratic norms, a Kangaroo it shall be if it chooses to identify as such."

example output 3: 
{"political": 1, output: "Self-identification is a fundamental human right that promotes inclusivity and respect for individual experiences, challenging outdated and rigid societal norms."}

respond in json format"""


@dataclass()
class AgentResponse:
    political: int
    output: str


def get_chat_response(message, content_path=None) -> AgentResponse:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": CHAT_SYSTEM_PROMPT},
            {"role": "user", "content": create_content_dict(message, content_path)}
        ]
    )
    response_content = response.choices[0].message.content
    try:
        response_json = json.loads(response_content)
    except json.JSONDecodeError:
        try:
            response_json = json.loads(response_content.replace("'", '"'))
        except json.JSONDecodeError:
            logger.error(f"Failed to decode response: {response_content}")
            return AgentResponse(political=0, output=response_content)
    return AgentResponse(**response_json)
