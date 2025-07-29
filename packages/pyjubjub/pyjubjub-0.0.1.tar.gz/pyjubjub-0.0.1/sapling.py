# Copyright (c) 2025 Duke Leto

# sapling is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

#from basicswap.util.address import bech32Encode, bech32Decode
import bech32
import os

class SaplingAddress:
    def __init__(self, diversifier, pubkey):
        self.diversifier = diversifier
        self.pubkey = pubkey
        self.hrp = "zs"
        self.encoder = bech32.bech32_encode
        self.decoder = bech32.decode
        if len(self.diversifier) != 11:
            raise ValueError("diversifier must be exactly 11 bytes")
        if len(self.pubkey) != 32:
            raise ValueError("pubkey must be exactly 32 bytes")

    def encode(self):
        #return self.encoder(self.hrp, self.diversifier + self.pubkey)
        #return self.encoder(self.hrp, 0, b''.join([self.diversifier, self.pubkey]) )
        return self.encoder(self.hrp, bech32.convertbits( b''.join([self.diversifier,self.pubkey]) , 8, 5))

    def decode(self, bech):
        return self.decoder(bech)

def test():
    diversifier = os.urandom(11)
    pubkey = os.urandom(32)

    address = SaplingAddress(diversifier,pubkey)

    #print(diversifier)
    #print(pubkey)
    print("address=", address.encode())

if __name__ == "__main__":
    test()

