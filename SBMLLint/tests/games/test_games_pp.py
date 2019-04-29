"""
Test for GAMES Plus (Reduced) Row Echelon Form (GAMES_PP)
"""
from SBMLLint.common import constants as cn
from SBMLLint.common.reaction import Reaction
from SBMLLint.common.simple_sbml import SimpleSBML
from SBMLLint.games.games_pp import SOMStoichiometry, SOMReaction, GAMES_PP
from SBMLLint.games.som import SOM
from SBMLLint.common import simple_sbml

import numpy as np
import os
import re
import tesbml
import unittest

IGNORE_TEST = False
# Molecule names
PGA = "PGA"
RUBP = "RuBP"
# Reaction names
PGA_CONS = "PGA_cons"
PGA_CONS_SOMREACTION_IDENTIFIER = "PGA_cons: {PGA} -> {RuBP}"
PGA_PROD_VC = "PGA_prod_Vc"
# SOMStoichiometry identifier
RUBP_ONE = "{RuBP} * 1.00"



#############################
# Tests
#############################
class TestSOMStoichiometry(unittest.TestCase):

  def setUp(self):
    self.simple = SimpleSBML()
    self.simple.initialize(cn.TEST_FILE_GAMES_PP1)
    self.reaction = self.simple.getReaction(PGA_CONS)
    self.rubp = self.reaction.products[0]
    self.rubl_ss = SOMStoichiometry(
        som = SOM([self.rubp.molecule]),
        stoichiometry = self.rubp.stoichiometry
        )

  def testConstructor(self):
    if IGNORE_TEST:
      return
    self.assertTrue(isinstance(self.rubl_ss, SOMStoichiometry))
    self.assertTrue(isinstance(self.rubl_ss.som, SOM))
    self.assertTrue(isinstance(self.rubl_ss.stoichiometry, float))

  def testMakeId(self):
  	self.assertEqual(self.rubl_ss.identifier, RUBP_ONE)


class TestSOMReaction(unittest.TestCase):

  def setUp(self):
    self.simple = SimpleSBML()
    self.simple.initialize(cn.TEST_FILE_GAMES_PP1)
    self.reaction = self.simple.getReaction(PGA_CONS)
    self.pga = self.reaction.reactants[0]
    self.pga_ss = SOMStoichiometry(
        som = SOM([self.pga.molecule]),
        stoichiometry = self.pga.stoichiometry
        )
    self.rubp = self.reaction.products[0]
    self.rubp_ss = SOMStoichiometry(
        som = SOM([self.rubp.molecule]),
        stoichiometry = self.rubp.stoichiometry
        )
    self.som_reaction = SOMReaction(
        reactants=[self.pga_ss],
        products=[self.rubp_ss],
        label=self.reaction.label)

  def testConstructor(self):
    self.assertTrue(isinstance(self.reaction, Reaction))
    self.assertEqual(self.pga.molecule.name, PGA)
    self.assertEqual(self.rubp.molecule.name, RUBP)    
    self.assertTrue(isinstance(self.pga_ss, SOMStoichiometry))
    self.assertTrue(isinstance(self.rubp_ss, SOMStoichiometry))
    self.assertTrue(isinstance(self.som_reaction, SOMReaction))      

  def testMakeId(self):
  	self.assertEqual(
  	    self.som_reaction.makeId(),
  	    PGA_CONS_SOMREACTION_IDENTIFIER
  	    )

  def testGetCategory(self):
  	self.assertEqual(
  	    self.som_reaction.category,
  	    cn.REACTION_1_1)



if __name__ == '__main__':
  unittest.main()