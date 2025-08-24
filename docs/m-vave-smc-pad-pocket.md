# Overview

This document provides information about the MIDI protocol used by the M-VAVE SMC Pad Pocket controller.

> DISCLAIMER: This information was acquired by reverse enginering, so if may be incorrect or incomplete. Use it under your own responsability.


# Specifications

* 16 x RGB PADs, with aftertouch and pressure sensitivity
* Note repeat, swing and latch functions
* MIDI over Bluetooth and USB-C
* Internal battery of 780 mAh
* Charging/BL status LED
* Hardware switch for on/off

* 4 presets
* 7 banks (for each preset)
* Special function PADs (bank +/-, swing +/-, ...)
* PAD trigger sensitivity also can be adjusted (calibrated)

# Notes

* The messages include the SysEx start (0xF0) and end (0xF7) bytes, but these are ignored on byte counting. The name of the messages are just an indication of its purpose.

* Changes made on the controller settings are not persistent, unless a SAVE request is sent. This is not applicable to the calibration settings, which are persisted immediately.

* When a special function is set on a PAD, it will be enabled on all banks of that preset (i.e you can not have a special function on the same PAD with different banks).


# Common fields/information

* Manufacturer addresses: there are at least these:

  - `00 32 0D`: used for status or dump requests.
  - `00 32 09`: used for setup the controller (set a LED color, pad note, etc).
  - `00 32 01`: used for ACKs.

* Checksum: usually, the last two bytes of each message contains a checksum, aplied to the relevant fields of the message. The checksum is of 8-bits, but it is stored using a 7-bit packaging, where the MS-bits are saved on the LS-bits of the following byte. Moreover, if the previous byte has remaining bits to pack, the LS-bits of the first byte are also used, so the whole checksum gets offsetted.

* Setting address: the addressing scheme is the same for many properties: each property of each PAD of each bank of each preset can be addressed individually. The address generation scheme is always the same, but each property starts with a different offset, and is separated from the others PADs by a distance of 26 places. For instance, the offset for the LEDs is 5, and for the note number is 2.

  Addresses are created taking into account the preset, the bank and the PAD index. Each preset is separated from the next by a distance of 19 places. The address of certain property could be obtained with the formula:

  `address = prop_offset + 19 * preset + (preset * 7 * 16 + bank * 16 + pad) * 26`

  Being 7 the number of banks and 16 the number of PADs.

* The PAD mode property address is an exception of the previous rule, as the mode is only affected by the preset and the PAD (is shared across all banks of the same preset).


# Message list

---
`F0  00 32 0D  41 00 00 00 02  00 00 00 00  00 01 00 00  73 01  F7`

* Get STATUS request

  - **Checksum**: Bytes 17-18 (value `73 01`)

---
`F0  00 32 0D  01 01 00 00 02  00 00 00 00  00 01 00 00  20 01 58 11 00 20 00 00  03  2E 00  F7`

* STATUS response

  - **Current preset**: Byte 25 (ex. value: `03`)

  - **Checksum**: Bytes 26-27 (ex. value `2E 00`)

---
`F0  00 32 09  49 00 00 00 02  07 00 00 00  10 00 00 00  02  63 03 F7`

* Change PRESET request

  - **Preset**: Byte 17, a number in range [0-3] (ex. value: `02`, preset 3)

  - **Checksum**: Bytes 18-19 (ex. value `63 03`)

---
`F0  00 32 09  59 00 00 40 02  1E 4B 00 00  30 00 00 00  00 00 00  20 03  F7`

`F0  00 32 09  59 00 00 40 02  1E 4B 00 00  30 00 00 00  7F 01 00  28 03  F7`

`F0  00 32 09  59 00 00 40 02  1E 4B 00 00  30 00 00 00  00 7E 03  28 03  F7`

`F0  00 32 09  59 00 00 40 02  1E 4B 00 00  30 00 00 00  00 00 7C  2F 03  F7`

* Change PAD color request

  - **LED address**: Bytes 9-10 (ex. value `1E 4B`). This property has an address offset of 0x05.

  - **Color**: Bytes 17-19 (ex. values `00 00 00`, `7F 01 00`, `00 7E 03` and `00 00 7C`). This value is given in 8-bit RGB components, but they are packed in 7-bit bytes (as 8th bit in MIDI SysEx is reserved). So, the RED 7 LS-bits are stored in byte 17, and its MS-bit is stored in LS-bit of next byte. The GREEN 6 LS-bits are stored in byte 18 (with an offset of 1, for the MS-bit of red), and its 2 MS-bits are stored in the LS-bits of the next byte. The BLUE color is packed the same way, but now with an offset of 2 bits, and its remaining 3 MS-bits are saved in the following byte, which is the first byte of the checksum (which will have an offset of 3 bits too).

  - **Checksum**: Bytes 20-21 (ex. value `20 03`, `28 03` and `2F 03`)

---
`F0  00 32 09  49 00 00 40 02  00 00  00 00  10 00 00 00  01  70 03  F7`

* Change PAD property request

  - **Property address**: Bytes 9-10 (ex. value `00 00`). The specific property to change is given by this field. Each property type has its own initial offset. Known ones are:
    - LED: 0x05
    - Note number: 0x02
    - Channel: 0x01
    - PAD Type: 0x00
    - PAD Mode: 2912 (this addressing is different, as explained above)

  - **Property value**: Byte 17 (ex. value `01`). One single byte value, usually less than 128.

  - **Checksum**: Bytes 18-19 (ex. value `70 03`)

---
`F0  00 32 0D  41 00 00 40 02  00 00  00 00  10 7E 00 00  06 00  F7`

`F0  00 32 0D  41 00 00 40 02  71 07  00 00  10 7E 00 00  12 00  F7`

`F0  00 32 0D  41 00 00 40 02  5B 56  00 00  10 4E 00 00  01 00  F7`

* DUMP SETTINGS request

  - **Offset**: Bytes 9-10 (ex. values: `00 00`, `71 07` and `5B 56`). Position of data to read from.
    - List of known offsets: `00 00`, `71 07`, `62 0F`, `53 17`, `44 1F`, `35 27`, `26 2F`, `17 37`, `08 3F`, `79 46`, `6A 4E` and `5B 56`.

  - **Checksum**: Bytes 17-18 (ex. value `06 00`, `12 00` and `01 00`)

---
`F0  00 32 01  08 00 00 00 00  7F 01  F7`

* ACK response
