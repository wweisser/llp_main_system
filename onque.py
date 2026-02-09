import ser_utils as su
import json
    
async def feed_queue(q, input: dict):
    try:
        if q and input:
            await q.put(input)
            # print('Item attached to que : ', input)
    except Exception as e:
        print("could not feed item to input que")
        print(e)

async def feed_qui_queue(q, input: dict):
    try:
        if q and input:
            await q.put(input)
            print('Item attached to que : ', input)
    except Exception as e:
        print("could not feed item to input que")
        print(e)

def create_q_item(msg_type: str, id: str, data):
    q_item = {
        'msg_type': '',
        'id': '',
        'data': ''
    }
    if msg_type:
        q_item['msg_type'] = msg_type
    if id:
        q_item['id'] = id
    if data:
        q_item['data'] = data
    return q_item

def parse_input(input):
    res = input[:9]
    if (res[0] == 32 and res[3] == 58 and res[6] == 58):
        return('cdi')
