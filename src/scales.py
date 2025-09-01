"""Musical scales module for generating and working with various musical scales."""

from typing import List, Literal

from music21 import duration, note, pitch, scale, stream

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


def create_scale(key: str, mode: str, octaves: int = 1) -> stream.Stream:
    """
    Create a scale using music21.

    Args:
        key: The root note (e.g., 'C', 'F#', 'Bb')
        mode: The scale mode
        octaves: Number of octaves to generate

    Returns:
        music21 Stream containing the scale
    """
    try:
        # Validate inputs
        validated_key = validate_key(key)
        validated_mode = validate_mode(mode)

        # Create the scale object
        if validated_mode.lower() == "major":
            sc = scale.MajorScale(validated_key)
        elif validated_mode.lower() == "minor":
            sc = scale.MinorScale(validated_key)
        elif validated_mode.lower() == "dorian":
            sc = scale.DorianScale(validated_key)
        elif validated_mode.lower() == "phrygian":
            sc = scale.PhrygianScale(validated_key)
        elif validated_mode.lower() == "lydian":
            sc = scale.LydianScale(validated_key)
        elif validated_mode.lower() == "mixolydian":
            sc = scale.MixolydianScale(validated_key)
        elif validated_mode.lower() == "locrian":
            sc = scale.LocrianScale(validated_key)
        elif validated_mode.lower() == "melodicminor":
            sc = scale.MelodicMinorScale(validated_key)
        elif validated_mode.lower() == "harmonicminor":
            sc = scale.HarmonicMinorScale(validated_key)
        elif validated_mode.lower() == "pentatonicmajor":
            # Create major pentatonic manually: 1, 2, 3, 5, 6
            from music21.scale import ConcreteScale

            sc = ConcreteScale(tonic=validated_key, pitches=["C", "D", "E", "G", "A"])
            if validated_key != "C":
                major_scale = scale.MajorScale(validated_key)
                pentatonic_pitches = [major_scale.pitches[i] for i in [0, 1, 2, 4, 5]]
                sc = ConcreteScale(
                    tonic=validated_key, pitches=[str(p) for p in pentatonic_pitches]
                )
        elif validated_mode.lower() == "pentatonicminor":
            # Create minor pentatonic manually: 1, b3, 4, 5, b7
            from music21.scale import ConcreteScale

            minor_scale = scale.MinorScale(validated_key)
            pentatonic_pitches = [minor_scale.pitches[i] for i in [0, 2, 3, 4, 6]]
            sc = ConcreteScale(
                tonic=validated_key, pitches=[str(p) for p in pentatonic_pitches]
            )
        elif validated_mode.lower() == "blues":
            # Create blues scale manually: 1, b3, 4, b5, 5, b7
            from music21 import interval
            from music21.scale import ConcreteScale

            tonic_pitch = pitch.Pitch(validated_key)
            blues_intervals = ["P1", "m3", "P4", "d5", "P5", "m7"]
            blues_pitches = [
                tonic_pitch.transpose(interval.Interval(i)) for i in blues_intervals
            ]
            sc = ConcreteScale(
                tonic=validated_key, pitches=[str(p) for p in blues_pitches]
            )
        elif validated_mode.lower() == "chromatic":
            sc = scale.ChromaticScale(validated_key)
        elif validated_mode.lower() == "wholetone":
            sc = scale.WholeToneScale(validated_key)
        elif validated_mode.lower() == "octatonic":
            sc = scale.OctatonicScale(validated_key)
        else:
            # This should never happen due to validate_mode, but keeping for safety
            raise ValueError(f"Unsupported scale mode: {mode}")

        # Create a stream with the scale notes
        s = stream.Stream()

        for octave in range(octaves):
            scale_pitches = sc.getPitches()
            # Use only the first 7 pitches (exclude the octave tonic)
            for p in scale_pitches[:-1]:  # Exclude the last pitch (octave tonic)
                # Adjust octave
                new_pitch = pitch.Pitch(p.name)
                new_pitch.octave = 4 + octave
                n = note.Note(new_pitch, duration=duration.Duration(0.5))
                s.append(n)

        # Add final tonic note one octave higher (only once)
        if hasattr(sc, "tonic") and sc.tonic is not None:
            final_pitch = pitch.Pitch(sc.tonic.name)
            final_pitch.octave = 4 + octaves
            s.append(note.Note(final_pitch, duration=duration.Duration(1.0)))

        return s

    except Exception as e:
        raise ValueError(f"Error creating scale: {e}")


def write_midi_file(
    scale_stream: stream.Stream, filename: str, tempo: int = 120
) -> None:
    """
    Write a scale to a MIDI file.

    Args:
        scale_stream: The music21 Stream to write
        filename: Output MIDI filename
        tempo: Tempo in BPM
    """
    try:
        # Set tempo
        from music21.tempo import MetronomeMark

        metronome = MetronomeMark(number=tempo)
        scale_stream.insert(0, metronome)

        # Write to MIDI file
        scale_stream.write("midi", fp=filename)
        print(f"MIDI file written to: {filename}")

    except Exception as e:
        print(f"Error writing MIDI file: {e}")
        raise


def print_scale_notes(scale_stream: stream.Stream, key: str, mode: str) -> None:
    """
    Print the notes in the scale.

    Args:
        scale_stream: The music21 Stream containing the scale
        key: The root note
        mode: The scale mode
    """
    notes = []
    for element in scale_stream.notes:
        if isinstance(element, note.Note) and element.pitch is not None:
            notes.append(str(element.pitch))

    print(f"\n{key} {mode.title()} Scale:")
    print("Notes:", " - ".join(notes))
    print()
