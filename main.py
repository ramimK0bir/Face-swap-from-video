import os
import shlex
import argparse
from module import faceSwap

def main():
    # Grab options from the environment variable "OPTIONS"
    options_str = os.environ.get("OPTIONS", "")
    # Use shlex.split to safely split the string into a list (handles quotes properly)
    args_list = shlex.split(options_str) if options_str else []

    parser = argparse.ArgumentParser(description="Face Swap from Image to Video")
    parser.add_argument("--source", required=True, help="Path to the source image")
    parser.add_argument("--target", required=True, help="Path to the target video")
    parser.add_argument("--output", required=True, help="Path to the output video")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second for output video")

    # Parse arguments from env OPTIONS
    args = parser.parse_args(args_list)

    # Prepend /input_output/ to paths
    args.source = os.path.join("/input_output", args.source)
    args.target = os.path.join("/input_output", args.target)
    args.output = os.path.join("/input_output", args.output)

    # Validate file paths
    if not os.path.isfile(args.source):
        print(f"Error: The source image path '{args.source}' is invalid or the file does not exist.")
        return
    
    if not os.path.isfile(args.target):
        print(f"Error: The target video path '{args.target}' is invalid or the file does not exist.")
        return
    
    # Validate output directory
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        print(f"Error: The output directory '{output_dir}' does not exist.")
        return

    # Print paths and settings
    print(f"Source Image Path: {args.source}")
    print(f"Target Video Path: {args.target}")
    print(f"FPS: {args.fps}")
    print(f"Output Video Path: {args.output}")

    # Run face swap
    try:
        editor = faceSwap.editor
        editor.swapFaceFromVideo(args.source, args.target, args.output, args.fps)
        print("Face swapping completed successfully!")
    except Exception as e:
        print(f"Error: An issue occurred during face swapping - {str(e)}")
        if "integer modulo b" in str(e):
            print("Tip: Try reducing --fps. If --fps is not used, try setting --fps equal to the source video's fps.")

# Standard Python entry point
if __name__ == "__main__":
    main()
