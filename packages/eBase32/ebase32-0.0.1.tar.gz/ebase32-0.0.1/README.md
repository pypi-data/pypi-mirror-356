# eBase32

`eBase32` is a custom Base32 encoding standard designed to be fully URL-safe and free from ambiguous characters. The goal is to provide a human-friendly, robust, and deterministic alternative to classical Base32 schemes such as Crockford or RFC 4648.

## Features

- ✅ No ambiguous characters (`0`, `O`, `I`, `l`, `1`, `S`, `B`, `Z`, etc.)
- ✅ Fully alphanumeric – no symbols
- ✅ Ideal for IDs, tokens, URLs, QR codes, or human-readable values
- ✅ No padding, no special rules

The character set consists of the following 32 characters:

```
ACEFHKLMNPRTWXYadeghknrtwxy34679
```

## Installation

```bash
pip install eBase32
```

## Usage

### Functional API

```python
from eBase32 import encode, decode

data = b"hello world"
encoded = encode(data)
decoded = decode(encoded)

assert decoded == data
```

### Object-Oriented API

```python
from eBase32 import EBase32

id = EBase32(b"hello")
print(str(id))         # eBase32 string
print(id.bytes)        # original bytes
print(id.string)       # eBase32 string (same as str())
print(bytes(id))       # original bytes
```

### Comparison & Equality

```python
a = EBase32(b"data")
b = EBase32(str(a))

assert a == b
assert a == b.bytes
assert a == b.string
```

## License

Released under the [MIT License](LICENSE).

## Author

Endkind ([@Endkind](https://github.com/Endkind))

---

## Technical Specification

For implementation and specification details, see [STANDARD.md](./docs/standard.md).

- Bit packing
- Character set origin
- Comparison to other standards
- Performance considerations
