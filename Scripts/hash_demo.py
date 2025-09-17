#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SHA-256 Step-by-Step CLI Demo (with pacing)
- Pretty output with 'rich' if installed, otherwise plain text.
- Adds timed delays and optional step-by-step pauses.
"""

import argparse
import hashlib
import struct
import time
from typing import List, Tuple

# --- Optional pretty printing (fallback to plain if Rich not installed) ---
USE_RICH = True
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.rule import Rule
    from rich.box import SIMPLE
    console = Console()
except Exception:
    USE_RICH = False
    console = None

def rotr(x, n): return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF
def shr(x, n):  return (x >> n) & 0xFFFFFFFF

def Ch(x, y, z):   return (x & y) ^ (~x & z)
def Maj(x, y, z):  return (x & y) ^ (x & z) ^ (y & z)

def Sigma0(x): return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)
def Sigma1(x): return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)
def sigma0(x): return rotr(x, 7) ^ rotr(x, 18) ^ shr(x, 3)
def sigma1(x): return rotr(x, 17) ^ rotr(x, 19) ^ shr(x, 10)

H_INIT = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

# --- Utility pacing helpers ---------------------------------------------------
def _sleep(delay: float):
    if delay > 0:
        time.sleep(delay)

def _pause(step: bool, prompt="Press [Enter] to continue..."):
    if step:
        try:
            input(prompt)
        except KeyboardInterrupt:
            pass

# --- Core SHA-256 -------------------------------------------------------------
def sha256_pad(msg: bytes) -> bytes:
    bit_len = len(msg) * 8
    padded = msg + b"\x80"
    while ((len(padded) * 8) % 512) != 448:
        padded += b"\x00"
    padded += struct.pack(">Q", bit_len)
    return padded

def chunk_blocks(padded: bytes) -> List[bytes]:
    return [padded[i:i+64] for i in range(0, len(padded), 64)]

def words_from_block(block64: bytes) -> List[int]:
    return list(struct.unpack(">16I", block64))

def extend_schedule(w: List[int]) -> List[int]:
    W = w[:] + [0]*48
    for t in range(16, 64):
        W[t] = (sigma1(W[t-2]) + W[t-7] + sigma0(W[t-15]) + W[t-16]) & 0xFFFFFFFF
    return W

def compress_block(H: List[int], W: List[int], rounds_to_log: int) -> Tuple[List[int], List[dict]]:
    a, b, c, d, e, f, g, h = H
    round_logs = []
    for t in range(64):
        T1 = (h + Sigma1(e) + Ch(e, f, g) + K[t] + W[t]) & 0xFFFFFFFF
        T2 = (Sigma0(a) + Maj(a, b, c)) & 0xFFFFFFFF
        new_h = g
        new_g = f
        new_f = e
        new_e = (d + T1) & 0xFFFFFFFF
        new_d = c
        new_c = b
        new_b = a
        new_a = (T1 + T2) & 0xFFFFFFFF
        a, b, c, d, e, f, g, h = new_a, new_b, new_c, new_d, new_e, new_f, new_g, new_h

        if t < rounds_to_log:
            round_logs.append({
                "t": t,
                "W[t]": W[t],
                "K[t]": K[t],
                "T1": T1,
                "T2": T2,
                "a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "g": g, "h": h
            })

    H_out = [
        (H[0] + a) & 0xFFFFFFFF, (H[1] + b) & 0xFFFFFFFF,
        (H[2] + c) & 0xFFFFFFFF, (H[3] + d) & 0xFFFFFFFF,
        (H[4] + e) & 0xFFFFFFFF, (H[5] + f) & 0xFFFFFFFF,
        (H[6] + g) & 0xFFFFFFFF, (H[7] + h) & 0xFFFFFFFF
    ]
    return H_out, round_logs

def digest_sha256_with_logs(msg: bytes, rounds_to_log: int = 8):
    padded = sha256_pad(msg)
    blocks = chunk_blocks(padded)

    H = H_INIT[:]
    all_block_logs = []
    for i, block in enumerate(blocks):
        W0_15 = words_from_block(block)
        W = extend_schedule(W0_15)
        H, round_logs = compress_block(H, W, rounds_to_log if i == 0 else 0)
        all_block_logs.append({
            "block_index": i,
            "block_hex": block.hex(),
            "W": W,
            "round_logs": round_logs
        })

    out = b"".join(struct.pack(">I", h) for h in H).hex()
    return {
        "input": msg,
        "padded_hex": padded.hex(),
        "blocks": all_block_logs,
        "digest": out
    }

# --- Output helpers with pacing ----------------------------------------------
def print_header(title: str, delay: float):
    if USE_RICH:
        console.rule(f"[bold]{title}[/bold]")
    else:
        print("\n" + "="*len(title))
        print(title)
        print("="*len(title))
    _sleep(delay)

def print_kv(title: str, kv: List[Tuple[str, str]], delay: float, step: bool):
    if USE_RICH:
        if title:
            console.print(Panel.fit(title, style="bold"))
        for k, v in kv:
            console.print(f"[bold]{k}[/bold]: {v}")
            _sleep(delay)
    else:
        if title: print(f"\n{title}:")
        for k, v in kv:
            print(f"  - {k}: {v}")
            _sleep(delay)
    _pause(step)

def print_schedule(W: List[int], limit: int, each_delay: float, step: bool):
    limit = max(0, min(64, limit))
    if USE_RICH:
        console.print(Panel.fit(f"Message Schedule W[0..{limit-1}]", style="bold"))
        for i in range(limit):
            console.print(f"[dim]W[{i:2d}][/dim] = 0x{W[i]:08x}")
            _sleep(each_delay)
    else:
        print(f"\nMessage Schedule W[0..{limit-1}]:")
        for i in range(limit):
            print(f"  W[{i:2d}] = 0x{W[i]:08x}")
            _sleep(each_delay)
    _pause(step)

def print_rounds(round_logs: List[dict], each_delay: float, step: bool):
    if not round_logs:
        return
    if USE_RICH:
        console.print(Panel.fit(f"First {len(round_logs)} Rounds", style="bold"))
    else:
        print(f"\nFirst {len(round_logs)} Rounds:")
    for r in round_logs:
        line = (
            f"t={r['t']:02d}  "
            f"W=0x{r['W[t]']:08x}  K=0x{r['K[t]']:08x}  "
            f"T1=0x{r['T1']:08x}  T2=0x{r['T2']:08x}  "
            f"a..h=0x{r['a']:08x},0x{r['b']:08x},0x{r['c']:08x},0x{r['d']:08x},"
            f"0x{r['e']:08x},0x{r['f']:08x},0x{r['g']:08x},0x{r['h']:08x}"
        )
        if USE_RICH:
            console.print(line)
        else:
            print(line)
        _sleep(each_delay)
    _pause(step)

# --- CLI ---------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Pretty SHA-256 step-by-step demo with pacing."
    )
    parser.add_argument("message", nargs="?", default=None,
                        help="Message to hash. If omitted, you'll be prompted.")
    parser.add_argument("--rounds", type=int, default=8,
                        help="How many rounds of the first block to display (default: 8).")
    parser.add_argument("--no-schedule", action="store_true",
                        help="Do not print the message schedule table.")
    parser.add_argument("--schedule-limit", type=int, default=16,
                        help="How many W[t] entries to show (default: 16; max 64).")
    parser.add_argument("--plain", action="store_true",
                        help="Force plain text (ignore Rich if installed).")

    # pacing options
    parser.add_argument("--delay", type=float, default=1,
                        help="Base delay (seconds) between printed items (default: 0.35).")
    parser.add_argument("--schedule-delay", type=float, default=None,
                        help="Delay per W[t] line (overrides --delay).")
    parser.add_argument("--round-delay", type=float, default=None,
                        help="Delay per round printed (overrides --delay).")
    parser.add_argument("--step", action="store_true",
                        help="Pause for Enter between major sections.")

    args = parser.parse_args()

    global USE_RICH
    if args.plain:
        USE_RICH = False

    msg = args.message
    if msg is None:
        try:
            if USE_RICH:
                console.print(Panel.fit("Enter the message to hash:", title="Input"))
                msg = input("> ")
            else:
                msg = input("Enter the message to hash: ")
        except KeyboardInterrupt:
            return

    # Effective per-line delays
    schedule_delay = args.schedule_delay if args.schedule_delay is not None else args.delay
    round_delay = args.round_delay if args.round_delay is not None else args.delay

    data = msg.encode("utf-8")
    result = digest_sha256_with_logs(data, rounds_to_log=max(0, args.rounds))

    # Header
    print_header("SHA-256 Step-by-Step", args.delay)
    print_kv("Input", [
        ("Text", repr(msg)),
        ("Bytes (hex)", data.hex()),
        ("Bit length", f"{len(data)*8} bits"),
    ], delay=args.delay, step=args.step)

    # Preprocessing
    print_header("Preprocessing", args.delay)
    padded_bits_len = len(bytes.fromhex(result["padded_hex"])) * 8
    print_kv("Padding", [
        ("Padded length (bits)", str(padded_bits_len)),
        ("Padded (hex)", result["padded_hex"]),
    ], delay=args.delay, step=args.step)
    print_kv("Blocks", [
        ("Count", str(len(result["blocks"]))),
        ("Block size", "512 bits (64 bytes)"),
    ], delay=args.delay, step=args.step)

    # First block deep-dive
    if result["blocks"]:
        b0 = result["blocks"][0]
        print_header("Block 0", args.delay)
        print_kv("Block 0", [("Bytes (hex)", b0["block_hex"])], delay=args.delay, step=args.step)

        if not args.no_schedule:
            print_schedule(b0["W"], limit=args.schedule_limit,
                           each_delay=schedule_delay, step=args.step)

        print_rounds(b0["round_logs"], each_delay=round_delay, step=args.step)

    # Final digest + verification
    print_header("Result", args.delay)
    ours = result["digest"]
    theirs = hashlib.sha256(data).hexdigest()
    ok = "✅ MATCH" if ours == theirs else "❌ MISMATCH"
    print_kv("Digest", [
        ("Computed (this script)", ours),
        ("hashlib.sha256", theirs),
        ("Verification", ok),
    ], delay=args.delay, step=False)

    if USE_RICH:
        console.print(Rule())
        console.print(
            "[dim]Tips:[/dim] "
            "[bold]--delay 0.1[/bold] faster • "
            "[bold]--step[/bold] for manual pauses • "
            "[bold]--schedule-limit 64[/bold] to show full W"
        )

if __name__ == "__main__":
    main()
