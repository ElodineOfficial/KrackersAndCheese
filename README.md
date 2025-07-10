# KrackersAndCheese
A kryptos scanner that proves how Sanborn originally intended K1 and K2 to be solved, includes an extended english crib list and K3-K4 for future crib scanning. Only K1 and K2 verified currently. Additional possible cribs have been added, but only further verified the initial solution methods for K1 and K2. Full details below.

How to solve:

Gather Clue From Morse Code + Kryptos tableau key:
E E VIRTUALLY E | E E E E E E INVISIBLE
Extract phrase 'AllyInvisible'
KRYPTOS key from tableau

The technical part:
You slide your crib along the ciphertext. For each position, for every pair of crib/ciphertext letters, you look up both letters in your Kryptos-alphabet, find the difference (mod 26), and use that as an index back into your alphabet to recover a key letter. You write out the sequence of these key letters, then look for the shortest repeat that covers the sequence. That’s the passcode needed at that spot. Repeat for each position.

Alphabet: ABCDEFGHIJKLMNOPQRSTUVWXYZ
Primary Key: KRYPTOS

Crib for K1 [best match]: ALLYINVISIBLE
K1: EMUFPHZLRFAXYUSDJKZLDKRNSHGNFIVJ YQTQUXQBQVYUVLLTREVJYQTMKYRDMFD
Output: ABSCISSA
Offset: 8

Crib for K2 [best match]:
K2: ANDTHEABSENCE
Output: PALIMPSEST
Offset: 20

Other solves using this same method getting the same keys using different cribs:

-- Crib: SUBTLESHADING --
Offset  Pattern        Key run
------  -------------  -------------------
    7   ESTPALIMPS    ESTPALIMPSEST

-- Crib: EXACTLOCATION --
Offset  Pattern        Key run
------  -------------  -------------------
  212   SCISSAAB      SCISSAABSCISS

-- Crib: MAGNETICFIELD --
Offset  Pattern        Key run
------  -------------  -------------------
   55   SAABSCIS      SAABSCISSAABS

-- Crib: UNDERGRUUNDTO --
Offset  Pattern        Key run
------  -------------  -------------------
  108   CISSAABS      CISSAABSCISSA
  
  -- Crib: INVISIBLEHOWS --
Offset  Pattern        Key run
------  -------------  -------------------
   12   ISSAABSC      ISSAABSCISSAA

-- Crib: USEDTHEEARTHS --
Offset  Pattern        Key run
------  -------------  -------------------
   42   BSCISSAA      BSCISSAABSCIS

-- Crib: KNOWSTHEEXACT --
Offset  Pattern        Key run
------  -------------  -------------------
  204   SCISSAAB      SCISSAABSCISS
  
-- Crib: LIESTHENUANCE --
Offset  Pattern        Key run
------  -------------  -------------------
   40   PALIMPSEST    PALIMPSESTPAL
