import json

# inputString = '{"dhtNodeData": {"local": true, "id": "25b7fc02f4ac41141775c97950f37a728d07cba6c434fb75e45128c82551c332", "_predecessor": "25b7fc02f4ac41141775c97950f37a728d07cba6c434fb75e45128c82551c332", "_successor": "25b7fc02f4ac41141775c97950f37a728d07cba6c434fb75e45128c82551c332"}, "LogicalNode": {"id": "25b7fc02f4ac41141775c97950f37a728d07cba6c434fb75e45128c82551c332", "_agents": [{"id": "7c1c8cabcbb994ac334a45575d320bb387a1bf53fc4044c02a6bb7aed267f1f8ab69364a206f8a097f6eec015a9b291c3409842140369b04e656d4cdefd7acc016dbae09d03918011603db6381558d3f1608500d31740033451f8d44064465d8e120e14030352ce0dbf712fd5fbebcd4edba35bf3675262f3650e5fff7d3e811b6300caa0bde6a42aec306dcffef0b72330a24b115794c3dae43975c670b288765747a8352c2695d56a08ed226285519a2dd8523c38dfb7ba95256f3b3ba0ed0e9ed93a9d6a7bb10cb5de2b3b95ab78905f0d6a8813b2fab8c1185bd439671c8ee75c4ed56af73643de8302a68a1116e97de59b8c56bbfb80ac83a40a0badd2c", "ip": "localhost", "port": "5005", "rank": 0, "_hosting": "", "capacity": 4000}]}, "predDhtNode": {"local": true, "id": "25b7fc02f4ac41141775c97950f37a728d07cba6c434fb75e45128c82551c332", "_predecessor": "25b7fc02f4ac41141775c97950f37a728d07cba6c434fb75e45128c82551c332", "_successor": "25b7fc02f4ac41141775c97950f37a728d07cba6c434fb75e45128c82551c332"}, "succDhtNode": {"local": true, "id": "25b7fc02f4ac41141775c97950f37a728d07cba6c434fb75e45128c82551c332", "_predecessor": "25b7fc02f4ac41141775c97950f37a728d07cba6c434fb75e45128c82551c332", "_successor": "25b7fc02f4ac41141775c97950f37a728d07cba6c434fb75e45128c82551c332"}}'

# truc = json.loads(inputString)

a = {'b6538c727cfeb78a46c246f733693ba9693c98698e0c0b14154edae8b01ff822': {'node': Node(id='b6538c727cfeb78a46c246f733693ba9693c98698e0c0b14154edae8b01ff822'), 'use': 1}, 'a8079686655fcb2c46ff35a9b104779ccdcb9308fb2ebe13671176966e4283d7': {'node': Node(id='a8079686655fcb2c46ff35a9b104779ccdcb9308fb2ebe13671176966e4283d7'), 'use': 1}}
b = {'b6538c727cfeb78a46c246f733693ba9693c98698e0c0b14154edae8b01ff822': {'node': Node(id='b6538c727cfeb78a46c246f733693ba9693c98698e0c0b14154edae8b01ff822'), 'use': 1}, 'a8079686655fcb2c46ff35a9b104779ccdcb9308fb2ebe13671176966e4283d7': {'node': Node(id='a8079686655fcb2c46ff35a9b104779ccdcb9308fb2ebe13671176966e4283d7'), 'use': 1}}
c = {'b6538c727cfeb78a46c246f733693ba9693c98698e0c0b14154edae8b01ff822': {'node': Node(id='b6538c727cfeb78a46c246f733693ba9693c98698e0c0b14154edae8b01ff822'), 'use': 1}, 'a8079686655fcb2c46ff35a9b104779ccdcb9308fb2ebe13671176966e4283d7': {'node': Node(id='a8079686655fcb2c46ff35a9b104779ccdcb9308fb2ebe13671176966e4283d7'), 'use': 1}}
d = {'b6538c727cfeb78a46c246f733693ba9693c98698e0c0b14154edae8b01ff822': {'node': Node(id='b6538c727cfeb78a46c246f733693ba9693c98698e0c0b14154edae8b01ff822'), 'use': 1}}


truc = {
    "succ": a, 
    "pred": b,
    "me": c,
    "fin": d
}


print(json.dumps(truc, indent=4))