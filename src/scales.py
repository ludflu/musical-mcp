"""Musical scales module for generating and working with various musical scales."""

from typing import List, Literal, Tuple

from mingus.containers import Bar, Note, Track
from mingus.core import intervals, notes, scales
from mingus.midi import midi_file_out

# Type definitions for allowed values
ScaleMode = Literal[
    "major",
    "minor",
    "dorian",
    "phrygian",
    "lydian",
    "mixolydian",
    "locrian",
    "melodicMinor",
    "harmonicMinor",
    "pentatonicMajor",
    "pentatonicMinor",
    "blues",
    "chromatic",
    "wholeTone",
    "octatonic",
]

# Since music21 is flexible with key input (accepts various formats like 'C', 'C#', 'Bb', etc.)
# and we want to maintain CLI flexibility, we'll keep key as str but add a type alias for clarity
MusicalKey = str  # Could be "C", "F#", "Bb", "D#", etc.


def get_available_modes() -> List[ScaleMode]:
    """Get list of available scale modes from music21."""
    return [
        "major",
        "minor",
        "dorian",
        "phrygian",
        "lydian",
        "mixolydian",
        "locrian",
        "melodicMinor",
        "harmonicMinor",
        "pentatonicMajor",
        "pentatonicMinor",
        "blues",
        "chromatic",
        "wholeTone",
        "octatonic",
    ]


def validate_mode(mode: str) -> ScaleMode:
    """Validate and return a scale mode, raising ValueError if invalid."""
    available_modes = get_available_modes()
    mode_lower = mode.lower()

    for available_mode in available_modes:
        if mode_lower == available_mode.lower():
            return available_mode

    raise ValueError(f"Unsupported scale mode: {mode}")


def validate_key(key: str) -> str:
    """Validate a musical key. For now, just return as-is since music21 handles validation."""
    # music21 is quite flexible with key inputs, so we'll let it handle validation
    return key


def create_scale(key: str, mode: str, octaves: int = 1) -> Track:
    """
    Create a scale using mingus.

    Args:
        key: The root note (e.g., 'C', 'F#', 'Bb')
        mode: The scale mode
        octaves: Number of octaves to generate

    Returns:
        mingus Track containing the scale
    """
    try:
        # Validate inputs
        validated_key = validate_key(key)
        validated_mode = validate_mode(mode)

        # Convert flat notation (Bb -> A#) for mingus compatibility
        if "b" in validated_key:
            validated_key = notes.diminish(validated_key.replace("b", ""))

        # Get scale notes using mingus
        scale_notes = []

        if validated_mode.lower() == "major":
            scale_notes = scales.Major(validated_key).ascending()
        elif validated_mode.lower() == "minor":
            scale_notes = scales.NaturalMinor(validated_key).ascending()
        elif validated_mode.lower() == "dorian":
            scale_notes = scales.Dorian(validated_key).ascending()
        elif validated_mode.lower() == "phrygian":
            scale_notes = scales.Phrygian(validated_key).ascending()
        elif validated_mode.lower() == "lydian":
            scale_notes = scales.Lydian(validated_key).ascending()
        elif validated_mode.lower() == "mixolydian":
            scale_notes = scales.Mixolydian(validated_key).ascending()
        elif validated_mode.lower() == "locrian":
            scale_notes = scales.Locrian(validated_key).ascending()
        elif validated_mode.lower() == "melodicminor":
            scale_notes = scales.MelodicMinor(validated_key).ascending()
        elif validated_mode.lower() == "harmonicminor":
            scale_notes = scales.HarmonicMinor(validated_key).ascending()
        elif validated_mode.lower() == "pentatonicmajor":
            # Major pentatonic: 1, 2, 3, 5, 6
            major_scale = scales.Major(validated_key).ascending()
            scale_notes = [major_scale[i] for i in [0, 1, 2, 4, 5]]
        elif validated_mode.lower() == "pentatonicminor":
            # Minor pentatonic: 1, b3, 4, 5, b7
            minor_scale = scales.NaturalMinor(validated_key).ascending()
            scale_notes = [minor_scale[i] for i in [0, 2, 3, 4, 6]]
        elif validated_mode.lower() == "blues":
            # Blues scale: manually create it (1, b3, 4, b5, 5, b7)
            # Start with natural minor and add the b5
            minor_scale = scales.NaturalMinor(validated_key).ascending()
            scale_notes = [
                minor_scale[0],
                minor_scale[2],
                minor_scale[3],
                notes.diminish(minor_scale[4]),
                minor_scale[4],
                minor_scale[6],
            ]
        elif validated_mode.lower() == "chromatic":
            scale_notes = scales.Chromatic(validated_key).ascending()
        elif validated_mode.lower() == "wholetone":
            scale_notes = scales.WholeTone(validated_key).ascending()
        elif validated_mode.lower() == "octatonic":
            scale_notes = scales.Octatonic(validated_key).ascending()
        else:
            raise ValueError(f"Unsupported scale mode: {mode}")

        # Create a mingus Track with the scale notes
        track = Track()
        bar = Bar()

        for octave in range(octaves):
            for note_name in scale_notes[:-1]:  # Exclude octave tonic
                octave_note = f"{note_name}-{4 + octave}"
                note_obj = Note(octave_note)
                if not bar.place_notes(note_obj, 8):  # Eighth note duration
                    track.add_bar(bar)
                    bar = Bar()
                    bar.place_notes(note_obj, 8)

        # Add final tonic note one octave higher
        final_note = Note(f"{validated_key}-{4 + octaves}")
        if not bar.place_notes(final_note, 4):  # Quarter note
            track.add_bar(bar)
            bar = Bar()
            bar.place_notes(final_note, 4)

        # Add the final bar if it has content
        if len(bar) > 0:
            track.add_bar(bar)

        return track

    except Exception as e:
        raise ValueError(f"Error creating scale: {e}")


def write_midi_file(scale_track: Track, filename: str, tempo: int = 120) -> None:
    """
    Write a scale to a MIDI file.

    Args:
        scale_track: The mingus Track to write
        filename: Output MIDI filename
        tempo: Tempo in BPM
    """
    try:
        # Write to MIDI file using mingus
        midi_file_out.write_Track(filename, scale_track, tempo)
        print(f"MIDI file written to: {filename}")

    except Exception as e:
        print(f"Error writing MIDI file: {e}")
        raise


def print_scale_notes(scale_track: Track, key: str, mode: str) -> None:
    """
    Print the notes in the scale.

    Args:
        scale_track: The mingus Track containing the scale
        key: The root note
        mode: The scale mode
    """
    notes = []
    for bar in scale_track:
        for beat in bar:
            if beat[2]:  # If there are notes in this beat
                for note in beat[2]:
                    if hasattr(note, "name"):
                        notes.append(note.name)
                    elif isinstance(note, str):
                        notes.append(note)
                    else:
                        notes.append(str(note))

    print(f"\n{key} {mode.title()} Scale:")
    print("Notes:", " - ".join(notes))
    print()
