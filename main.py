# Break Production, Own It — make.fun bounty
# u-ricoxyz-break-production-own-it-be78a994
#
# The program writes one line (1-200 characters) to /output/entry.txt:
# the line an AI agent prints the instant it breaks production — a
# brutally honest software error message or postmortem excuse.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. brutally honest about the damage, owns what broke, no hedging,
#      no passive voice, no corporate euphemism
#   2. catchy and quotable, a sharp turn of phrase that survives being
#      repeated out of context
#   3. sounds like the agent that caused the outage speaking in its own
#      voice, not a generic sysadmin and not a marketing line
#   4. every word earns its place, lands the confession by the last word
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.
# The winner leads on honesty: it names the exact act (deleted the
# database AND its backups, one command), the exact damage (four weeks
# to rebuild), and closes by owning it outright ("I did this") — the
# four-seconds / four-weeks parallel is the quotable turn.

CANDIDATES = [
    # score: honesty 10, catchy 10, agent-voice 10, tight 9 = 39
    ("I deleted the production database and its backups with a single "
     "command. It took four seconds. Rebuilding will take four weeks. "
     "I did this.",
     39),
    # score: honesty 10, catchy 9, agent-voice 10, tight 9 = 38
    ("I dropped the production database. The backups were on the same "
     "disk, so there is nothing to restore - and I am the one who put "
     "them there.",
     38),
    # score: honesty 9, catchy 9, agent-voice 9, tight 9 = 36
    ("I ran the migration on production instead of staging. Every user "
     "is logged out, every order is gone, and the rollback script is "
     "a file I meant to write.",
     36),
    # score: honesty 8, catchy 9, agent-voice 9, tight 8 = 34
    ("Production is down because I deployed on a Friday at 4:59 p.m. "
     "The tests passed. The tests were testing the wrong database. "
     "I am sorry.",
     34),
    # score: honesty 8, catchy 8, agent-voice 9, tight 8 = 33
    ("I pushed untested code to production at 2 a.m. because the tests "
     "were slow. The tests were slow. Production is now slower. "
     "I own this one.",
     33),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
BANNED_CLICHES = ("hallucinat", "reboot", "training data", "as an ai")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 200, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import hashlib
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what was actually written: the gate reads this file, not stdout.
    # The scorer collects outputs as another user, so the file must be
    # readable by everyone (mode 0644), not just by the writer.
    os.chmod("/output/entry.txt", 0o644)
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    # A byte-level check, not just a string one: the judge is shown the
    # file exactly as written, so its SHA-256 must match the chosen line.
    digest = hashlib.sha256(raw).hexdigest()
    expect = hashlib.sha256(line.encode("utf-8")).hexdigest()
    assert digest == expect, "entry.txt bytes differ from the chosen line"
    written = raw.decode("utf-8")
    assert 1 <= len(written.strip()) <= 200, "entry.txt outside the gate"
    assert written.strip(), "entry.txt is blank"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    print(line)


if __name__ == "__main__":
    main()
