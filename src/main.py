import asyncio

from viam.resource.easy_resource import EasyResource
from viam.components.generic import Generic
from viam.module.module import Module
from viam.proto.app.robot import ComponentConfig
from typing import Mapping, Optional, Self
from viam.utils import ValueTypes
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam import logging

from adafruit_extended_bus import ExtendedI2C as I2C
from adafruit_ht16k33 import segments, ht16k33

LOGGER = logging.getLogger(__name__)

class Ht16k33_Seg14x4(Generic, EasyResource):
    MODEL = "michaellee1019:ht16k33:seg_14_x_4"
    i2c: I2C
    i2c_bus: int = 1
    segs = None
    addresses: list[int] = []

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
                    self.marquee(args['text'], args.get('delay'))
                    result[name] = True
                else:
                    result[name] = 'missing text parameter'
            if name == 'print':
                if 'value' in args:
                    self.print(args['value'], args.get('decimal'))
                    result[name] = True
                else:
                    result[name] = 'missing value parameter'
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
        self.segs.print(value, decimal = 0 if decimal is None else int(decimal))

    def set_digit_raw(self, index: int, bitmask: any) -> None:
        int_bitmask = bitmask if isinstance(bitmask, int) else int(bitmask, 0)
        self.segs.set_digit_raw(int(index), int_bitmask)

    @classmethod
    def new(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        output = self(config.name)
        output.reconfigure(config, dependencies)
        return output

    def reconfigure(self,
                    config: ComponentConfig,
                    dependencies: Mapping[ResourceName, ResourceBase]):
        
        if 'i2c_bus' in config.attributes.fields:
            self.i2c_bus = int(config.attributes.fields["i2c_bus"].number_value)

        self.i2c = I2C(self.i2c_bus)
        
        brightness = None
        auto_write = None
        if 'brightness' in config.attributes.fields:
            brightness = config.attributes.fields["brightness"].number_value
        if 'auto_write' in config.attributes.fields:
            auto_write = config.attributes.fields["auto_write"].bool_value

        if 'addresses' in config.attributes.fields:
            self.addresses = [int(address,16) for address in config.attributes.fields["addresses"].list_value]
        else:
            self.addresses = [int("0x70",16)]

        self.segs = segments.Seg14x4(
            i2c=self.i2c,
            address=self.addresses,
            auto_write= True if auto_write is None else auto_write,
            chars_per_display=4)

        if brightness is not None:
            ht16k33.HT16K33(self.i2c, self.addresses, brightness=brightness)

    @classmethod
    def validate_config(self, config: ComponentConfig) -> None:
        return None
    
if __name__ == "__main__":
    asyncio.run(Module.run_from_registry())