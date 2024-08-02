import viam_wrap
from viam.components.generic import Generic
from viam.proto.app.robot import ComponentConfig
from typing import Mapping, Optional, Self
from viam.utils import ValueTypes
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
import sys

# Import all board pins and bus interface.
import board
import busio

# Import the HT16K33 LED matrix module.
from adafruit_ht16k33 import segments, ht16k33

class Ht16k33_Seg14x4(Generic):
    MODEL = "michaelleetest:ht16k33:seg_14_x_4"
    i2c = None
    segs = None

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        result = {key: False for key in command.keys()}
        for (name, args) in command.items():
            if name == 'marquee':
                if 'text' in args:
                    #TODO: NoneType is not converted to None
                    self.marquee(args['text'], args.get('delay'))
                    result[name] = True
                else:
                    result[name] = 'missing text parameter'
            if name == 'print':
                if 'value' in args:
                    # TODO: decimal results in Error: TypeError - slice indices must be integers or None or have an __index__ method
                    self.print(args['value'], args.get('decimal'))
                    result[name] = True
                else:
                    result[name] = 'missing value parameter'
            if name == 'print_hex':
                if 'value' in args:
                    self.print_hex(args['value'])
                    result[name] = True
                else:
                    result[name] = 'missing value parameter'
            if name == 'scroll':
                if 'count' in args:
                    self.scroll(args['count'])
                    result[name] = True
                else:
                    result[name] = 'missing count parameter'
            if name == 'set_digit_raw':
                if all(k in args for k in ('index','bitmask')):
                    self.set_digit_raw(args['index'], args['bitmask'])
                    result[name] = True
                else:
                    result[name] = 'missing index and/or bitmask parameters'
        return result

    
    def marquee(self, text: str, delay: float) -> None:
        # TODO try to support loop
        self.segs.marquee(text, loop = False, delay= 0 if delay is None else delay)

    def print(self, value, decimal: int) -> None:
        self.segs.print(value, decimal= 0 if decimal is None else decimal)

    def print_hex(self, value: int) -> None:
        self.segs.print_hex(value)

    def scroll(self, count: int) -> None:
        # TODO Error: IndexError - bytearray index out of range
        self.segs.scroll(2)

    def set_digit_raw(self, index: int, bitmask: int) -> None:
        # TODO Error: TypeError - unsupported operand type(s) for &=: 'float' and 'int'
        self.segs.set_digit_raw(1, bitmask)

    @classmethod
    def new(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        self.i2c = busio.I2C(board.SCL, board.SDA)
        
        brightness = None
        auto_write = None
        if 'brightness' in config.attributes.fields:
            brightness = config.attributes.fields["brightness"].number_value
        if 'auto_write' in config.attributes.fields:
            auto_write = config.attributes.fields["auto_write"].bool_value

        addresses = config.attributes.fields["addresses"].list_value
        hex_addresses=[]
        for address in addresses:
            hex_addresses.append(int(address,16))
            # set brightness through base class

        self.segs = segments.Seg14x4(
            i2c=self.i2c,
            address=hex_addresses,
            auto_write= True if auto_write is None else auto_write,
            chars_per_display=4)

        if brightness is not None:
            ht16k33.HT16K33(self.i2c, hex_addresses, brightness=brightness)

        output = self(config.name)
        return output

    @classmethod
    def validate_config(self, config: ComponentConfig) -> None:
        addresses = config.attributes.fields["addresses"].list_value
        if addresses is None:
            raise Exception('A address attribute is required for seg_14_x_4 component. Must be a string array of 1 or more addresses in hexidecimal format such as "0x00".')
        
        # TODO: assert len()>1, parse addresses here
        
        return None

if __name__ == '__main__':
    # necessary for pyinstaller to see it
    # build this with: 
    # pyinstaller --onefile --hidden-import viam-wrap --paths $VIRTUAL_ENV/lib/python3.10/site-packages installable.py 
    # `--paths` arg may no longer be necessary once viam-wrap is published somewhere
    # todo: utility to append this stanza automatically at build time
    viam_wrap.main(sys.modules.get(__name__))