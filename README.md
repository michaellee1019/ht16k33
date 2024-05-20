# michaellee1019:ht16k33
A Viam module that controls LED segment displays based on ht16k33/vk16k33 chips.

### michaellee1019:ht16k33
The ht16k33 family of components is a Viam wrapper around the [Adafruit_CircuitPython_HT16K33](https://github.com/adafruit/Adafruit_CircuitPython_HT16K33/) library. The model has also been tested and works with the vk16k33 family of components which functionality is similar to the ht16k33.

#### seg_14_x_4
This component supports 14-segment LED devices that have a four character display in each device. Depending on the device you can chain multiple displays together on the same channel, usually by soldering contacts that change the i2c address. Put each device address into the address array when wanting to string together the characters in each display, in the order that they are physically positioned from left to right.

This model implements the [adafruit_ht16k33.segments.Seg14x4 API](https://docs.circuitpython.org/projects/ht16k33/en/latest/api.html#adafruit_ht16k33.segments.Seg14x4)

Example Config
```
{
      "model": "michaellee1019:ht16k33:seg_14_x_4",
      "name": "segments",
      "type": "generic",
      "attributes": {
        "address": ["0x70","0x71"]
      },
      "depends_on": []
}
```

Example Do Commands:

Marquee text across the display once. Repeating marquee is currently not supported.
```
{"marquee":{"text":"MICHAELLEE1019"}}
```

Marquee text with a custom time between scrolls, in seconds
{"marquee":{"text":"MICHAELLEE1019","delay":0.1}}

Print text onto the display. This method does not clear existing characters so it is recommended to pad the text with space chacters.
```
{"print":{"value":"ELLO POPPET"}}
```

Print number. Optionally, provide `decimal` to round the number to a specific number of points.
```
{"print":{"value":3.14159265,"decimal":2}}
```

Not working:
{"scroll":{"count":2}}

Not working:
{"set_digit_raw":{"index":1,"bitmask":24}}

