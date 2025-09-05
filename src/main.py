import argparse
import sys

import pygame

from scales import create_scale, get_available_modes, print_scale_notes, write_midi_file


def play_midi(fname: str) -> None:
    pygame.init()
    pygame.mixer.music.load(fname)  # Load the MIDI file
    pygame.mixer.music.play()  # Start playback
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Limit CPU usage


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate musical scales and write them to MIDI files using mingus",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s C major output.mid                    # Write C major scale to output.mid
  %(prog)s F# minor f_sharp_minor.mid            # Write F# minor scale to file
  %(prog)s Bb dorian -o 2 dorian.mid            # Write Bb dorian scale over 2 octaves
  %(prog)s D pentatonicMajor -t 140 penta.mid   # Write D major pentatonic at 140 BPM
  %(prog)s --list-modes                          # Show available modes
        """,
    )

    parser.add_argument(
        "key", nargs="?", help="Root note of the scale (e.g., C, F#, Bb, D#)"
    )

    parser.add_argument(
        "mode",
        nargs="?",
        help="Scale mode (e.g., major, minor, dorian, pentatonicMajor)",
    )

    parser.add_argument(
        "output_file",
        nargs="?",
        help="Output MIDI filename (e.g., scale.mid, output.midi)",
    )

    parser.add_argument(
        "-o",
        "--octaves",
        type=int,
        default=1,
        help="Number of octaves to generate (default: 1)",
    )

    parser.add_argument(
        "-t",
        "--tempo",
        type=int,
        default=120,
        help="Playback tempo in BPM (default: 120)",
    )

    parser.add_argument(
        "--list-modes", action="store_true", help="List all available scale modes"
    )

    args = parser.parse_args()

    if args.list_modes:
        print("Available scale modes:")
        for mode in get_available_modes():
            print(f"  {mode}")
        return

    if not args.key or not args.mode or not args.output_file:
        parser.print_help()
        print("\nError: All three arguments (key, mode, output_file) are required.")
        return

    # Validate mode
    available_modes = [m.lower() for m in get_available_modes()]
    if args.mode.lower() not in available_modes:
        print(f"Error: '{args.mode}' is not a supported mode.")
        print("Use --list-modes to see available modes.")
        sys.exit(1)

    try:
        # Create the scale
        scale_track = create_scale(args.key, args.mode, args.octaves)

        # Print the scale notes
        print_scale_notes(scale_track, args.key, args.mode)

        # Write the scale to MIDI file
        write_midi_file(scale_track, args.output_file, args.tempo)

        # play_midi(args.output_file)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
