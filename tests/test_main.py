"""Tests for the musical scale CLI tool."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest
from music21 import note, pitch, stream

from src.main import (
    create_scale,
    get_available_modes,
    print_scale_notes,
    write_midi_file,
)


class TestScaleCreation:
    """Test scale creation functionality."""

    def test_get_available_modes(self) -> None:
        """Test that get_available_modes returns expected scale modes."""
        modes = get_available_modes()

        assert isinstance(modes, list)
        assert len(modes) > 0
        assert "major" in modes
        assert "minor" in modes
        assert "dorian" in modes
        assert "pentatonicMajor" in modes
        assert "blues" in modes

    def test_create_major_scale(self) -> None:
        """Test creating a C major scale."""
        scale_stream = create_scale("C", "major")

        assert isinstance(scale_stream, stream.Stream)

        notes = [
            element.pitch.name
            for element in scale_stream.notes
            if isinstance(element, note.Note) and element.pitch is not None
        ]
        expected_notes = ["C", "D", "E", "F", "G", "A", "B", "C"]

        assert notes == expected_notes

    def test_create_minor_scale(self) -> None:
        """Test creating an A minor scale."""
        scale_stream = create_scale("A", "minor")

        assert isinstance(scale_stream, stream.Stream)

        notes = [
            element.pitch.name
            for element in scale_stream.notes
            if isinstance(element, note.Note) and element.pitch is not None
        ]
        expected_notes = ["A", "B", "C", "D", "E", "F", "G", "A"]

        assert notes == expected_notes

    def test_create_dorian_scale(self) -> None:
        """Test creating a D dorian scale."""
        scale_stream = create_scale("D", "dorian")

        assert isinstance(scale_stream, stream.Stream)
        assert (
            len([n for n in scale_stream.notes]) == 8
        )  # 7 scale notes + 1 final tonic note

    def test_create_pentatonic_major_scale(self) -> None:
        """Test creating a G major pentatonic scale."""
        scale_stream = create_scale("G", "pentatonicMajor")

        assert isinstance(scale_stream, stream.Stream)

        notes = [
            element.pitch.name
            for element in scale_stream.notes
            if isinstance(element, note.Note) and element.pitch is not None
        ]
        # G major pentatonic: G, A, B, D, E, G
        expected_notes = ["G", "A", "B", "D", "E", "G"]

        assert notes == expected_notes

    def test_create_blues_scale(self) -> None:
        """Test creating an E blues scale."""
        scale_stream = create_scale("E", "blues")

        assert isinstance(scale_stream, stream.Stream)

        notes = [
            element.pitch.name
            for element in scale_stream.notes
            if isinstance(element, note.Note) and element.pitch is not None
        ]
        # E blues scale should have 6 notes + final tonic
        assert len(notes) == 7  # 6 blues notes + 1 final tonic note

    def test_create_scale_multiple_octaves(self) -> None:
        """Test creating a scale over multiple octaves."""
        scale_stream = create_scale("C", "major", octaves=2)

        notes = [element for element in scale_stream.notes if hasattr(element, "pitch")]

        # Should have more notes for 2 octaves
        assert len(notes) > 8  # More than single octave

    def test_invalid_scale_mode(self) -> None:
        """Test that invalid scale mode raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported scale mode"):
            create_scale("C", "invalid_mode")  # type: ignore[arg-type]

    def test_create_scale_with_sharp_key(self) -> None:
        """Test creating a scale with sharp key signature."""
        scale_stream = create_scale("F#", "major")

        assert isinstance(scale_stream, stream.Stream)
        notes = [
            element.pitch.name
            for element in scale_stream.notes
            if isinstance(element, note.Note) and element.pitch is not None
        ]

        # F# major scale should start with F#
        assert notes[0] == "F#"

    def test_create_scale_with_flat_key(self) -> None:
        """Test creating a scale with flat key signature."""
        scale_stream = create_scale("Bb", "major")

        assert isinstance(scale_stream, stream.Stream)
        notes = [
            element.pitch.name
            for element in scale_stream.notes
            if isinstance(element, note.Note) and element.pitch is not None
        ]

        # Bb major scale should start with Bb
        assert notes[0] == "B-"  # music21 represents Bb as B-


class TestScaleDisplay:
    """Test scale display functionality."""

    @patch("builtins.print")
    def test_print_scale_notes(self, mock_print) -> None:
        """Test printing scale notes."""
        scale_stream = create_scale("C", "major")

        print_scale_notes(scale_stream, "C", "major")

        # Check that print was called
        mock_print.assert_called()

        # Get the printed output - handle different call formats
        printed_calls = []
        for call in mock_print.call_args_list:
            if call.args:
                printed_calls.append(call.args[0])

        # Should contain scale name and notes
        printed_text = " ".join(str(call) for call in printed_calls)
        assert "C Major Scale:" in printed_text
        assert "Notes:" in printed_text


class TestMidiFileWriting:
    """Test MIDI file writing functionality."""

    @patch("builtins.print")
    def test_write_midi_file(self, mock_print) -> None:
        """Test MIDI file writing functionality."""
        import os
        import tempfile

        scale_stream = create_scale("C", "major")

        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as tmp:
            tmp_filename = tmp.name

        try:
            write_midi_file(scale_stream, tmp_filename, tempo=140)

            # Verify file was created
            assert os.path.exists(tmp_filename)
            assert os.path.getsize(tmp_filename) > 0  # File has content

            # Verify success message was printed
            mock_print.assert_called()
            printed_text = " ".join([str(call) for call in mock_print.call_args_list])
            assert tmp_filename in printed_text

        finally:
            # Clean up
            if os.path.exists(tmp_filename):
                os.unlink(tmp_filename)

    @patch("builtins.print")
    def test_write_midi_file_error_handling(self, mock_print) -> None:
        """Test error handling during MIDI file writing."""
        scale_stream = create_scale("C", "major")

        # Try to write to an invalid path
        invalid_path = "/nonexistent/directory/test.mid"

        with pytest.raises(Exception):
            write_midi_file(scale_stream, invalid_path)

        # Should print error message
        mock_print.assert_called()
        printed_text = " ".join([str(call) for call in mock_print.call_args_list])
        assert "Error writing MIDI file" in printed_text


class TestCLIArguments:
    """Test CLI argument handling."""

    def test_mode_validation(self) -> None:
        """Test that mode validation works correctly."""
        available_modes = [m.lower() for m in get_available_modes()]

        assert "major" in available_modes
        assert "minor" in available_modes
        assert "invalid_mode" not in available_modes

    def test_octave_parameter(self) -> None:
        """Test octave parameter in scale creation."""
        single_octave = create_scale("C", "major", octaves=1)
        double_octave = create_scale("C", "major", octaves=2)

        single_notes = len([n for n in single_octave.notes])
        double_notes = len([n for n in double_octave.notes])

        # Double octave should have more notes
        assert double_notes > single_notes
