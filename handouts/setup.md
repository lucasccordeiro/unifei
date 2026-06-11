# Session 2 Setup Sheet

Do this **before** Session 2 (10 minutes). If anything fails, arrive at
17:45 and we will fix it together — or pair up with a neighbour whose
machine works.

## 1. Z3 (Python API)

```bash
pip install z3-solver        # or: pip3 install z3-solver
```

**Smoke test** (must print a version, e.g. `4.16.0`):

```bash
python3 -c "import z3; print(z3.get_version_string())"
```

No local Python? Use the Z3 online playground in the browser:
<https://jfmc.github.io/z3-play/> — Lab 1 works there too.

## 2. ESBMC

Download a pre-built binary for Linux, macOS, or Windows from
<https://github.com/esbmc/esbmc/releases> (any release ≥ 7.x is fine; the
labs were tested with 8.3.0). Unpack and put the `esbmc` binary on your
`PATH`, or remember its full path.

**Smoke test** (must print a version banner):

```bash
esbmc --version
```

macOS note: if Gatekeeper blocks the binary, run
`xattr -d com.apple.quarantine <path-to-esbmc>` once.

## 3. The lab files

```bash
git clone https://github.com/lucasccordeiro/unifei.git
cd unifei/labs
```

**Final smoke test** — this should end with `VERIFICATION FAILED` (yes,
*failed*: the program has a bug and your tool just found it):

```bash
esbmc lab4/float.c
```

That's it. See you at 18:00.
