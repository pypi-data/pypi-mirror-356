"""
Command line interface for pdf2gif library.
"""

import argparse
import sys
from . import convert_pdf_to_gif


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Convert PDF files to animated GIFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdf2gif presentation.pdf
  pdf2gif document.pdf --frame-delay 200
  pdf2gif slides.pdf --first-slide-multiplier 5 --frame-delay 100
        """
    )
    
    parser.add_argument(
        "pdf_filename",
        help="Path to the input PDF file"
    )
    
    parser.add_argument(
        "--frame-delay",
        type=int,
        default=150,
        help="Frame delay in milliseconds (default: 150)"
    )
    
    parser.add_argument(
        "--first-slide-multiplier",
        type=int,
        default=10,
        help="Number of times to repeat the first slide (default: 10)"
    )
    
    args = parser.parse_args()
    
    try:
        gif_filename = convert_pdf_to_gif(
            args.pdf_filename,
            frame_delay=args.frame_delay,
            first_slide_multiplier=args.first_slide_multiplier
        )
        print(f"Successfully created: {gif_filename}")
        
    except FileNotFoundError:
        print(f"Error: File '{args.pdf_filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 