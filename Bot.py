import os
import json

import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.tools import VkTools
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


with open(os.path.join(os.path.dirname(__file__), 'tokens.json'), 'r') as fp:
    private_data = json.load(fp)


vk_session = vk_api.VkApi(token=private_data['access_token'])
longpoll = VkBotLongPoll(vk_session, private_data['group_id'])


class EventHandler:
    """
    Handles incoming events.
    """
    
    def __init__(self):
        pass
    
class ActionHandler:
    """
    Performs the specified action.
    """
    
    def __init__(self, api, key, server, ts):
        self.vk = api
        self.server_key = key
        self.server = server
        self.ts = ts
        
    def send_message(self, text, id, from_user=False):
        if from_user:
            self.vk.messages.send(
                key = self.server_key,
                server = self.server,
                ts = self.ts,
                random_id = get_random_id(),
                message = text,
                user_id = id
            )  
        else:
            self.vk.messages.send(
                key = self.server_key,
                server = self.server,
                ts = self.ts,
                random_id = get_random_id(),
                message = text,
                chat_id = id
            )  


class MessageHandler:
    """
    Handles incoming messages.
    """

    def __init__(self):
        from glitch_text.glitchmaker import Glitcher
        self.glitcher = Glitcher()
    
    
    def handle(self, msg):
        if msg != "STOP":
            response = self.glitcher.glitch(msg)
        else:
            response = "___STOP_LISTENING___"
            
        return response
                
    
class VkBot:
    """
    Connects to api.
    """
    
    def __init__(self, vk_session, key, server, ts, group_id):
        self.vk = vk_session.get_api()
        self.longpoll = VkBotLongPoll(vk_session, group_id)
        self.server_key = key
        self.server = server
        self.ts = ts
        
        self.action_handler = ActionHandler(self.vk, key, server, ts)
        self.message_handler = MessageHandler()
        
        self.is_listening = False
        
    def check_events(self):
        events = self.longpoll.check()
        return events
    
    def process_event(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.message['text']
            if not message:
                return
            response = self.message_handler.handle(message)
            


            if event.from_chat:
                send_to = event.chat_id
                from_user = False
            elif event.from_user:
                send_to = event.message.from_id
                from_user = True
            elif event.from_group:
                pass
            
            if response == "___STOP_LISTENING___":
                self.is_listening = False
                self.action_handler.send_message("Stopped.", send_to, from_user=from_user)
                return
            else:
                self.action_handler.send_message(response, send_to, from_user=from_user)

#             print(event.obj.from_id)
#             print(event.obj.text)
#             print(event.obj.chat_id)

        elif event.type == VkBotEventType.MESSAGE_REPLY:
            pass
#             print(event.obj.peer_id)
#             print(event.obj.text)
        elif event.type == VkBotEventType.MESSAGE_EDIT:
            pass
        elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            pass
#             print(event.obj.from_id)
#             print(event.obj.to_id)
        elif event.type == VkBotEventType.GROUP_JOIN:
            pass
#             print(event.obj.user_id)
        elif event.type == VkBotEventType.GROUP_LEAVE:
            pass
#             print(event.obj.user_id)
        else:
            pass
#             print(event.type)
            
    def get_conversation_messages(self, conversation_id, msg_ids):
        msg_ids = ''.join([f"{i}," for i in range(100)])
        
        messages = vk.messages.getByConversationMessageId(
            peer_id=2000000000+conversation_id,
            conversation_message_ids=msg_ids
        )
        
        return messages
    
    
    def listen(self):
        self.is_listening = True
        for event in longpoll.listen():
            self.process_event(event)
            if not self.is_listening:
                return



bot = VkBot(vk_session,
            key=private_data['key'],
            server=private_data['server'],
            ts=private_data['ts'],
            group_id=private_data['group_id']
           )


if __name__ == "__main__":
    bot.listen()

