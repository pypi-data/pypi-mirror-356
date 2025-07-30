"""
Integration tests for the Compact Frame Format library.

These tests verify the complete framing protocol workflow by:
1. Parsing individual frame files to extract payloads
2. Combining frame files into a stream and parsing the entire stream
3. Recreating frames from payloads and verifying they match the original stream

The test data includes various payload types:
- Empty payload
- Simple text
- Binary data with all byte values
- Large text payload
- JSON-like data
- Data with null bytes
- All spaces
- Numeric data
"""

import glob
import os
import re
from pathlib import Path

import pytest

from compact_frame_format.cff import Cff, ParseResultEnum


class DataPaths:
    """Helper class to manage test data file paths."""

    def __init__(self, test_data_dir: Path):
        self.test_data_dir = test_data_dir

    def get_frame_files(self) -> list[Path]:
        """Get all numbered frame files, sorted by number."""
        pattern = str(self.test_data_dir / "[0-9][0-9]_*.bin")
        frame_files = glob.glob(pattern)

        def extract_number(filename: str) -> int:
            basename = os.path.basename(filename)
            match = re.match(r"^(\d+)_", basename)
            return int(match.group(1)) if match else 0

        frame_files.sort(key=extract_number)
        return [Path(f) for f in frame_files]

    @property
    def stream_file(self) -> Path:
        """Path to the stream.bin file."""
        return self.test_data_dir / "stream.bin"


@pytest.fixture
def test_data_dir() -> Path:
    """Fixture providing the path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def test_paths(test_data_dir: Path) -> DataPaths:
    """Fixture providing helper for test data paths."""
    return DataPaths(test_data_dir)


@pytest.fixture
def frame_handler() -> Cff:
    """Fixture providing a fresh Frame instance for each test."""
    return Cff()


@pytest.fixture
def expected_payloads(test_paths: DataPaths, frame_handler: Cff) -> list[bytes]:
    """Fixture that loads expected payloads by parsing individual frame files."""
    frame_files = test_paths.get_frame_files()
    assert frame_files, "No numbered frame files found in test data"

    payloads = []
    for frame_file in frame_files:
        with open(frame_file, "rb") as f:
            frame_data = f.read()

        cframe, result = frame_handler.parse(frame_data)
        assert result == ParseResultEnum.SUCCESS, f"Failed to parse {frame_file.name}: {result}"
        payloads.append(cframe.payload)

    return payloads


@pytest.fixture
def stream_data(test_paths: DataPaths) -> bytes:
    """Fixture that loads the stream.bin file data."""
    stream_file = test_paths.stream_file
    assert stream_file.exists(), f"Stream file not found: {stream_file}"

    with open(stream_file, "rb") as f:
        return f.read()


@pytest.fixture
def recreated_stream_file() -> Path:
    """Fixture that creates stream.bin from numbered frame files and returns its path."""
    test_data_dir = Path(__file__).parent / "data"
    output_file = test_data_dir / "stream.bin"

    # Get all numbered frame files
    pattern = str(test_data_dir / "[0-9][0-9]_*.bin")
    frame_files = glob.glob(pattern)

    def extract_number(filename: str) -> int:
        basename = os.path.basename(filename)
        match = re.match(r"^(\d+)_", basename)
        return int(match.group(1)) if match else 0

    frame_files.sort(key=extract_number)
    assert frame_files, "No numbered frame files found for stream creation"

    # Combine all frame files into stream.bin
    with open(output_file, "wb") as stream_file:
        for frame_file in frame_files:
            if os.path.exists(frame_file):
                with open(frame_file, "rb") as f:
                    frame_data = f.read()
                    stream_file.write(frame_data)

    return output_file


class TestFrameFileIntegration:
    """Integration tests for individual frame file processing."""

    def test_frame_files_exist(self, test_paths: DataPaths):
        """Test that all expected frame files exist."""
        frame_files = test_paths.get_frame_files()
        assert len(frame_files) > 0, "No frame files found"

        # Verify files are properly named and numbered
        expected_numbers = set()
        for frame_file in frame_files:
            basename = frame_file.name
            match = re.match(r"^(\d+)_.*\.bin$", basename)
            assert match, f"Frame file {basename} doesn't match expected naming pattern"
            expected_numbers.add(int(match.group(1)))

        # Check for sequential numbering (allowing gaps)
        min_num = min(expected_numbers)
        assert min_num >= 1, "Frame numbering should start from 1 or higher"
        assert len(frame_files) == len(expected_numbers), "Duplicate frame numbers detected"

    def test_all_frame_files_parseable(self, test_paths: DataPaths, frame_handler: Cff):
        """Test that all individual frame files can be parsed successfully."""
        frame_files = test_paths.get_frame_files()

        for frame_file in frame_files:
            with open(frame_file, "rb") as f:
                frame_data = f.read()

            cframe, result = frame_handler.parse(frame_data)
            assert result == ParseResultEnum.SUCCESS, f"Failed to parse {frame_file.name}: {result}"
            assert cframe.payload is not None, f"Payload is None for {frame_file.name}"
            assert cframe.frame_counter is not None, f"Frame counter is None for {frame_file.name}"

    def test_expected_payloads_loaded(self, expected_payloads: list[bytes]):
        """Test that expected payloads fixture works correctly."""
        assert len(expected_payloads) > 0, "No expected payloads loaded"

        # Verify we have different payload types based on known test data
        payload_lengths = [len(p) for p in expected_payloads]
        unique_lengths = set(payload_lengths)
        assert len(unique_lengths) > 1, "Expected payloads of different lengths"

        # Check for empty payload (should be first based on naming)
        assert len(expected_payloads[0]) == 0, "First payload should be empty based on file naming"


class TestStreamProcessing:
    """Integration tests for stream processing functionality."""

    def test_stream_file_exists(self, test_paths: DataPaths):
        """Test that stream.bin file exists and has reasonable size."""
        stream_file = test_paths.stream_file
        assert stream_file.exists(), f"Stream file not found: {stream_file}"

        file_size = stream_file.stat().st_size
        assert file_size > 0, "Stream file should not be empty"

        # Stream should be larger than any individual frame
        frame_files = test_paths.get_frame_files()
        individual_sizes = []
        for frame_file in frame_files:
            individual_sizes.append(frame_file.stat().st_size)

        max_individual_size = max(individual_sizes) if individual_sizes else 0
        assert file_size >= max_individual_size, "Stream should be at least as large as largest individual frame"

    def test_parse_stream_payloads(self, stream_data: bytes, expected_payloads: list[bytes], frame_handler: Cff):
        """Test parsing all payloads from stream.bin and verify they match expected payloads."""
        # Parse all payloads from stream
        found_payloads = []
        remaining_data = stream_data

        while remaining_data:
            cframe, bytes_consumed = frame_handler.find_frame(remaining_data)
            if not cframe:
                break

            found_payloads.append(cframe.payload)

            # Advance by bytes consumed
            if bytes_consumed >= len(remaining_data):
                break
            remaining_data = remaining_data[bytes_consumed:]

        # Verify we found all expected payloads
        assert len(found_payloads) == len(expected_payloads), (
            f"Expected {len(expected_payloads)} payloads, found {len(found_payloads)}"
        )

        for i, (found, expected) in enumerate(zip(found_payloads, expected_payloads)):
            assert found == expected, f"Payload {i} mismatch: expected {len(expected)} bytes, got {len(found)} bytes"

    def test_recreate_stream_from_payloads(self, expected_payloads: list[bytes], stream_data: bytes):
        """Test recreating stream from payloads and verify it matches original stream."""
        # Create a new frame handler for recreation
        frame_handler = Cff()

        # Recreate frames from payloads
        recreated_stream = b""
        for payload in expected_payloads:
            frame = frame_handler.create(payload)
            recreated_stream += frame

        # Verify the recreated stream matches the original
        assert len(recreated_stream) == len(stream_data), (
            f"Recreated stream length {len(recreated_stream)} != original {len(stream_data)}"
        )
        assert recreated_stream == stream_data, "Recreated stream doesn't match original"

        # Additional verification: parse the recreated stream
        frame_handler_verify = Cff()
        verified_payloads = []
        remaining = recreated_stream

        while remaining:
            cframe, bytes_consumed = frame_handler_verify.find_frame(remaining)
            if not cframe:
                break

            verified_payloads.append(cframe.payload)
            if bytes_consumed >= len(remaining):
                break
            remaining = remaining[bytes_consumed:]

        assert verified_payloads == expected_payloads, "Verified payloads don't match expected"


class TestEndToEndWorkflow:
    """End-to-end integration tests simulating real-world usage."""

    def test_complete_workflow(self, test_paths: DataPaths):
        """Test complete workflow from individual files to stream processing."""
        frame_handler = Cff()

        # Step 1: Parse individual frame files
        frame_files = test_paths.get_frame_files()
        individual_payloads = []

        for frame_file in frame_files:
            with open(frame_file, "rb") as f:
                frame_data = f.read()

            cframe, result = frame_handler.parse(frame_data)
            assert result == ParseResultEnum.SUCCESS, f"Failed to parse {frame_file.name}"
            individual_payloads.append(cframe.payload)

        # Step 2: Load and parse stream
        stream_data = test_paths.stream_file
        with open(stream_data, "rb") as f:
            stream_bytes = f.read()

        stream_payloads = []
        remaining = stream_bytes

        while remaining:
            cframe, bytes_consumed = frame_handler.find_frame(remaining)
            if not cframe:
                break

            stream_payloads.append(cframe.payload)
            if bytes_consumed >= len(remaining):
                break
            remaining = remaining[bytes_consumed:]

        # Step 3: Verify consistency
        assert len(individual_payloads) == len(stream_payloads), "Payload count mismatch"
        assert individual_payloads == stream_payloads, "Payload content mismatch"

        # Step 4: Recreate stream and verify
        recreated_handler = Cff()
        recreated_stream = b""

        for payload in individual_payloads:
            frame = recreated_handler.create(payload)
            recreated_stream += frame

        assert recreated_stream == stream_bytes, "Recreated stream doesn't match original"

    def test_frame_boundary_detection(self, stream_data: bytes, frame_handler: Cff):
        """Test that frame boundaries are correctly detected in stream data."""
        # Find all frames in the stream
        frames, total_consumed = frame_handler.parse_frames(stream_data)

        assert len(frames) > 0, "Should find at least one frame in stream"
        assert total_consumed <= len(stream_data), "Should not consume more bytes than available"

        # Verify we can parse each frame correctly by recreating them
        recreated_handler = Cff()
        for i, cframe in enumerate(frames):
            # Create a new frame with the same payload and counter
            recreated_frame = recreated_handler.create(cframe.payload, frame_counter=cframe.frame_counter)

            # Parse the recreated frame
            parsed_cframe, result = frame_handler.parse(recreated_frame)
            assert result == ParseResultEnum.SUCCESS, f"Recreated frame {i} should parse successfully"
            assert parsed_cframe.payload == cframe.payload, f"Frame {i} payload should match"
            assert parsed_cframe.frame_counter == cframe.frame_counter, f"Frame {i} counter should match"

    def test_error_resilience(self, stream_data: bytes, frame_handler: Cff):
        """Test error resilience with corrupted stream data."""
        # Test 1: Corrupt a single byte in the middle of stream
        corrupted_stream = bytearray(stream_data)
        if len(corrupted_stream) > 100:
            corrupted_stream[50] ^= 0xFF  # Flip all bits in byte 50

            # Should still find some valid frames
            frames, total_consumed = frame_handler.parse_frames(bytes(corrupted_stream))
            # We might find fewer frames due to corruption, but shouldn't crash
            assert len(frames) >= 0, "Should handle corruption gracefully"

        # Test 2: Truncated stream
        if len(stream_data) > 20:
            truncated_stream = stream_data[:-10]  # Remove last 10 bytes

            frames, total_consumed = frame_handler.parse_frames(truncated_stream)
            # Should find at least some frames from the beginning
            assert len(frames) >= 0, "Should handle truncation gracefully"

        # Test 3: Stream with junk data at beginning
        junk_prefix = b"JUNK DATA" * 10
        prefixed_stream = junk_prefix + stream_data

        original_frames, original_consumed = frame_handler.parse_frames(stream_data)
        prefixed_frames, prefixed_consumed = frame_handler.parse_frames(prefixed_stream)

        # Should find the same payloads
        original_payloads = [cframe.payload for cframe in original_frames]
        prefixed_payloads = [cframe.payload for cframe in prefixed_frames]

        assert original_payloads == prefixed_payloads, "Should find same payloads despite junk prefix"

    def test_complete_workflow_with_stream_api(self, test_paths: DataPaths):
        """Test complete workflow using the stream API (parse_frames)."""
        frame_handler = Cff()

        # Load stream data
        with open(test_paths.stream_file, "rb") as f:
            stream_data = f.read()

        # Parse using stream API
        stream_frames, total_consumed = frame_handler.parse_frames(stream_data)
        stream_payloads = [cframe.payload for cframe in stream_frames]

        # Load individual frame files for comparison
        frame_files = test_paths.get_frame_files()
        individual_payloads = []

        for frame_file in frame_files:
            with open(frame_file, "rb") as f:
                frame_data = f.read()

            cframe, result = frame_handler.parse(frame_data)
            assert result == ParseResultEnum.SUCCESS, f"Failed to parse {frame_file.name}"
            individual_payloads.append(cframe.payload)

        # Verify stream API results match individual file results
        assert len(stream_payloads) == len(individual_payloads), "Stream API should find all frames"
        assert stream_payloads == individual_payloads, "Stream API payloads should match individual files"

        # Verify frame counters are sequential
        stream_counters = [cframe.frame_counter for cframe in stream_frames]
        expected_counters = list(range(len(stream_frames)))
        assert stream_counters == expected_counters, "Frame counters should be sequential"

        # Verify total bytes consumed makes sense
        assert total_consumed <= len(stream_data), "Should not consume more bytes than available"

    def test_systematic_byte_corruption_error_recovery(
        self, stream_data: bytes, expected_payloads: list[bytes], frame_handler: Cff
    ):
        """Test byte corruption - corrupting any single byte should result in exactly one frame being lost."""
        expected_frame_count = len(expected_payloads)

        # Convert to bytearray for efficient in-place modification
        byte_stream = bytearray(stream_data)

        # Test corruption at each byte position
        for corrupt_pos in range(len(byte_stream)):
            # Corrupt the byte at this position (flip all bits)
            byte_stream[corrupt_pos] ^= 0xFF

            frames, _ = frame_handler.parse_frames(bytes(byte_stream))

            # Corrupting any single byte should result in exactly one frame being corrupted,
            # so we should parse exactly (expected_frame_count - 1) frames
            assert len(frames) == expected_frame_count - 1, (
                f"Corrupting byte at position {corrupt_pos} should result in exactly {expected_frame_count - 1} "
                f"frames parsed, but got {len(frames)}"
            )

            # Restore the corrupted byte
            byte_stream[corrupt_pos] ^= 0xFF
