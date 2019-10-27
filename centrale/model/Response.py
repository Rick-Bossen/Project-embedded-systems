from Enums import *


class Response:

    def __init__(self, response):
        self.raw_response = response
        self.decoded_response = False

    def decode(self):
        bytes = [b for b in self.raw_response]

        while len(bytes) > 0:
            byte = bytes.pop(0)
            type = byte >> 4

            if type not in [inner for inner in ResponseType]:
                continue
            elif not self.decoded_response:
                self.decoded_response = {}

            response_type = ResponseType(byte >> 4)
            value = byte & 0x0F

            if response_type is ResponseType.STATE_INFO:
                self.decoded_response['state'] = {
                    'name': State(value).name,
                    'value': value,
                    'value_in_cm': bytes.pop(0)
                }
            elif response_type is ResponseType.UNIT_INFO:
                self.decoded_response['unit'] = {
                    'name': Unit(value).name,
                    'value': value
                }
            elif response_type is ResponseType.UNIT_VALUE_INFO:
                if 'unit_values' not in self.decoded_response:
                    self.decoded_response['unit_values'] = {}

                self.decoded_response['unit_values'][Unit(value).name.lower()] = {
                    'open_at': bytes.pop(0),
                    'close_at': bytes.pop(0),
                    'current': bytes.pop(0),
                }
        return self.decoded_response
