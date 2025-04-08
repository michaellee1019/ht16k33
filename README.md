# Module michaellee1019:ht16k33
A Viam module that controls LED segment displays based on ht16k33/vk16k33 chips. This module is a Viam wrapper around the [Adafruit_CircuitPython_HT16K33](https://github.com/adafruit/Adafruit_CircuitPython_HT16K33/) library. The model has also been tested and works with the vk16k33 family of components which functionality is similar to the ht16k33.

## Model seg_14_x_4
This component supports 14-segment LED devices that have a four character display in each device. Depending on the device you can chain multiple displays together on the same channel, usually by soldering contacts that change the i2c address. Put each device address into the address array when wanting to string together the characters in each display, in the order that they are physically positioned from left to right.

This model implements the [adafruit_ht16k33.segments.Seg14x4 API](https://docs.circuitpython.org/projects/ht16k33/en/latest/api.html#adafruit_ht16k33.segments.Seg14x4)

### Supported Hardware
- [Adafruit 0.54" Quad Alphanumeric FeatherWing Display](https://www.adafruit.com/product/4261)
- [2Pcs Digital Tube Module Orange 0.54 Inch 4 Digit Tube Module LED Display 4 Digit Tube LED Segment Display Module I2C Tube Clock Display for Arduino](https://www.amazon.com/gp/product/B0BXDL1LFT/)

Note: Other hardware may work, but may have different segment mappings to the ht16k33/vk16k33. You should be able to use the `set_digit_raw` command to set the segments for your specific display.

### Configuration
```json
{
  "i2c_bus": <int>,
  "addresses": ["<hex_i2c_address_1>","<hex_i2c_address_2>"],
  "brightness": <float 0-1>,
  "auto_write": <true/false>
}
```

### Attributes
The following attributes are available for this model:

| Name          | Type   | Inclusion | Description                |
|---------------|--------|-----------|----------------------------|
| `i2c_bus`     | int    | Optional  | The I2C bus number. Defaults to `1`.        |
| `addresses`   | list   | Optional  | A list of I2C addresses in string hexadecimal format. Defaults to `["0x70"]`. |
| `brightness`  | float  | Optional  | The percentage brightness of the display as a number between 0 and 1. Defaults to `1`. |
| `auto_write`  | bool   | Optional  | Whether to automatically write to the display. Defaults to `true`. |

### Example Do Commands:

#### Marquee
Marquee text across the display once. Repeating marquee is currently not supported.
```json
{
  "marquee": {
    "text": "MICHAELLEE1019"
  }
}
```

Marquee text with a custom time between scrolls, in seconds
```json
{
  "marquee": {
    "text": "MICHAELLEE1019",
    "delay": 0.1
  }
}
```

#### Print
Print text onto the display. This method does not clear existing characters so it is recommended to pad the text with space chacters.
```json
{
  "print": {
    "value": "ELLO POPPET"
  }
}
```

Print number. Optionally, provide `decimal` to round the number to a specific number of points.
```json
{
  "print": {
    "value": 3.14159265,
    "decimal": 2
  }
}
```

Note: printing characters onto the display is pushed to the end of the display. If you send a single character, it will be placed in the right most digit, pushing any existing characters to the left. To clear the display, you can send space characters to `print`, or always send a string of characters matching the number of digits in the display.

#### Set Digit Raw
To get finer control over the display, you can set the raw bitmask for a specific digit. `index` is the index of the digit to set (0-3), and `bitmask` is a two byte integer from 0 to 65535 where each bit represents a segment of the display from 1-16. 

The most logical way to pass in the `bitmask` is as a binary string. The bits in the string represent a single segment of the display. The bits are ordered depending on the specific wiring of the segments on the display. The usual order is    reverse alphabetical such as`N-M-L-K-J-H-G-F-E-D-C-B-A`. You should check the datasheet of the display you are using to confirm the order. Seriously though, there is a ton of variation in how the segments are wired. Some displays will have two "A", and/or two "D" segments, and/or some with two "G" segments. The different display models will have different bit masks.

Using the [Adafruit 0.54" Quad Alphanumeric FeatherWing Display](https://www.adafruit.com/product/4261) for example, the following various bitmasks will light up the display in different ways:

| Bitmask | Result |
| --- | --- |
| `0b000000000000000` | Turn off all segments |
| `0b000000000000001` | Lights up segment A |
| `0b000000000000010` | Lights up segment B |
| ... | ... |
| `0b001000000000000` | Lights up segment M |
| `0b010000000000000` | Lights up segment N |
| `0b100000000000000` | Lights up segment Decimal Point (DP) |
| `0b111111111111111` | Lights up all segments |

The DoCommand payload to display a 0 on the second digit of a 14x4 display would be:
```json
{
  "set_digit_raw": {
    "index": 1,
    "bitmask": "0b000000000111111"
  }
}
```

