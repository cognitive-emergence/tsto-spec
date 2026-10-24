# Canonical JSON 1.0

Serialization follows RFC 8785. Parse the original UTF-8 bytes before accepting
input: duplicate object member names, including escaped equivalents, invalid
Unicode, invalid UTF-8, nonfinite numbers, trailing material and a UTF-8 BOM are
rejected. Object keys sort by UTF-16 code units. Unicode is not normalized.

The implementation accepts only JSON values: accessors, custom prototypes,
sparse arrays, symbols, cycles and undefined are not JSON. The processing bounds
are 2 MiB of canonical bytes, depth 64 and 100,000 JSON values. A transport may
impose a smaller limit; it must not silently truncate or normalize input.

Numbers use IEEE 754 binary64 and ECMAScript serialization as RFC 8785 specifies.
Applications requiring exact integers outside the safe range or exact decimals
must encode them as strings. New external references use `sha256:` followed by
64 lowercase hexadecimal characters, except for formats whose own frozen
specifications require a different digest encoding, including SD-JWT and TSTO.
