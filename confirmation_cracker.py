#!/usr/bin/env python3
"""
kryptos multi passcode scan.py
-----------------------------------------
Slides a list of cribs across multiple ciphertexts,
finding and ranking repeating-key (passcode) patterns.
Shows the top N results for each crib/ciphertext combo.
Will likely be needed to scan for more passcodes.
"""

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PRIMARY  = "KRYPTOS"

def keyed_alphabet(keyword: str) -> str:
    seen = set()
    return ''.join(ch for ch in (keyword + ALPHABET) if not (ch in seen or seen.add(ch)))

TABLEAU = keyed_alphabet(PRIMARY)

def key_letter(p: str, c: str) -> str:
    idx = (TABLEAU.index(c) - TABLEAU.index(p)) % 26
    return TABLEAU[idx]

def minimal_period_prefix(s: str, max_p: int = 12) -> int:
    for p in range(1, min(max_p, len(s)) + 1):
        if all(s[i] == s[i % p] for i in range(len(s))):
            return p
    return len(s)

def scan_for_passcodes(cipher: str, crib: str, max_pat_len: int = 12):
    results = []
    cipher = ''.join('K' if ch == '?' else ch for ch in cipher.upper() if ch.isalpha() or ch == '?')
    for off in range(len(cipher) - len(crib) + 1):
        seg = cipher[off : off + len(crib)]
        key_run = ''.join(key_letter(p, c) for p, c in zip(crib, seg))
        period  = minimal_period_prefix(key_run, max_pat_len)
        pattern = key_run[:period]
        score   = len(pattern)  # Shortest pattern = best
        results.append((off, pattern, key_run, score))
    results.sort(key=lambda x: (x[3], x[0]))  # By pattern length, then offset
    return results

def main():
    # === Preset your ciphertexts here ===
    ciphertexts = {
        "K1": "EMUFPHZLRFAXYUSDJKZLDKRNSHGNFIVJ YQTQUXQBQVYUVLLTREVJYQTMKYRDMFD",
        "K2": "VFPJUDEEHZWETZYVGWHKKQETGFQJNCE GGWHKK?DQMCPFQZDQMMIAGPFXHQRLG TIMVMZJANQLVKQEDAGDVFRPJUNGEUNA QZGZLECGYUXUEENJTBJLBQCRTBJDFHRR YIZETKZEMVDUFKSJHKFWHKUWQLSZFTI HHDDDUVH?DWKBFUFPWNTDFIYCUQZERE EVLDKFEZMOQQJLTTUGSYQPFEUNLAVIDX FLGGTEZ?FKZBSFDQVGOGIPUFXHHDRKF FHQNTGPUAECNUVPDJMQCLQUMUNEDFQ ELZZVRRGKFFVOEEXBDMVPNFQXEZLGRE DNQFMPNZGLFLPMRJQYALMGNUVPDXVKP DQUMEBEDMHDAFMJGZNUPLGEWJLLAETG",
        "K3": "ENDYAHROHNLSRHEOCPTEOIBIDYSHNAIA CHTNREYULDSLLSLLNOHSNOSMRWXMNE TPRNGATIHNRARPESLNNELEBLPIIACAE WMTWNDITEENRAHCTENEUDRETNHAEOE TFOLSEDTIWENHAEIOYTEYQHEENCTAYCR EIFTBRSPAMHHEWENATAMATEGYEERLB TEEFOASFIOTUETUAEOTOARMAEERTNRTI BSEDDNIAAHTTMSTEWPIEROAGRIEWFEB AECTDDHILCEIHSITEGOEAOSDDRYDLORIT RKLMLEHAGTDHARDPNEOHMGFMFEUHE ECDMRIPFEIMEHNLSSTTRTVDOHW?",
        "K4": "OBKR UOXOGHULBSOLIFBBWFLRVQQPRNGKSSO TWTQSJQSSEKZZWATJKLUDIAWINFBNYP VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR",
        # Add more if needed
    }
    # === Preset your crib list here ===
    crib_list = [
		"HANDCORNERAND",
		"KNOWSTHEEXACT",
		"LIESTHENUANCE",
		"THEDOORWAYWAS",
		"THEROOMWITHIN",
		"USEDTHEEARTHS",
		"WESTXLAYERTWO",
		"YOURPOSITIONE",
        # Add more candidate cribs here!
    ]
    max_pat_len = 12
    top_n = 15

    for ct_label, cipher in ciphertexts.items():
        print(f"\n=== Results for ciphertext: {ct_label} ===")
        for crib in crib_list:
            print(f"\n-- Crib: {crib} --")
            results = scan_for_passcodes(cipher, crib, max_pat_len)
            print("Offset  Pattern        Key run")
            print("------  -------------  -------------------")
            for off, pat, run, score in results[:top_n]:
                print(f"{off:5}   {pat:<12}  {run}")
            print(f"\n[Top {top_n} hits for crib '{crib}' on {ct_label} shown above]\n")
    print("Scan complete.")

if __name__ == "__main__":
    main()
