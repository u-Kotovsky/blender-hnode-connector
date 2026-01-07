from typing import Optional

dmx_buffer = {}

def set_channel_value(channel: int, value: int) -> None:
    dmx_buffer[channel] = value

def get_channel_value(channel: int, default: Optional[int] = None) -> Optional[int]:
    #check if channel exists, return none if it doesn't
    return dmx_buffer.get(channel, default)
