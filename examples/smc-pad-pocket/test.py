#!/usr/bin/env python3

import mido
from hexdump import hexdump

# Cambia esto por tu puerto MIDI de salida
MIDI_OUT_PORT = "SINCO:SINCO SMC-PAD Pocket-Private"

# Dirección y color para pad 2 en violeta
# sysex_msg = [
#     0xF0,       # inicio SysEx
#     0x00, 0x32, 0x09, 0x59, 0x00, 0x00, 0x40, 0x02,  # header fijo del controlador
#     0x5F, 0x06,   # bytes de dirección del pad 2
#     0x00, 0x00, 0x30, 0x00, 0x00, 0x00,  # bytes fijos según el mensaje original
#     0x7F, 0x00, 0x7F,  # color RGB (violeta)
#     0x30, 0x09,  # bytes de posición interna del pad 2
#     0xF7        # fin SysEx
# ]

# SysEx Start : 1byte
# ID (00 + B1 + b2) : 3bytes
# SysEx End : 1byte

# RED, pads 1 - 8
# f0  00 32 09  59 00 00 40 02  45 06  00 00 30 00 00 00 7f 01 00  00 0b  f7
# f0  00 32 09  59 00 00 40 02  5f 06  00 00 30 00 00 00 7f 01 00  30 09  f7
# f0  00 32 09  59 00 00 40 02  79 06  00 00 30 00 00 00 7f 01 00  60 07  f7
# f0  00 32 09  59 00 00 40 02  13 07  00 00 30 00 00 00 7f 01 00  10 06  f7
# f0  00 32 09  59 00 00 40 02  2d 07  00 00 30 00 00 00 7f 01 00  40 04  f7
# f0  00 32 09  59 00 00 40 02  47 07  00 00 30 00 00 00 7f 01 00  70 02  f7
# f0  00 32 09  59 00 00 40 02  61 07  00 00 30 00 00 00 7f 01 00  20 01  f7
# f0  00 32 09  59 00 00 40 02  7b 07  00 00 30 00 00 00 7f 01 00  50 0f  f7

# GREEN, pads 1 - 8
# f0  00 32 09  59 00 00 40 02  45 06  00 00 30 00 00 00 00 7e 03  00 0b  f7
# f0  00 32 09  59 00 00 40 02  5f 06  00 00 30 00 00 00 00 7e 03  30 09  f7
# f0  00 32 09  59 00 00 40 02  79 06  00 00 30 00 00 00 00 7e 03  60 07  f7
# f0  00 32 09  59 00 00 40 02  13 07  00 00 30 00 00 00 00 7e 03  10 06  f7
# f0  00 32 09  59 00 00 40 02  2d 07  00 00 30 00 00 00 00 7e 03  40 04  f7
# f0  00 32 09  59 00 00 40 02  47 07  00 00 30 00 00 00 00 7e 03  70 02  f7
# f0  00 32 09  59 00 00 40 02  61 07  00 00 30 00 00 00 00 7e 03  20 01  f7
# f0  00 32 09  59 00 00 40 02  7b 07  00 00 30 00 00 00 00 7e 03  50 0f  f7

# BLUE, pad 1
# f0  00 32 09  59 00 00 40 02  45 06  00 00 30 00 00 00 00 00 7c  07 0b  f7

# YELLOW, pad 1
# f0  00 32 09  59 00 00 40 02  45 06  00 00 30 00 00 00 7f 7f 03  08 0b  f7

# WHITE, pad 1
# f0  00 32 09  59 00 00 40 02  45 06  00 00 30 00 00 00 7f 7f 7f  17 0b  f7

def rgb_to_midi_bytes(r, g, b):
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    # 0RRR RRRR
    # 0GGG GGGR
    # 0BBB BBGG
    # 0XXX XBBB

    # Byte 1: first 7 bits of RED
    byte1 = r & 0x7F  # R0-R6

    # Byte 2: bit 7 of RED + first 6 bits of GREEN
    byte2 = ((r >> 7) & 0b1) | ((g & 0x3F) << 1)  # R7 + G0-G5

    # Byte 3: bits 6-7 of GREEN + first 5 bits of BLUE
    byte3 = ((g >> 6) & 0b11) | ((b & 0x1F) << 2)  # G6-G7 + B0-B4

    # Byte 4: bits 5-7 of BLUE
    byte4 = (b >> 5) & 0b111  # B5-B7

    return [byte1, byte2, byte3, byte4]


def midi_bytes_to_rgb(byte1, byte2, byte3, byte4):
    r = ((byte2 & 0x01) << 7) | (byte1 & 0x7F)
    g = ((byte3 & 0x03) << 6) | ((byte2 >> 1) & 0x3F)
    b = ((byte4 & 0x03) << 5) | ((byte3 >> 2) & 0x1F)
    return r, g, b


# sysex_msg = list(bytes.fromhex(
#     "f0  00 32 09  59 00 00 40 02  45 06  00 00 30 00 00 00 7f 01 00  00 0b  f7"
# ))

# color = (0, 0, 0)
# sysex_msg[-6:-2] = rgb_to_midi_bytes(*color)
# hexdump(bytes(sysex_msg))

# msg = mido.Message('sysex', data=sysex_msg[1:-1])

# with mido.open_output(MIDI_OUT_PORT) as outport:
#     outport.send(msg)
#     print(f"Pad set to {color}")





# def popcount(byte):
#     """Cuenta el número de bits a 1 en un byte."""
#     return bin(byte).count('1')

# def verificar_checksum(msg):
#     """
#     msg: lista de enteros, ejemplo:
#     [0x00, 0x32, 0x09, ..., 0x17, 0x0b, 0xf7]
#     """
#     # Quitamos F0 y F7 si están incluidos
#     if msg[0] == 0xF0: msg = msg[1:]
#     if msg[-1] == 0xF7: msg = msg[:-1]

#     # Tomamos todos los bytes excepto los últimos dos
#     datos = msg[:-2]
#     checksum1, checksum2 = msg[-2], msg[-1]

#     total_bits = sum(popcount(b) for b in datos)
#     print(f"Total bits a 1: {total_bits:02x}")
#     print(f"Checksum del mensaje: {checksum1:02x} {checksum2:02x}")

# # Ejemplo con tu mensaje de blanco
# mensaje = [0xF0, 0x00, 0x32, 0x09, 0x59, 0x00, 0x00, 0x40, 0x02,
#            0x45, 0x06, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x7f, 0x7f, 0x7f,
#            0x17, 0x0b, 0xF7]

# verificar_checksum(mensaje)


def generar_checksum(mensaje):
    """
    mensaje: lista de enteros, sin incluir F0 ni F7
    Devuelve los dos bytes de checksum según tu esquema:
    - Byte 1: bits 6,5,4,3 → popcount parcial
              bits 2,1,0 → reservados para color azul
    - Byte 2: nibble inferior → popcount adicional
    """
    # Inicializamos los contadores de bits
    total_bits = 0

    # Contamos bits a 1 de todos los bytes excepto los dos últimos (si existieran)
    for b in mensaje:
        total_bits += bin(b).count("1")

    # Byte 1: ponemos popcount en bits 6–3
    byte1 = ((total_bits & 0b1111) << 3)  # 4 bits para bits 6–3
    # Bits 2–0 ya están ocupados por azul, se dejan en 0
    byte1 |= mensaje[-1]

    # Byte 2: nibble inferior con popcount restante
    byte2 = total_bits >> 4  # desplazamos 4 bits que ya usamos en byte1

    return byte1 & 0x7F, byte2 & 0x7F  # aseguramos que cada byte < 128

# Ejemplo de uso con un mensaje (sin F0 ni F7)
# f0  00 32 09  59 00 00 40 02  45 06  00 00 30 00 00 00 00 7e 03  00 0b  f7
# mensaje = [
#     # 0xF0,
#     0x00, 0x32, 0x09,
#     0x59, 0x00, 0x00, 0x40, 0x02,
#     0x45, 0x06,
#     0x00, 0x00, 0x30, 0x00, 0x00, 0x00,
#     0x7f, 0x7f, 0x7f,
#     0x17 & 0x05,
#     # 0x0b, 0xF7,
# ]

# mensaje = [
#     # 0xF0,
#     0x00, 0x32, 0x09,
#     0x59, 0x00, 0x00, 0x40, 0x02,
#     0x45, 0x06,
#     0x00, 0x00, 0x30, 0x00, 0x00, 0x00,
#     0x00, 0x00, 0x00,
#     0x78 & 0b111,
#     # 0x0A,
#     # 0xF7,
# ]

# chk1, chk2 = generar_checksum(mensaje)
# print(f"Checksum generado: {chk1:02x} {chk2:02x}")



# # Lista de mensajes SysEx RED (como ejemplo)
messages_red = [
    "f0  00 32 09  59 00 00 40 02  45 06  00 00 30 00 00 00 7f 01 00  00 0b  f7",
    "f0  00 32 09  59 00 00 40 02  5f 06  00 00 30 00 00 00 7f 01 00  30 09  f7",
    "f0  00 32 09  59 00 00 40 02  79 06  00 00 30 00 00 00 7f 01 00  60 07  f7",
    "f0  00 32 09  59 00 00 40 02  13 07  00 00 30 00 00 00 7f 01 00  10 06  f7",
    "f0  00 32 09  59 00 00 40 02  2d 07  00 00 30 00 00 00 7f 01 00  40 04  f7",
    "f0  00 32 09  59 00 00 40 02  47 07  00 00 30 00 00 00 7f 01 00  70 02  f7",
    "f0  00 32 09  59 00 00 40 02  61 07  00 00 30 00 00 00 7f 01 00  20 01  f7",
    "f0  00 32 09  59 00 00 40 02  7b 07  00 00 30 00 00 00 7f 01 00  50 0f  f7",
]

# def parse_message(msg):
#     return [int(x, 16) for x in msg.split()]

# def calculate_checksum(msg_bytes):
#     # Excluir f0, f7, b5 y nibble alto de b4
#     bytes_for_checksum = msg_bytes[1:-2].copy()  # todo menos f0 y b4+b5
#     bytes_for_checksum[-1] &= 0x0F  # mantener solo nibble bajo de b4

#     # print(bytes_for_checksum)

#     # Posibles métodos de checksum
#     sum_mod128 = sum(bytes_for_checksum) % 128
#     sum_mod256 = sum(bytes_for_checksum) % 256
#     xor_all = 0
#     for b in bytes_for_checksum:
#         xor_all ^= b
#     bits_set = sum(bin(b).count("1") for b in bytes_for_checksum)

#     return sum_mod128, sum_mod256, xor_all, bits_set

# for i, msg in enumerate(messages_red):
#     msg_bytes = parse_message(msg)

#     # b4 = msg_bytes[-2], b5 = msg_bytes[-1]
#     b4, b5 = msg_bytes[-3], msg_bytes[-2]

#     sum128, sum256, xor_val, bits_set = calculate_checksum(msg_bytes)
#     chs = (b4 >> 4) | (b5 << 4)
#     print(f"Pad {i+1}: b4={b4:02X}, b5={b5:02X} | {chs:02X} : "
#           f"Checksum? sum128={sum128:02X}, sum256={sum256:02X}, "
#           f"xor={xor_val:02X}, bits={bits_set:02X}")




# messages_red = [
#     "f0 00 32 09 59 00 00 40 02 45 06 00 00 30 00 00 00 7f 01 00 00 0b f7",
#     "f0 00 32 09 59 00 00 40 02 5f 06 00 00 30 00 00 00 7f 01 00 30 09 f7",
#     "f0 00 32 09 59 00 00 40 02 79 06 00 00 30 00 00 00 7f 01 00 60 07 f7",
# ]

# def parse_message(msg):
#     return [int(x, 16) for x in msg.split()]

# def get_bytes_for_checksum(msg_bytes):
#     # Excluir f0, f7 y nibble alto de b4
#     b4, b5 = msg_bytes[-2], msg_bytes[-1]
#     bytes_for_checksum = msg_bytes[1:-2].copy()
#     bytes_for_checksum[-1] &= 0x0F  # conservar nibble bajo de b4
#     return bytes_for_checksum, b4, b5

# def test_checksum_ops(bytes_for_checksum, target_b4, target_b5):
#     # Operaciones posibles a probar
#     s = sum(bytes_for_checksum) & 0xFF  # suma módulo 256
#     xor = 0
#     for b in bytes_for_checksum:
#         xor ^= b
#     nibbles = sum((b & 0xF0) >> 4 for b in bytes_for_checksum) + sum(b & 0x0F for b in bytes_for_checksum)

#     candidates = [s, xor, nibbles, (~s)&0xFF, (~xor)&0xFF]  # incluir complementos
#     for c in candidates:
#         if ((c >> 4) & 0x0F) == (target_b4 >> 4) and (c & 0x0F) == (target_b5 & 0x0F):
#             return c
#     return None

# for msg in messages_red:
#     msg_bytes = parse_message(msg)
#     bytes_for_checksum, b4, b5 = get_bytes_for_checksum(msg_bytes)
#     checksum = test_checksum_ops(bytes_for_checksum, b4, b5)
#     print(f"Mensaje: {msg}")
#     if checksum is not None:
#         print(f"  Checksum deducido: {checksum:02X}")
#     else:
#         print("  No se encontró operación que coincida")



# messages = [
#     # RED pads 1-3 como ejemplo, añade el resto después
#     "f0 00 32 09 59 00 00 40 02 45 06 00 00 30 00 00 00 7f 01 00 00 0b f7",
#     "f0 00 32 09 59 00 00 40 02 5f 06 00 00 30 00 00 00 7f 01 00 30 09 f7",
#     "f0 00 32 09 59 00 00 40 02 79 06 00 00 30 00 00 00 7f 01 00 60 07 f7",
# ]

# def parse_message(msg):
#     return [int(x, 16) for x in msg.split()]

# def relevant_bytes(msg_bytes):
#     # Excluye f0 y f7
#     b4, b5 = msg_bytes[-2], msg_bytes[-1]
#     data = msg_bytes[1:-2].copy()
#     data[-1] &= 0x0F  # conservar solo nibble bajo de b4
#     return data, b4, b5

# def bits_set(byte_list):
#     return sum(bin(b).count('1') for b in byte_list)

# def sum_nibbles(byte_list):
#     return sum((b >> 4) + (b & 0x0F) for b in byte_list)

# def guess_checksum(messages):
#     for i, msg in enumerate(messages):
#         msg_bytes = parse_message(msg)
#         data, b4, b5 = relevant_bytes(msg_bytes)
#         # valores reales del checksum
#         real_b4 = b4 >> 4
#         real_b5 = b5 & 0x0F

#         # probar combinaciones simples
#         bits = bits_set(data)
#         nibbles = sum_nibbles(data)
#         candidates = []
#         for op in ['bits', 'nibbles', 'bits+nibbles', 'bits^nibbles', 'bits+1', 'nibbles+1']:
#             if op == 'bits':
#                 val = bits & 0x0F
#             elif op == 'nibbles':
#                 val = nibbles & 0x0F
#             elif op == 'bits+nibbles':
#                 val = (bits + nibbles) & 0x0F
#             elif op == 'bits^nibbles':
#                 val = (bits ^ nibbles) & 0x0F
#             elif op == 'bits+1':
#                 val = (bits + 1) & 0x0F
#             elif op == 'nibbles+1':
#                 val = (nibbles + 1) & 0x0F

#             if val == real_b4 or val == real_b5:
#                 candidates.append(op)
#         print(f"Msg {i+1}: b4={real_b4:02X}, b5={real_b5:02X}, candidates={candidates}")

# guess_checksum(messages)



# # -*- coding: utf-8 -*-
# from itertools import product

# # Tus mensajes SysEx (sin F0 y F7)
# messages = [
#     # RED, pads 1-8
#     "00 32 09 59 00 00 40 02 45 06 00 00 30 00 00 00 7f 01 00 00 0b",
#     "00 32 09 59 00 00 40 02 5f 06 00 00 30 00 00 00 7f 01 00 30 09",
#     "00 32 09 59 00 00 40 02 79 06 00 00 30 00 00 00 7f 01 00 60 07",
#     "00 32 09 59 00 00 40 02 13 07 00 00 30 00 00 00 7f 01 00 10 06",
#     "00 32 09 59 00 00 40 02 2d 07 00 00 30 00 00 00 7f 01 00 40 04",
#     "00 32 09 59 00 00 40 02 47 07 00 00 30 00 00 00 7f 01 00 70 02",
#     "00 32 09 59 00 00 40 02 61 07 00 00 30 00 00 00 7f 01 00 20 01",
#     "00 32 09 59 00 00 40 02 7b 07 00 00 30 00 00 00 7f 01 00 50 0f",
# ]

# # Convierte string a lista de enteros
# def parse_message(msg):
#     return [int(b, 16) for b in msg.split()]

# # Extrae el checksum real de b4 y b5
# def extract_checksum(b4, b5):
#     high = (b4 >> 3) & 0x0F
#     low = b5 & 0x0F
#     return (high << 4) | low

# # Algoritmos de checksum a probar
# def checksum_sum(bytes_):
#     return sum(bytes_) & 0xFF

# def checksum_sum_mod128(bytes_):
#     return sum(bytes_) & 0x7F

# def checksum_xor(bytes_):
#     result = 0
#     for b in bytes_:
#         result ^= b
#     return result & 0xFF

# def checksum_xor_mod128(bytes_):
#     result = 0
#     for b in bytes_:
#         result ^= b
#     return result & 0x7F

# def checksum_complement_mod128(bytes_):
#     return (128 - (sum(bytes_) & 0x7F)) & 0x7F

# algorithms = {
#     "sum": checksum_sum,
#     "sum_mod128": checksum_sum_mod128,
#     "xor": checksum_xor,
#     "xor_mod128": checksum_xor_mod128,
#     "complement_mod128": checksum_complement_mod128,
# }

# # Probar algoritmos
# for msg_str in messages:
#     msg = parse_message(msg_str)
#     b4, b5 = msg[-2], msg[-1]
#     # Poner a 0 los 5 bits más significativos de b4
#     b4_calc = b4 & 0x07
#     msg_for_checksum = msg[:-2] + [b4_calc, 0]
#     real_checksum = extract_checksum(b4, b5)

#     print(f"\nMensaje: {' '.join(f'{b:02X}' for b in msg)}")
#     print(f"Checksum real: {real_checksum:02X}")

#     for name, func in algorithms.items():
#         cs = func(msg_for_checksum)
#         print(f"{name:15s}: {cs:02X}")


# # -*- coding: utf-8 -*-
# from itertools import product

# # Tus mensajes SysEx (sin F0 y F7)
# messages = [
#     # RED, pads 1-8
#     "F0 00 32 09 59 00 00 40 02 45 06 00 00 30 00 00 00 7f 01 00 00 0b F7",
#     "F0 00 32 09 59 00 00 40 02 5f 06 00 00 30 00 00 00 7f 01 00 30 09 F7",
#     "F0 00 32 09 59 00 00 40 02 79 06 00 00 30 00 00 00 7f 01 00 60 07 F7",
#     "F0 00 32 09 59 00 00 40 02 13 07 00 00 30 00 00 00 7f 01 00 10 06 F7",
#     "F0 00 32 09 59 00 00 40 02 2d 07 00 00 30 00 00 00 7f 01 00 40 04 F7",
#     "F0 00 32 09 59 00 00 40 02 47 07 00 00 30 00 00 00 7f 01 00 70 02 F7",
#     "F0 00 32 09 59 00 00 40 02 61 07 00 00 30 00 00 00 7f 01 00 20 01 F7",
#     "F0 00 32 09 59 00 00 40 02 7b 07 00 00 30 00 00 00 7f 01 00 50 0f F7",
# ]

# def parse_message(msg):
#     return [int(b, 16) for b in msg.split()]

# def extract_checksum(b4, b5):
#     high = (b4 >> 3) & 0x0F
#     low = b5 & 0x0F
#     return (high << 4) | low

# def complement_mod16_checksum(bytes_):
#     total = sum(bytes_)
#     # checksum de 4 bits, complemento a 16
#     return (16 - (total % 16)) % 16

# for msg_str in messages:
#     msg = parse_message(msg_str)
#     b4, b5 = msg[-2], msg[-1]

#     # Poner a 0 los 5 bits más significativos de b4
#     b4_calc = b4 & 0x07
#     msg_for_checksum = msg[:-2] + [b4_calc, 0]

#     # Calcular checksum teórico
#     cs_nibble = complement_mod16_checksum(msg_for_checksum)
#     cs_high = cs_nibble
#     cs_low = cs_nibble

#     # Extraer checksum real
#     real_cs = extract_checksum(b4, b5)

#     print(f"\nMensaje: {' '.join(f'{b:02X}' for b in msg)}")
#     print(f"Checksum real: {real_cs:02X}")
#     print(f"Checksum teórico (4 bits): {cs_nibble:02X}")


# -*- coding: utf-8 -*-

# # Mensajes SysEx sin F0/F7
# messages = [
#     # RED, pads 1-8
#     "00 32 09 59 00 00 40 02 45 06 00 00 30 00 00 00 7f 01 00 00 0b",
#     "00 32 09 59 00 00 40 02 5f 06 00 00 30 00 00 00 7f 01 00 30 09",
#     "00 32 09 59 00 00 40 02 79 06 00 00 30 00 00 00 7f 01 00 60 07",
#     "00 32 09 59 00 00 40 02 13 07 00 00 30 00 00 00 7f 01 00 10 06",
#     "00 32 09 59 00 00 40 02 2d 07 00 00 30 00 00 00 7f 01 00 40 04",
#     "00 32 09 59 00 00 40 02 47 07 00 00 30 00 00 00 7f 01 00 70 02",
#     "00 32 09 59 00 00 40 02 61 07 00 00 30 00 00 00 7f 01 00 20 01",
#     "00 32 09 59 00 00 40 02 7b 07 00 00 30 00 00 00 7f 01 00 50 0f",
# ]

# def parse_message(msg):
#     return [int(b, 16) for b in msg.split()]

def extract_checksum(b1, b2):
    """Extrae el checksum real de los nibbles"""
    low = (b1 >> 3) & 0x0F
    high = b2 & 0x0F
    return (high << 4) | low

# def calculate_checksum(bytes_):
#     """Calcula complemento mod 16 sobre la suma de los bytes relevantes"""
#     total = sum(bytes_)
#     return (16 - (total % 16)) % 16

# for msg_str in messages:
#     msg = parse_message(msg_str)
#     b4, b5 = msg[-2], msg[-1]

#     # Poner a cero los bits del checksum antes de calcular
#     b4_calc = b4 & 0x07  # bits 0-2 conservados, bits 3-7 a 0
#     b5_calc = 0           # bits 0-3 a 0
#     msg_for_checksum = msg[:-2] + [b4_calc, b5_calc]

#     # Calcular checksum teórico
#     cs_nibble = calculate_checksum(msg_for_checksum)

#     # Extraer checksum real
#     real_cs = extract_checksum(b4, b5)

#     print(f"Mensaje: {' '.join(f'{b:02X}' for b in msg)}")
#     print(f"Checksum real: {real_cs:02X}, calculado: {cs_nibble:02X}\n")


messages = [
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 6F 5F 0A F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 6B 67 0A F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 67 6F 0A F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 63 77 0A F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 5F 7F 0A F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 5B 07 0B F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 57 0F 0B F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 53 17 0B F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 4F 1F 0B F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 4B 27 0B F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 47 2F 0B F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 43 37 0B F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 3F 3F 0B F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 3B 47 0B F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 37 4F 0B F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 33 57 0B F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 07 28 0A F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 33 50 09 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 03 34 02 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 7F 3B 02 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 03 34 02 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 7F 3B 02 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 7B 43 02 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 77 4B 02 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 73 53 02 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 6F 5B 02 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 6B 63 02 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 67 6B 02 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 63 73 02 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 1B 00 0A F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 03 32 06 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 7F 39 06 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 7B 41 06 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 0F 18 0A F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 03 31 08 F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 0F 18 0A F7",
    # "F0 00 32 09 59 00 00 40 02 53 00 00 00 30 00 00 00 7F 7F 7F 38 08 F7",
    # "F0 00 32 09 59 00 00 40 02 39 00 00 00 30 00 00 00 7F 7F 7F 0F 0C F7",
    # "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 7F 2B 7D 7F 09 F7",

    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 01 00 00 08 0F F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 02 00 00 00 0F F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 03 00 00 78 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 04 00 00 70 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 05 00 00 68 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 06 00 00 60 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 07 00 00 58 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 08 00 00 50 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 09 00 00 48 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 0A 00 00 40 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 0B 00 00 38 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 0C 00 00 30 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 0D 00 00 28 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 0E 00 00 20 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 0F 00 00 18 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 10 00 00 10 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 11 00 00 08 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 12 00 00 00 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 13 00 00 78 0D F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 14 00 00 70 0D F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 15 00 00 68 0D F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 16 00 00 60 0D F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 17 00 00 58 0D F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 18 00 00 50 0D F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 19 00 00 48 0D F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 1A 00 00 40 0D F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 1B 00 00 38 0D F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 1C 00 00 30 0D F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 1D 00 00 28 0D F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 1E 00 00 20 0D F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 1F 00 00 18 0D F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 20 00 00 10 0D F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 21 00 00 08 0D F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 22 00 00 00 0D F7",
    "",

    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 7F 7F 37 3F 00 F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 7F 7F 3B 37 00 F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 7F 7F 3F 2F 00 F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 7F 7F 43 27 00 F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 7F 7F 47 1F 00 F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 7F 7F 4B 17 00 F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 7F 7F 4F 0F 00 F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 7F 7F 53 07 00 F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 7F 7F 57 7F 0F F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 7F 7F 5B 77 0F F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 7F 7F 5F 6F 0F F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 7F 7F 63 67 0F F7",
    "",

    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 7F 7D 63 6F 0F F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 7E 7D 63 77 0F F7",
    "",

    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 00 00 10 0F F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 02 00 08 0F F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 04 00 00 0F F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 06 00 78 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 08 00 70 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 0A 00 68 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 0C 00 60 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 0E 00 58 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 10 00 50 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 12 00 48 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 14 00 40 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 16 00 38 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 18 00 30 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 1A 00 28 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 1C 00 20 0E F7",
    "F0 00 32 09 59 00 00 40 02 05 00 00 00 30 00 00 00 00 1E 00 18 0E F7",
    "",
]

# from functools import reduce
# from crc8 import crc8

# for m in messages:
#     if not m:
#         print(30 * "-")
#         continue

#     bs = list(bytes.fromhex(m))

#     expected = bs[-2] << 4 | bs[-3] >> 3

#     bs = bs[:-2]
#     bs[-1] &= 0b111

#     check_1 = reduce(lambda x, y: x ^ y, bs)

#     check_2 = sum(bs)
#     check_2 = (check_2 // 256) - (check_2 % 256)

#     check_3 = crc8()
#     check_3.update(bytes(bs))
#     check_3 = int(check_3.hexdigest(), 16)

#     print(expected, ":", check_1, check_2, check_3)


# Cambio de color a negro los pads de los bancos 1, 2, 3.., en orden
messages = [
    "F0  00 32 09 59 00 00 40 02  05 00  00 00 30 00 00 00 00 00 00  10 0F  F7",
    "F0  00 32 09 59 00 00 40 02  1F 00  00 00 30 00 00 00 00 00 00  40 0D  F7",
    "F0  00 32 09 59 00 00 40 02  39 00  00 00 30 00 00 00 00 00 00  70 0B  F7",
    "F0  00 32 09 59 00 00 40 02  53 00  00 00 30 00 00 00 00 00 00  20 0A  F7",
    "F0  00 32 09 59 00 00 40 02  6D 00  00 00 30 00 00 00 00 00 00  50 08  F7",
    "F0  00 32 09 59 00 00 40 02  07 01  00 00 30 00 00 00 00 00 00  00 07  F7",
    "F0  00 32 09 59 00 00 40 02  21 01  00 00 30 00 00 00 00 00 00  30 05  F7",
    "F0  00 32 09 59 00 00 40 02  3B 01  00 00 30 00 00 00 00 00 00  60 03  F7",
    "F0  00 32 09 59 00 00 40 02  55 01  00 00 30 00 00 00 00 00 00  10 02  F7",
    "F0  00 32 09 59 00 00 40 02  6F 01  00 00 30 00 00 00 00 00 00  40 00  F7",
    "F0  00 32 09 59 00 00 40 02  09 02  00 00 30 00 00 00 00 00 00  68 0E  F7",
    "F0  00 32 09 59 00 00 40 02  23 02  00 00 30 00 00 00 00 00 00  18 0D  F7",
    "F0  00 32 09 59 00 00 40 02  3D 02  00 00 30 00 00 00 00 00 00  48 0B  F7",
    "F0  00 32 09 59 00 00 40 02  57 02  00 00 30 00 00 00 00 00 00  78 09  F7",
    "F0  00 32 09 59 00 00 40 02  71 02  00 00 30 00 00 00 00 00 00  28 08  F7",
    "F0  00 32 09 59 00 00 40 02  0B 03  00 00 30 00 00 00 00 00 00  58 06  F7",
    "",
    "F0  00 32 09 59 00 00 40 02  25 03  00 00 30 00 00 00 00 00 00  08 05  F7",
    "F0  00 32 09 59 00 00 40 02  3F 03  00 00 30 00 00 00 00 00 00  38 03  F7",
    "F0  00 32 09 59 00 00 40 02  59 03  00 00 30 00 00 00 00 00 00  68 01  F7",
    "F0  00 32 09 59 00 00 40 02  73 03  00 00 30 00 00 00 00 00 00  18 00  F7",
    "F0  00 32 09 59 00 00 40 02  0D 04  00 00 30 00 00 00 00 00 00  40 0E  F7",
    "F0  00 32 09 59 00 00 40 02  27 04  00 00 30 00 00 00 00 00 00  70 0C  F7",
    "F0  00 32 09 59 00 00 40 02  41 04  00 00 30 00 00 00 00 00 00  20 0B  F7",
    "F0  00 32 09 59 00 00 40 02  5B 04  00 00 30 00 00 00 00 00 00  50 09  F7",
    "F0  00 32 09 59 00 00 40 02  75 04  00 00 30 00 00 00 00 00 00  00 08  F7",
    "F0  00 32 09 59 00 00 40 02  0F 05  00 00 30 00 00 00 00 00 00  30 06  F7",
    "F0  00 32 09 59 00 00 40 02  29 05  00 00 30 00 00 00 00 00 00  60 04  F7",
    "F0  00 32 09 59 00 00 40 02  43 05  00 00 30 00 00 00 00 00 00  10 03  F7",
    "F0  00 32 09 59 00 00 40 02  5D 05  00 00 30 00 00 00 00 00 00  40 01  F7",
    "F0  00 32 09 59 00 00 40 02  77 05  00 00 30 00 00 00 00 00 00  70 0F  F7",
    "F0  00 32 09 59 00 00 40 02  11 06  00 00 30 00 00 00 00 00 00  18 0E  F7",
    "F0  00 32 09 59 00 00 40 02  2B 06  00 00 30 00 00 00 00 00 00  48 0C  F7",
    "",
    "F0  00 32 09 59 00 00 40 02  45 06  00 00 30 00 00 00 00 00 00  78 0A  F7",
    "F0  00 32 09 59 00 00 40 02  5F 06  00 00 30 00 00 00 00 00 00  28 09  F7",
    "F0  00 32 09 59 00 00 40 02  79 06  00 00 30 00 00 00 00 00 00  58 07  F7",
    "F0  00 32 09 59 00 00 40 02  13 07  00 00 30 00 00 00 00 00 00  08 06  F7",
    "F0  00 32 09 59 00 00 40 02  2D 07  00 00 30 00 00 00 00 00 00  38 04  F7",
    "F0  00 32 09 59 00 00 40 02  47 07  00 00 30 00 00 00 00 00 00  68 02  F7",
    "F0  00 32 09 59 00 00 40 02  61 07  00 00 30 00 00 00 00 00 00  18 01  F7",
    "F0  00 32 09 59 00 00 40 02  7B 07  00 00 30 00 00 00 00 00 00  48 0F  F7",
    "F0  00 32 09 59 00 00 40 02  15 08  00 00 30 00 00 00 00 00 00  70 0D  F7",
    "F0  00 32 09 59 00 00 40 02  2F 08  00 00 30 00 00 00 00 00 00  20 0C  F7",
    "F0  00 32 09 59 00 00 40 02  49 08  00 00 30 00 00 00 00 00 00  50 0A  F7",
    "F0  00 32 09 59 00 00 40 02  63 08  00 00 30 00 00 00 00 00 00  00 09  F7",
    "F0  00 32 09 59 00 00 40 02  7D 08  00 00 30 00 00 00 00 00 00  30 07  F7",
    "F0  00 32 09 59 00 00 40 02  17 09  00 00 30 00 00 00 00 00 00  60 05  F7",
    "F0  00 32 09 59 00 00 40 02  31 09  00 00 30 00 00 00 00 00 00  10 04  F7",
    "F0  00 32 09 59 00 00 40 02  4B 09  00 00 30 00 00 00 00 00 00  40 02  F7",
    "",
    "F0  00 32 09 59 00 00 40 02  65 09  00 00 30 00 00 00 00 00 00  70 00  F7",
    "F0  00 32 09 59 00 00 40 02  7F 09  00 00 30 00 00 00 00 00 00  20 0F  F7",
    "F0  00 32 09 59 00 00 40 02  19 0A  00 00 30 00 00 00 00 00 00  48 0D  F7",
    "F0  00 32 09 59 00 00 40 02  33 0A  00 00 30 00 00 00 00 00 00  78 0B  F7",
    "F0  00 32 09 59 00 00 40 02  4D 0A  00 00 30 00 00 00 00 00 00  28 0A  F7",
    "F0  00 32 09 59 00 00 40 02  67 0A  00 00 30 00 00 00 00 00 00  58 08  F7",
    "F0  00 32 09 59 00 00 40 02  01 0B  00 00 30 00 00 00 00 00 00  08 07  F7",
    "F0  00 32 09 59 00 00 40 02  1B 0B  00 00 30 00 00 00 00 00 00  38 05  F7",
    "F0  00 32 09 59 00 00 40 02  35 0B  00 00 30 00 00 00 00 00 00  68 03  F7",
    "F0  00 32 09 59 00 00 40 02  4F 0B  00 00 30 00 00 00 00 00 00  18 02  F7",
    "F0  00 32 09 59 00 00 40 02  69 0B  00 00 30 00 00 00 00 00 00  48 00  F7",
    "F0  00 32 09 59 00 00 40 02  03 0C  00 00 30 00 00 00 00 00 00  70 0E  F7",
    "F0  00 32 09 59 00 00 40 02  1D 0C  00 00 30 00 00 00 00 00 00  20 0D  F7",
    "F0  00 32 09 59 00 00 40 02  37 0C  00 00 30 00 00 00 00 00 00  50 0B  F7",
    "F0  00 32 09 59 00 00 40 02  51 0C  00 00 30 00 00 00 00 00 00  00 0A  F7",
    "F0  00 32 09 59 00 00 40 02  6B 0C  00 00 30 00 00 00 00 00 00  30 08  F7",
    "",
    "",
    "F0  00 32 09 49 00 00 40 02  02 00  00 00 10 00 00 00 01        6C 03  F7",
    "F0  00 32 09 49 00 00 40 02  1C 00  00 00 10 00 00 00 01        38 03  F7",
    "F0  00 32 09 49 00 00 40 02  36 00  00 00 10 00 00 00 01        04 03  F7",
    "F0  00 32 09 49 00 00 40 02  50 00  00 00 10 00 00 00 01        50 02  F7",
    "F0  00 32 09 49 00 00 40 02  6A 00  00 00 10 00 00 00 07        10 02  F7",
    "F0  00 32 09 49 00 00 40 02  04 01  00 00 10 00 00 00 08        5A 01  F7",
    "F0  00 32 09 49 00 00 40 02  1E 01  00 00 10 00 00 00 09        24 01  F7",
    "F0  00 32 09 49 00 00 40 02  38 01  00 00 10 00 00 00 0A        6E 00  F7",
    "F0  00 32 09 49 00 00 40 02  52 01  00 00 10 00 00 00 0B        38 00  F7",
    "F0  00 32 09 49 00 00 40 02  6C 01  00 00 10 00 00 00 0C        02 00  F7",
    "F0  00 32 09 49 00 00 40 02  06 02  00 00 10 00 00 00 0D        4A 03  F7",
    "F0  00 32 09 49 00 00 40 02  20 02  00 00 10 00 00 00 0E        14 03  F7",
    "F0  00 32 09 49 00 00 40 02  3A 02  00 00 10 00 00 00 0F        5E 02  F7",
    "F0  00 32 09 49 00 00 40 02  54 02  00 00 10 00 00 00 10        28 02  F7",
    "F0  00 32 09 49 00 00 40 02  6E 02  00 00 10 00 00 00 11        72 01  F7",
    "F0  00 32 09 49 00 00 40 02  08 03  00 00 10 00 00 00 12        3C 01  F7",
]


class Device:
    CMD_SET_LED = 0x59

    def __init__(self, address: str = [0x00, 0x32, 0x09]):
        self._address = address
        self._dev = mido.open_output(MIDI_OUT_PORT)

    def set_color(self, pad: int, color: tuple, bank: int = 0):
        """DEVID[3] CMD[1] 00 00 40 02 ADDR[2] 00 00 30 00 00 00 R[1] G[1] B+CRC[1] CRC[1]"""

        cmd: list = self._address[:]
        cmd += [self.CMD_SET_LED, 0, 0, 0x40, 0x02]
        cmd += self._get_pad_addr(bank, pad)
        cmd += [0, 0, 0x30, 0, 0, 0]
        cmd += self._pack_bytes(bytes(color))

        pad_no = 5 + (bank * 16 + pad) * 26
        checksum = self._get_checksum([pad_no] + list(color))
        cs_bytes = self._pack_bytes(checksum.to_bytes(1, "little"), 3)
        cmd[-1] |= cs_bytes[0]
        cmd.append(cs_bytes[1])

        # t = [f"{b:02X} " for b in cmd]
        # t.insert(3, " ")
        # t.insert(5, " ")
        # t.insert(10, " ")
        # t.insert(13, " ")
        # t.insert(20, " ")
        # t.insert(24, " ")
        # print(" ?:", "".join(t))
        # return cmd

        msg = mido.Message('sysex', data=cmd)
        self._dev.send(msg)

    def _get_pad_addr(self, bank: int, pad: int, offset: int = 5):
        n_pad = bank * 16 + pad
        b1 = offset + (n_pad * 26) % 0x80
        b2 = n_pad // 5
        return [b1, b2]

    def _get_checksum(self, data: bytes):
        magic = 0xF7
        ds = 0
        for x in data:
            y = x
            while y > 0:
                ds += (y & 0xFF)
                y >>= 8
        cs = (magic - (ds & 0xFF)) & 0xFF
        # print("sum:", ds, "cs:", cs, "data:", data)

        return cs

    def _pack_bytes(self, data: bytes, bit_offset: int = 0):
        retval = [0]
        for b in data:
            retval[-1] |= (b << bit_offset) & 0x7F
            retval.append(b >> (7 - bit_offset))
            bit_offset += 1
            if bit_offset > 6:
                bit_offset = 0

        return bytes(retval)


# F0  00 32 09 59 00 00 40 02  05 00  00 00 30 00 00 00  00 00 00  10 0F  F7
# F0  00 32 09 59 00 00 40 02  05 00  00 00 30 00 00 00  01 00 00  08 0F  F7
# F0  00 32 09 59 00 00 40 02  05 00  00 00 30 00 00 00  02 00 00  00 0F  F7

# F0  00 32 09 59 00 00 40 02  1F 00  00 00 30 00 00 00  00 00 00  40 0D  F7
# F0  00 32 09 59 00 00 40 02  1F 00  00 00 30 00 00 00  01 00 00  38 0D  F7
# F0  00 32 09 59 00 00 40 02  1F 00  00 00 30 00 00 00  02 00 00  30 0D  F7

# F0  00 32 09 59 00 00 40 02  55 01  00 00 30 00 00 00  00 00 00  10 02  F7
# F0  00 32 09 59 00 00 40 02  6F 01  00 00 30 00 00 00  00 00 00  40 00  F7
# F0  00 32 09 59 00 00 40 02  09 02  00 00 30 00 00 00  00 00 00  68 0E  F7

dev = Device()

# print("\n01: 00 32 09  59  00 00 40 02  05 00  00 00 30 00 00 00  00 00 00  10 0F")
# dev.set_color(0, (255, 255, 255))
dev.set_color(2, (255, 255, 255), bank=1)

# print("\n02: 00 32 09  59  00 00 40 02  05 00  00 00 30 00 00 00  01 00 00  08 0F")
# dev.set_color(0, (1, 0, 0))

# print("\n04: 00 32 09  59  00 00 40 02  05 00  00 00 30 00 00 00  7E 01 00  20 0F")
# dev.set_color(0, (254, 0, 0))

# print("\n03: 00 32 09  59  00 00 40 02  05 00  00 00 30 00 00 00  7F 01 00  18 0F")
# dev.set_color(0, (255, 0, 0))

# print("\n04: 00 32 09  59  00 00 40 02  05 00  00 00 30 00 00 00  7F 7F 03  20 0F")
# dev.set_color(0, (255, 255, 0))

# print("\n05: 00 32 09  59  00 00 40 02  0D 04  00 00 30 00 00 00  00 00 00  40 0E")
# dev.set_color(4, (0, 0, 0), bank=1)

# print("\n06: 00 32 09  59  00 00 40 02  45 06  00 00 30 00 00 00  00 00 00  78 0A")
# dev.set_color(0, (0, 0, 0), bank=2)

# print("\n07: 00 32 09  59  00 00 40 02  45 06  00 00 30 00 00 00  7F 01 00  00 0B")
# dev.set_color(0, (255, 0, 0), bank=2)

# print("\n08: 00 32 09  59  00 00 40 02  05 00  00 00 30 00 00 00  7F 00 00  18 07")
# dev.set_color(0, (127, 0, 0))

# print("\n08: 00 32 09  59  00 00 40 02  05 00  00 00 30 00 00 00  00 01 00  10 07")
# dev.set_color(0, (128, 0, 0))

# print("\n09: 00 32 09  59  00 00 40 02  05 00  00 00 30 00 00 00  01 01 00  08 07")
# dev.set_color(0, (129, 0, 0))

# print("\n09: 00 32 09  59  00 00 40 02  05 00  00 00 30 00 00 00  2F 01 00  18 04")
# dev.set_color(0, (175, 0, 0))

# print("\n10: 00 32 09  59  00 00 40 02  05 00  00 00 30 00 00 00  7A 01 00  40 0F")
# dev.set_color(0, (250, 0, 0))

# print("\n11: 00 32 09  59  00 00 40 02  05 00  00 00 30 00 00 00  76 01 00  60 0F")
# dev.set_color(0, (246, 0, 0))

# print("\n11: 00 32 09  59  00 00 40 02  05 00  00 00 30 00 00 00  77 01 00  58 0F")
# dev.set_color(0, (247, 0, 0))

# print("\n11: 00 32 09  59  00 00 40 02  05 00  00 00 30 00 00 00  78 01 00  50 0F")
# dev.set_color(0, (248, 0, 0))

# def check_sum(pad, color, cs, bank=0):
#     dev.set_color(pad, color, bank=bank)
#     cs_int = extract_checksum(*bytes.fromhex(cs))
#     print(f">>> expected cs: {cs_int} - {cs}\n")


# check_sum(0,  (0, 0, 0),    "10 0F")
# check_sum(0,  (1, 0, 0),    "08 0F")
# check_sum(0,  (2, 0, 0),    "00 0F")
# check_sum(1,  (0, 0, 0),    "40 0D")
# check_sum(1,  (1, 0, 0),    "38 0D")
# check_sum(1,  (2, 0, 0),    "30 0D")
# check_sum(8,  (0, 0, 0),    "10 02")
# check_sum(9,  (0, 0, 0),    "40 00")

# print("--")
# check_sum(10, (1, 0, 0),    "60 0E")
# check_sum(10, (0, 0, 0),    "68 0E")
# check_sum(0,  (255, 5, 0),  "70 0E")
# print("--")

# check_sum(11, (0, 0, 0),    "18 0D")
# check_sum(15, (0, 0, 0),    "58 06")
# check_sum(0,  (175, 0, 0),  "18 04")

# check_sum(0,  (247, 0, 0),  "58 0F")
# check_sum(0,  (248, 0, 0),  "50 0F")

# check_sum(0,  (250, 0, 0),  "40 0F")
# check_sum(0,  (254, 0, 0),  "20 0F")


# pad = 0
# for i in range(20):
#     m = messages[i]
#     if not m:
#         continue
#     csb = m[-9:-4]
#     print(pad, "=>", m)
#     print(extract_checksum(*bytes.fromhex(csb)), csb.split())
#     dev.set_color(pad, (0, 0, 0))
#     print("-----")
#     pad += 1


# class Message:
#     CMD_SET_LED = "59"

#     def __init__(self, address="00 32 09"):
#         self._addr = address
#         self._cmd = self.CMD_SET_LED
#         self._pad = self._get_pad_bytes(0, 0)
#         self._size = "30"
#         self._args = ""

#     def __repr__(self):
#         retval = f"{self._addr} {self._cmd} 00 00 00 40 02"
#         retval += f" {self._pad} 00 00"
#         retval += f" {self._size} 00 00 00"
#         retval += f" {self._args}"
#         retval += f" {self._checksum}"
#         return retval

#     def _get_pad_bytes(self, bank, pad, offset=5):
#         n_pad = bank * 16 + pad
#         b1 = offset + (n_pad * 26) % 0x80
#         b2 = n_pad // 5
#         return f"{b1} {b2}"


# def pad_addr(bank, pad, offset=5):
#     n_pad = bank * 16 + pad
#     b1 = offset + (n_pad * 26) % 0x80
#     b2 = n_pad // 5
#     return b1, b2

# breaks = 0
# for i, m in enumerate(messages):
#     if not m:
#         print(30 * "-")
#         breaks += 1
#         continue

#     idx = i - breaks
#     bank = idx // 16
#     pad = idx % 16

#     bs = list(bytes.fromhex(m))
#     addr1, addr2 = bs[9:11]
#     b1, b2 = pad_addr(bank, pad)
#     print(f"{idx:02}: {addr1:02X} {addr2:02X} | {addr1:08b} {addr2:08b} | {b1:02X} {b2:02X}")



# 05 00 | 0 00 0010 1 00000000 | 02 - 00000
# 1F 00 | 0 00 1111 1 00000000 | 0F - 00000
# 39 00 | 0 01 1100 1 00000000 | 1C - 00001
# 53 00 | 0 10 1001 1 00000000 | 29 - 00010

# 6D 00 | 0 11 0110 1 00000000 | 36 - 00011
# 07 01 | 0 00 0011 1 00000001 | 03 - 00100
# 21 01 | 0 01 0000 1 00000001 | 10 - 00101
# 3B 01 | 0 01 1101 1 00000001 | 1D - 00101

# 55 01 | 0 10 1010 1 00000001 | 2A - 00110
# 6F 01 | 0 11 0111 1 00000001 | 37 - 00111
# 09 02 | 0 00 0100 1 00000010 | 04 - 01000
# 23 02 | 0 01 0001 1 00000010 | 11 - 01001

# 3D 02 | 0 01 1110 1 00000010 | 1E - 01001
# 57 02 | 0 10 1011 1 00000010 | 2B - 01010
# 71 02 | 0 11 1000 1 00000010 | 38 - 01011
# 0B 03 | 0 00 0101 1 00000011 | 05 - 01100
# --------- ---- -----------------
# 25 03 | 0 01 0010 1 00000011 | 12 - 01101
# 3F 03 | 0 01 1111 1 00000011 | 1F - 01101
# 59 03 | 0 10 1100 1 00000011 | 2C - 01110
# 73 03 | 0 11 1001 1 00000011 | 39 - 01111

# 0D 04 | 0 00 0110 1 00000100 | 06 - 10000
# 27 04 | 0 01 0011 1 00000100 | 13 - 10001
# 41 04 | 0 10 0000 1 00000100 | 20 - 10010
# 5B 04 | 0 10 1101 1 00000100 | 2D - 10010

# 75 04 | 0 11 1010 1 00000100 | 3A - 10011
# 0F 05 | 0 00 0111 1 00000101 | 07 - 10100
# 29 05 | 0 01 0100 1 00000101 | 14 - 10101
# 43 05 | 0 10 0001 1 00000101 | 21 - 10110

# 5D 05 | 0 10 1110 1 00000101 | 2E - 10110
# 77 05 | 0 11 1011 1 00000101 | 3B - 10111
# 11 06 | 0 00 1000 1 00000110 | 08 - 11000
# 2B 06 | 0 01 0101 1 00000110 | 15 - 11001
# --------- -- ---- - --------------
# 45 06 | 0 10 0010 1 00000110 | 22
# 5F 06 | 0 10 1111 1 00000110 | 2F
# 79 06 | 0 11 1100 1 00000110 | 3C
# 13 07 | 0 00 1001 1 00000111 | 09

# 2D 07 | 0 01 0110 1 00000111 | 16
# 47 07 | 0 10 0011 1 00000111 | 23
# 61 07 | 0 11 0000 1 00000111 | 30
# 7B 07 | 0 11 1101 1 00000111 | 3D

# 15 08 | 0 00 1010 1 00001000 | 0A
# 2F 08 | 0 01 0111 1 00001000 | 17
# 49 08 | 0 10 0100 1 00001000 | 24
# 63 08 | 0 11 0001 1 00001000 | 31

# 7D 08 | 0 11 1110 1 00001000 | 3E
# 17 09 | 0 00 1011 1 00001001 | 0B
# 31 09 | 0 01 1000 1 00001001 | 18
# 4B 09 | 0 10 0101 1 00001001 | 25
# --------- -- ---- - --------------
# 65 09 | 0 11 0010 1 00001001 | 32
# 7F 09 | 0 11 1111 1 00001001 | 3F
# 19 0A | 0 00 1100 1 00001010 | 0C
# 33 0A | 0 01 1001 1 00001010 | 19

# 4D 0A | 0 10 0110 1 00001010 | 26
# 67 0A | 0 11 0011 1 00001010 | 33
# 01 0B | 0 00 0000 1 00001011 | 00
# 1B 0B | 0 00 1101 1 00001011 | 0D

# 35 0B | 0 01 1010 1 00001011 | 1A
# 4F 0B | 0 10 0111 1 00001011 | 27
# 69 0B | 0 11 0100 1 00001011 | 34
# 03 0C | 0 00 0001 1 00001100 | 01

# 1D 0C | 0 00 1110 1 00001100 | 0E
# 37 0C | 0 01 1011 1 00001100 | 1B
# 51 0C | 0 10 1000 1 00001100 | 28
# 6B 0C | 0 11 0101 1 00001100 | 35
