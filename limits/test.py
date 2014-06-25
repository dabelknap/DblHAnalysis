import unittest
from datacard import Datacard


_TEST1 = (
'''#test_card
imax  1 number of channels
jmax  3 number of backgrounds
kmax  5 number of nuisance parameters
------------
bin 1
observation 1
------------
bin                  1        1        1        1    
process             ggH     qqWW     ggWW    others  
process              0        1        2        3    
rate               1.47     0.63     0.06     0.22   
------------
lumi        lnN    1.11       -      1.11       -    
xs_ggH      lnN    1.16       -        -        -    
WW_norm     gmN 4    -      0.16       -        -    
xs_ggWW     lnN      -        -       1.5       -    
bg_others   lnN      -        -        -       1.3   
''')


class TestDatacard(unittest.TestCase):

    def setUp(self):
        self.datacard = Datacard("test_card")
        self.datacard.set_observed(1)

    def test_add_sig(self):
        self.datacard.add_sig("ggH", 1.47)
        self.assertEqual(self.datacard.signal, ("ggH",1.47))

    def test_add_bkg1(self):
        self.datacard.add_bkg("qqWW", 0.63)
        self.assertEqual(self.datacard.bkg, [("qqWW", 0.63)])

    def test_add_bkg2(self):
        self.datacard.add_bkg("qqWW", 0.63)
        self.datacard.add_bkg("ggWW", 0.06)
        self.datacard.add_bkg("others", 0.22)
        self.assertEqual(self.datacard.bkg, [("qqWW", 0.63), ("ggWW", 0.06), ("others", 0.22)])

    def test_full(self):
        self.datacard.add_sig("ggH", 1.47)
        self.datacard.add_bkg("qqWW", 0.63)
        self.datacard.add_bkg("ggWW", 0.06)
        self.datacard.add_bkg("others", 0.22)

        self.datacard.add_syst("lumi", "lnN", ggH=1.11, ggWW=1.11)
        self.datacard.add_syst("xs_ggH", "lnN", ggH=1.16)
        self.datacard.add_syst("WW_norm", "gmN 4", qqWW=0.16)
        self.datacard.add_syst("xs_ggWW", "lnN", ggWW=1.50)
        self.datacard.add_syst("bg_others", "lnN", others=1.30)

        self.assertEqual(self.datacard.dump(), _TEST1)


if __name__ == "__main__":
    unittest.main()
