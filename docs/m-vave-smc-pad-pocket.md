# Overview

This document provides information about the MIDI protocol used by the M-VAVE SMC Pad Pocket controller.

> DISCLAIMER: This information was acquired by reverse enginering, so if may be incorrect or incomplete. Use it under your own responsability.


# Specifications

* 16 x RGB PADs, with aftertouch and pressure sensitivity
* Note repeat, swing and latch functions
* MIDI over Bluetooth and USB-C
* Internal battery of 780 mAh
* charging/BL status LED
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

* Manufacturer addresses: there are at least these address:
  - `00 32 0D`: used for status or dump requests.
  - `00 32 09`: used for setup the controller (set a LED color, pad note, etc).
  - `00 32 01`: used for ACKs.

* Checksum: usually, the last two bytes contains some kind of checksum, aplied to the relevant fields of the message. The checksum is of 8-bits, but it is stored using a 7-bit packaging, where the MS-bits are saved on the LS-bits of the following byte. Moreover, if the previous byte has remaining bits to pack, the LS-bits of the first byte are also used, so the whole checksum gets offsetted.


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

---
`F0  00 32 09  59 00 00 40 02  1E 4B 00 00  30 00 00 00  00 00 00  20 03  F7`

`F0  00 32 09  59 00 00 40 02  1E 4B 00 00  30 00 00 00  7F 01 00  28 03  F7`

`F0  00 32 09  59 00 00 40 02  1E 4B 00 00  30 00 00 00  00 7E 03  28 03  F7`

`F0  00 32 09  59 00 00 40 02  1E 4B 00 00  30 00 00 00  00 00 7C  2F 03  F7`

* Change PAD color request:
  - **PAD Address**: Bytes 9-10 (ex. value `1E 4B`)
  - **Color**: Bytes 17-19 (ex. values `00 00 00`, `7F 01 00`, `00 7E 03` and `00 00 7C`). This value is given in 8-Bit RGB components, but they are packed in 7-bit bytes (as 8th bit in MIDI SysEx is reserved). So, the RED 7 LS-bits are stored in byte 17, and its MS-bit is stored in LS-bit of next byte. The GREEN 6 LS-bits are stored in byte 18 (with an offset of 1, for the MS-bit of red), and its 2 MS-bits are stored in the LS-bits of the next byte. The BLUE color is packed the same way, but now with an offset of 2 bits, and its remaining 3 MS-bits are saved in the following byte, which is the first byte of the checksum (which will have an offset of 3 bits too).


---
`F0  00 32 0D  41 00 00 40 02  00 00  00 00  10 7E 00 00  06 00  F7`

`F0  00 32 0D  41 00 00 40 02  71 07  00 00  10 7E 00 00  12 00  F7`

`F0  00 32 0D  41 00 00 40 02  5B 56  00 00  10 4E 00 00  01 00  F7`

* DUMP SETTINGS request:
  - **Offset**: Bytes 9-10 (ex. values: `00 00`, `71 07` and `5B 56`)
    - List of known offsets: `00 00`, `71 07`, `62 0F`, `53 17`, `44 1F`, `35 27`, `26 2F`, `17 37`, `08 3F`, `79 46`, `6A 4E` and `5B 56`.

---
`F0  00 32 01  08 00 00 00 00  7F 01  F7`

* ACK response:

