import pytest
from src.message import message_send_v2 as message_send
from src.message import message_sendlater_v1 as message_sendlater
from src.message import message_senddm_v1
from src.channels import channels_create_v2 as channels_create
from src.dm import dm_create_v1
from src.auth import auth_register_v2 as register
import src.error as error
import src.helper as helper
from src.other import clear_v1 as clear
from datetime import datetime, timezone
import time

'''
test InputError
'''
def test_invalid_channelid():
    clear()
    
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    message_content = "hi"
    now_time = datetime.utcnow()
    now_timestamp = int(now_time.replace(tzinfo=timezone.utc).timestamp())
    time_sent_after = now_timestamp + 3
    
    with pytest.raises(error.InputError):
        message_sendlater(token1, -7, message_content, time_sent_after)


def test_message_too_long():
    clear()
    
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_id = channel['channel_id']
    message_content = "hi"*666
    now_time = datetime.utcnow()
    now_timestamp = int(now_time.replace(tzinfo=timezone.utc).timestamp())
    time_sent_after = now_timestamp + 3
    
    with pytest.raises(error.InputError):
        message_sendlater(token1, channel_id, message_content, time_sent_after)

def test_time_past():
    clear()
    
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_id = channel['channel_id']
    message_content = "hi"
    now_time = datetime.utcnow()
    now_timestamp = int(now_time.replace(tzinfo=timezone.utc).timestamp())
    time_sent_before = now_timestamp - 3
    
    with pytest.raises(error.InputError):
        message_sendlater(token1, channel_id, message_content, time_sent_before)

'''
test AccessError
'''
def test_invalid_token():
    clear()
    
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_id = channel['channel_id']
    message_content = "hi"
    now_time = datetime.utcnow()
    now_timestamp = int(now_time.replace(tzinfo=timezone.utc).timestamp())
    time_sent_after = now_timestamp + 3
    
    with pytest.raises(error.AccessError):
        message_sendlater(token1 + 'abc', channel_id, message_content, time_sent_after)

def test_not_member():
    clear()
    
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', '12asdcde', 'Robin', 'Hood')
    
    token1 = user1['token']
    token2 = user2['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_id = channel['channel_id']
    message_content = "hi"
    now_time = datetime.utcnow()
    now_timestamp = int(now_time.replace(tzinfo=timezone.utc).timestamp())
    time_sent_after = now_timestamp + 3
    
    with pytest.raises(error.AccessError):
        message_sendlater(token2, channel_id, message_content, time_sent_after)


def test_sendlater_success():
    clear()
    
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', '123asdbc', 'Mickey', 'Mouse')
    
    token1 = user1['token']
    channel = channels_create(token1, 'channel_one', True)
    channel_id = channel['channel_id']
    message_content = "hi"
    dm = dm_create_v1(token1, [user2['auth_user_id']])
    dm_one_id = dm['dm_id']
    message_senddm_v1(token1, dm_one_id, "hi")
    now_time = datetime.utcnow()
    now_timestamp = int(now_time.replace(tzinfo=timezone.utc).timestamp())
    time_sent_after = now_timestamp + 3

    message_id = message_sendlater(token1, channel_id, message_content, time_sent_after)

    
    assert message_id['message_id'] == 2