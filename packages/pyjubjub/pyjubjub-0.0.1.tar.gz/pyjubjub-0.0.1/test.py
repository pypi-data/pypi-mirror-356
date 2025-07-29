import unittest
import pyjubjub
from pyjubjub import *

class TestJubjub(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setting up test data...")
        # calling into Rust and getting the data back is slow, so
        # reusing data across tests makes the tests run faster
        cls.privkey1 = new_privkey()
        cls.privkey2 = new_privkey()
        cls.pubkey1  = get_pubkey(cls.privkey1)
        cls.pubkey2  = get_pubkey(cls.privkey2)
        cls.sig1     = sign(cls.privkey1, "Jabberwocky")
        cls.sig2     = sign(cls.privkey1, "Jabberwocky2")

    def test_privkey(self):
        # privkeys are a list of 32 unsigned 8bit bytes (u8 in Rust)
        self.assertEqual( len(self.privkey1), 32 )
        self.assertEqual( len(self.privkey2), 32 )

    def test_pubkey(self):
        # pubkeys are a list of 32 unsigned 8bit bytes (u8 in Rust)
        self.assertEqual( len(self.pubkey1), 32 )
        self.assertEqual( len(self.pubkey2), 32 )

    def test_sum_pubkeys(self):
        pubkey3 = sum_pubkeys(self.pubkey1, self.pubkey2)
        pubkey4 = sum_pubkeys(self.pubkey2, self.pubkey1)
        # a+b=b+a so pubkey3==pubkey4
        self.assertEqual( pubkey3, pubkey4)

    def test_sign(self):
        # signatures are 64 bytes
        self.assertEqual( len(self.sig1) , 64)
        self.assertEqual( len(self.sig2) , 64)
        # signing different data with the same privkey should produce a
        # different signature
        self.assertNotEqual( self.sig1, self.sig2 )

    def test_verify(self):
        # verifying the correct msg should be true
        valid = verify(self.pubkey1, "Jabberwocky", self.sig1)
        self.assertTrue( valid )
        # verifying the wrong msg should be false
        invalid = verify(self.pubkey1, "Snark", self.sig1)
        self.assertFalse( invalid )

    def test_is_on_curve(self):
        # all pubkeys must be on the elliptic curve
        self.assertTrue( is_on_curve(self.pubkey1) )
        self.assertTrue( is_on_curve(self.pubkey2) )
        pubkey3 = sum_pubkeys(self.pubkey1, self.pubkey2)
        pubkey4 = sum_pubkeys(self.pubkey2, self.pubkey1)
        # adding pubkeys generates another valid pubkey which must be on the
        # elliptic curve
        self.assertTrue( is_on_curve(pubkey3) )
        self.assertTrue( is_on_curve(pubkey4) )

        # invalid pubkeys are not on the elliptic curve
        invalid_pubkey = [1] * 32
        self.assertFalse( is_on_curve(invalid_pubkey) )

        invalid_pubkey = [2] * 32
        self.assertFalse( is_on_curve(invalid_pubkey) )


if __name__ == '__main__':
    unittest.main(verbosity=2)
