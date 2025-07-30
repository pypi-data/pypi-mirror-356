# Python Reference Implementation of Compact Frame Format

[![PyPI](https://img.shields.io/pypi/v/compact-frame-format.svg)](https://pypi.org/project/compact-frame-format/)
[![Changelog](https://img.shields.io/github/v/release/CompactFrameFormat/compact-frame-format?include_prereleases&label=changelog)](https://github.com/CompactFrameFormat/cff-python/releases)
[![Tests](https://github.com/CompactFrameFormat/cff-python/actions/workflows/test.yml/badge.svg)](https://github.com/CompactFrameFormat/cff-python/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/CompactFrameFormat/cff-python/blob/master/LICENSE)

## Overview

Compact Frame Format (CFF) is a way of delineating messages (called the _payload_) in a byte stream. It is designed specifically with Microcontrollers (MCUs) in mind, leading to the following design goals:

1. Take advantage of hardware acceleration like Direct Memory Access (DMA) controllers and the CRC peripherals available on most 32-bit MCUs. This precludes the use of delimiter-based packet boundaries that require the CPU to examine every byte.
2. Exploit the fact that modern serial links are already reliable. Universal Serial Bus (USB), Controller Area Network Bus (CANBus), and Bluetooth Low Energy (BLE), already detect and retransmit lost or corrupted packets. Other serial interfaces like Universal Asynchronous Receiver-Transmitters (UART), Serial Peripheral Interface (SPI), and Inter-Integrated Circuit (I2C) are often reliable in practice, with extremely low error rates when the wiring is short and clean. Therefore, the it's okay for error recovery to be expensive, so long as it's possible and the happy path is cheap.
3. Easy to implement and debug. Firmware running on MCUs is not amenable to taking dependencies on 3rd party libraries, so the implementation should be small enough to fit comfortably in a single file, and simple enough that you wouldn't mind implementing it yourself if you had to.
4. Interoperate cleanly with binary serialization formats like [FlatBuffers](https://flatbuffers.dev/) and [CBOR](https://cbor.io/).

In CFF, a frame consists of a header, a payload, and a payload CRC.

```mermaid
block-beta
  columns 6
  block:Header["Header<br><br><br>"]:4
    columns 4
    space:4
    Preamble FrameCounter["Frame Counter"] PayloadSize["Payload Size"] HeaderCRC["Header CRC"]
  end
  Payload
  PayloadCRC["Payload CRC"]
```

The header consists of:

* A 2-byte preamble: [0xFA, 0xCE]. Note that this is better though of as an array of two bytes rather than an unsigned short (ushort) because it is transmitted as 0xFA, 0xCE (spelling face), whereas the ushort 0xFACE would be transmitted as 0xCE, 0xFA (spelling  nothing) in little endian.
* A little-endian ushort frame counter which increments for every frame sent and rolls over to 0 after 65,535 (2^16 - 1) frames have been sent.
* A little-endian ushort payload size, in bytes. This gives a theoretical maximum payload size of 65,535, though few MCU-based applications would want to support this. A protocol making use of CFF can enforce smaller maximum payload sizes if desired. Note that this excludes both the header and the payload CRC at the end. In other words, the _frame_ size is `header_size + payload_size + crc_size`.
* A 16-bit header CRC (see below for details) calculated over the preamble, frame counter, and payload size. This allows the receiver to validate the header and, crucially, the payload size without having to read in the entire frame, as would be the case if there were just one CRC, at the end, covering the entire frame. The problem with having a single CRC is that the if the payload size is corrupted in such a way that it is extremely large (65,535 in the pathological case) the reciever will not detect this until it reads that many bytes, calculates the CRC, and discovers that it doesn't match. Depending on the transmitter's data rate at the time of the error, it could take a long time to receive this many bytes, making the issue look like a dropped link.

Both CRCs are calculated using CRC-16/CCITT-FALSE, with the following settings:

- Width: 16
- Polynomial: 0x1021
- Init: 0xFFFF
- RefIn/RefOut: false / false
- XorOut: 0x0000
- Check("123456789): 0x29B1l

## Usage

### Installation

Install the package using pip:

```powershell
pip install compact-frame-format
```

Or using uv:

```powershell
uv add compact-frame-format
```

### Example

Here's a complete working example (from [`usage_example.py`](https://github.com/CompactFrameFormat/cff-python/blob/main/usage_example.py)):

```python
from compact_frame_format import Cff

# Create and send frames
messages = ["Hello", "World", "CFF"]
buffer = bytearray()

cff = Cff()

print("Creating frames:")
for i, message in enumerate(messages):
    payload = message.encode("utf-8")
    frame = cff.create(payload)

    print(f"  Frame {i}: {message} -> {len(frame)} bytes")

    # Simulate adding to receive buffer
    buffer.extend(frame)

print(f"\nBuffer contains {len(buffer)} bytes total")

# Parse all frames from buffer
received_frames, consumed_bytes = cff.parse_frames(bytes(buffer))

print(f"\nProcessed {consumed_bytes} bytes from buffer")
print("Received frames:")
for frame in received_frames:
    message = frame.payload.decode("utf-8")
    print(f"  Frame {frame.frame_counter}: {message}")

```

## Development

Checkout the code:
```powershell
git clone https://github.com/CompactFrameFormat/cff-python.git
cd cff-python
```

Create a new virtual environment:
```powershell
uv venv && .venv\Scripts\activate.ps1
```

Install dependencies:
```powershell
uv sync --all-extras
```

Install pre-commit hooks:
```powershell
pre-commit install
```

### Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting. Pre-commit hooks are configured to run code quality checks automatically.

Check code formatting and linting:
```powershell
ruff check .
ruff format --check .
```

Format code and fix linting issues:
```powershell
ruff check --fix . && ruff format .
```

### Testing

Run the tests:
```powershell
python -m pytest
```

Run tests with coverage:
```powershell
python -m pytest --cov=compact_frame_format
```
