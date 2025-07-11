#!/usr/bin/env python3
"""
full_password_slider.py  —  v1.1  (2025‑07‑10)
────────────────────────────────────────────────────────────────
Automates Kryptos‑style *crib sliding* **and now prunes already
confirmed passcodes** so they never clutter the rankings again.

New in v1.1
-----------
•  Adds `KEYWORDS_TO_PRUNE` (default: ABSCISSA, PALIMPSEST).
•  Detects the keywords even when *mildly scrambled* via:
   – exact match (ABSCISSA)
   – cyclic rotation   (BSCISSAA …)
   – simple anagram    (SABSCISA …)
•  Any slice generating such a pattern is silently discarded before
   entering the global list.
•  Everything else works as before: window 7‑17, top‑10 per slice,
   live progress, safe Ctrl‑C shutdown.

Replace placeholder texts with live Kryptos data to unleash full power.
"""
from __future__ import annotations
import itertools
import signal
from typing import List, Tuple

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PRIMARY_KEY = "KRYPTOS"        # primary key driving the tableau
MIN_SLICE = 13                  # inclusive
MAX_SLICE = 64                 # inclusive
TOP_PER_SLICE = 50             # keep this many per plaintext slice
MAX_PATTERN_LEN = 64           # search up to this period length

KEYWORDS_TO_PRUNE = [
    "ABSCISSA",
    "PALIMPSEST",
]

# ────────────────────────────────────────────────────────────────
# 1. Tableau helpers
# ────────────────────────────────────────────────────────────────

def keyed_alphabet(keyword: str) -> str:
    seen = set()
    return ''.join(ch for ch in (keyword + ALPHABET) if not (ch in seen or seen.add(ch)))

TABLEAU = keyed_alphabet(PRIMARY_KEY)


def key_letter(p: str, c: str) -> str:
    idx = (TABLEAU.index(c) - TABLEAU.index(p)) % 26
    return TABLEAU[idx]


# ────────────────────────────────────────────────────────────────
# 2. Pattern utilities
# ────────────────────────────────────────────────────────────────

def minimal_period_prefix(s: str, max_p: int = MAX_PATTERN_LEN) -> int:
    for p in range(1, min(max_p, len(s)) + 1):
        if all(s[i] == s[i % p] for i in range(len(s))):
            return p
    return len(s)


def letter_only(text: str) -> str:
    return ''.join('K' if ch == '?' else ch for ch in text.upper() if ch.isalpha() or ch == '?')


# ────────────────────────────────────────────────────────────────
# 3. Keyword‑prune helpers
# ────────────────────────────────────────────────────────────────

def is_cyclic_rotation(a: str, b: str) -> bool:
    """Return True if *a* is any rotation of *b*. (Case‑sensitive, assumes
    equal length.)"""
    return len(a) == len(b) and a in (b + b)


def is_anagram(a: str, b: str) -> bool:
    return len(a) == len(b) and sorted(a) == sorted(b)


def should_prune(pattern: str) -> bool:
    for kw in KEYWORDS_TO_PRUNE:
        if len(pattern) != len(kw):
            continue
        if pattern == kw or is_cyclic_rotation(pattern, kw) or is_anagram(pattern, kw):
            return True
    return False


# ────────────────────────────────────────────────────────────────
# 4. Core algorithm – slide one crib across one cipher
# ────────────────────────────────────────────────────────────────

def scan_slice_against_cipher(cipher: str, crib: str, max_pat_len: int = MAX_PATTERN_LEN) -> List[Tuple[int, str, str, int]]:
    cipher = letter_only(cipher)
    crib   = letter_only(crib)
    win    = len(crib)
    results = []
    for off in range(len(cipher) - win + 1):
        seg       = cipher[off : off + win]
        key_run   = ''.join(key_letter(p, c) for p, c in zip(crib, seg))
        period    = minimal_period_prefix(key_run, max_pat_len)
        pattern   = key_run[:period]
        if should_prune(pattern):
            continue  # drop already‑known keyword patterns
        score     = period  # shorter pattern = better
        results.append((off, pattern, key_run, score))
    results.sort(key=lambda t: (t[3], t[0]))
    return results[:TOP_PER_SLICE]


# ────────────────────────────────────────────────────────────────
# 5. Plaintext window generator
# ────────────────────────────────────────────────────────────────

def generate_slices(plain: str, min_len: int = MIN_SLICE, max_len: int = MAX_SLICE):
    txt = letter_only(plain)
    for win in range(min_len, max_len + 1):
        for start in range(len(txt) - win + 1):
            yield start, txt[start:start + win]


# ────────────────────────────────────────────────────────────────
# 6. Main driver
# ────────────────────────────────────────────────────────────────

def graceful_exit(signum, frame):  # noqa: D401 – simple handler
    print("\n[!] Interrupted – shutting down gracefully …")
    raise SystemExit(0)


signal.signal(signal.SIGINT, graceful_exit)


def main() -> None:
    # --- Replace placeholders with real data as needed ---
    solved_texts = {
        "K0": "EEVIRTUALLYEEEEEEEINVISIBLEDIGETALEEEINTERPRETATITEESHADOWEEFORCESEEEEELUCIDEEEMEMORYETISYOURPOSITIONESOSRQ",
        "K1_plain": "BETWEENSUBTLESHADINGANDTHEABSENCEOFLIGHTLIESTHENUANCEOFIQLUSION", 
        "K2_plain": "ITWASTOTALLYINVISIBLEHOWSTHATPOSSIBLETHEYUSEDTHEEARTHSMAGNETICFIELDTHEINFORMATIONWASGATHEREDANDTRANSMITTEDUNDERGRUUNDTOANUNKNOWNLOCATIONDOESLANGLEYKNOWABOUTTHISTHEYSHOULDITSBURIEDOUTTHERESOMEWHEREWHOKNOWSTHEEXACTLOCATIONONLYWWTHISWASHISLASTMESSAGETHIRTYEIGHTDEGREESFIFTYSEVENMINUTESSIPOINTFIVESECONDSNORTHSEVENTYSEVENDEGREESEIGHTMINUTESFORTYFOURSECONDSWESTLAYERTWO",  # example only
        "K3_plain": "SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWASREMOVEDWITHTREMBLINGHANDSIMADEATINYBREACHINTHEUPPERLEFTHANDCORNERANDTHENWIDENINGTHEHOLEALITTLEIINSERTEDTHECANDLEANDPEEREDINTHEHOTAIRESCAPINGFROMTHECHAMBERCAUSEDTHEFLAMETOFLICKERBUTPRESENTLYDETAILSOFTHEROOMWITHINEMERGEDFROMTHEMISTCANYOUSEEANYTHINGQ",  # example only
    }

    ciphertexts = {
        "K1": "EMUFPHZLRFAXYUSDJKZLDKRNSHGNFIVJYQTQUXQBQVYUVLLTREVJYQTMKYRDMFD",
        "K2": "VFPJUDEEHZWETZYVGWHKKQETGFQJNCE GGWHKK?DQMCPFQZDQMMIAGPFXHQRLG TIMVMZJANQLVKQEDAGDVFRPJUNGEUNA QZGZLECGYUXUEENJTBJLBQCRTBJDFHRR YIZETKZEMVDUFKSJHKFWHKUWQLSZFTI HHDDDUVH?DWKBFUFPWNTDFIYCUQZERE EVLDKFEZMOQQJLTTUGSYQPFEUNLAVIDX FLGGTEZ?FKZBSFDQVGOGIPUFXHHDRKF FHQNTGPUAECNUVPDJMQCLQUMUNEDFQ ELZZVRRGKFFVOEEXBDMVPNFQXEZLGRE DNQFMPNZGLFLPMRJQYALMGNUVPDXVKP DQUMEBEDMHDAFMJGZNUPLGEWJLLAETG",  # shortened for brevity
        "K3": "ENDYAHROHNLSRHEOCPTEOIBIDYSHNAIA CHTNREYULDSLLSLLNOHSNOSMRWXMNE TPRNGATIHNRARPESLNNELEBLPIIACAE WMTWNDITEENRAHCTENEUDRETNHAEOE TFOLSEDTIWENHAEIOYTEYQHEENCTAYCR EIFTBRSPAMHHEWENATAMATEGYEERLB TEEFOASFIOTUETUAEOTOARMAEERTNRTI BSEDDNIAAHTTMSTEWPIEROAGRIEWFEB AECTDDHILCEIHSITEGOEAOSDDRYDLORIT RKLMLEHAGTDHARDPNEOHMGFMFEUHE ECDMRIPFEIMEHNLSSTTRTVDOHW?",  # shortened
        "K4": "OBKR UOXOGHULBSOLIFBBWFLRVQQPRNGKSSO TWTQSJQSSEKZZWATJKLUDIAWINFBNYP VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR",  # shortened
    }

    global_results: List[Tuple[int, str, str, int, str, int, str, str]] = []
    # (pattern_len, pattern, key_run, offset, cipher_label, slice_start, plain_label, slice_text)

    for plain_label, plain in solved_texts.items():
        print(f"\n>>> Processing plaintext source: {plain_label}")
        for slice_start, slice_text in generate_slices(plain):
            if slice_start % 500 == 0:
                print(f"  → slice @ {slice_start:4} len {len(slice_text):2}", end="\r")

            for cipher_label, cipher in ciphertexts.items():
                slice_hits = scan_slice_against_cipher(cipher, slice_text)
                for off, pat, key_run, score in slice_hits:
                    record = (score, pat, key_run, off, cipher_label, slice_start, plain_label, slice_text)
                    global_results.append(record)

    # Global ranking
    print("\n\n=== Aggregating results (pruned) ===")
    global_results.sort(key=lambda r: (r[0], r[3]))

    print("Pattern  Len Offset Cipher Slice-src Slice-idx  Key-run")
    print("------- ---- ------ ------ ---------- --------- -------------------")
    for rank, rec in enumerate(global_results[:3000], 1):
        score, pat, key_run, off, cipher_label, slice_start, plain_label, slice_text = rec
        print(f"#{rank:02} {pat:<8} {score:4} {off:6} {cipher_label:<6} {plain_label:<10} {slice_start:7}  {key_run}")

    print("\n[*] Done. Keywords {', '.join(KEYWORDS_TO_PRUNE)} have been pruned.\n")


if __name__ == "__main__":
    main()
