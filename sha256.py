import struct 
import bitwise_tools

def pad_message(message_bytes):
    # padding .. .. .. .. é um padding

    original_length_bits = len(message_bytes) * 8
    padded_message = bytearray(message_bytes)

    # adiciona o bit 1
    padded_message.append(0x80)

    # adiciona 0x00 até 56 bytes
    while len(padded_message) % 64 != 56:
        padded_message.append(0x00)

    padded_message += struct.pack('>Q', original_length_bits)

    return padded_message

def sha256(message_bytes):
    padded_message = pad_message(message_bytes)

    H = list(bitwise_tools.H_INICIAIS)

    #processa cada bloco de 64 bites
    for i in range(0, len(padded_message), 64):
        chunk = padded_message[i:i+64]

        W = [0] * 64
        chunk_words = struct.unpack('>16I', chunk)
        for j in range(16):
            W[j] = chunk_words[j]

        for j in range(16, 64):
            W[j] = bitwise_tools.add_mod32(bitwise_tools.sigma1(W[j-2]), W[j-7], bitwise_tools.sigma0(W[j-15]), W[j-16])

        #Compressão, incializa as variáveis com o estado atual de H
        a, b, c, d, e, f, g, h = H

        #Executa as 64 rodadas
        for j in range(64):
            T1 = bitwise_tools.add_mod32(h, bitwise_tools.SIGMA1(e), bitwise_tools.ch(e, f, g), bitwise_tools.K[j], W[j])

            T2 = bitwise_tools.add_mod32(bitwise_tools.SIGMA0(a), bitwise_tools.maj(a, b, c))

            h = g
            g = f
            f = e
            e = bitwise_tools.add_mod32(d, T1)
            d = c
            c = b
            b = a
            a = bitwise_tools.add_mod32(T1, T2)

        H[0] = bitwise_tools.add_mod32(H[0], a)        
        H[1] = bitwise_tools.add_mod32(H[1], b)        
        H[2] = bitwise_tools.add_mod32(H[2], c)        
        H[3] = bitwise_tools.add_mod32(H[3], d)        
        H[4] = bitwise_tools.add_mod32(H[4], e)        
        H[5] = bitwise_tools.add_mod32(H[5], f)        
        H[6] = bitwise_tools.add_mod32(H[6], g)        
        H[7] = bitwise_tools.add_mod32(H[7], h)    

    #Geração de hash final---
    hash_final = ''.join(f'{value:08x}' for value in H)

    return hash_final

# bloco teste
if __name__ == '__main__':
    msg = b"aba"
    resultado = sha256(msg)
        
    print(f"Mensagem de Entrada: '{msg.decode()}'")
    print(f"Hash Gerado:  {resultado}")
