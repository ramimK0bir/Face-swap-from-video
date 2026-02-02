from module import faceSwap
import argparse
import os
import shlex

def main():
    # Read arguments from environment variable
    import os as os_env
    env_options = os_env.getenv("OPTIONS", "")
    args_list = shlex.split(env_options)  # safely split like shell arguments

    parser = argparse.ArgumentParser(description="DeepFake Face Swapper")
    
    parser.add_argument('--source', type=str, required=True, help='Path to the source image (face to swap in)')
    parser.add_argument('--target', type=str, required=True, help='Path to the target video (face to be replaced)')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second for output video')
    parser.add_argument('--output', type=str, default='output.mp4', help='Path to save the output video (default: output.mp4)')
    
    args = parser.parse_args(args_list)  # parse from env variable

    # Prepend /input_output/ to source, target, output paths
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
    
    # Validate the output directory or file path
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        print(f"Error: The output directory '{output_dir}' does not exist.")
        return
    
    print(f"Source Image Path: {args.source}")
    print(f"Target Video Path: {args.target}")
    print(f"FPS: {args.fps}")
    print(f"Output Video Path: {args.output}")
    
    try:
        editor = faceSwap.editor
        editor.swapFaceFromVideo(args.source, args.target, args.output, args.fps)
        print("Face swapping completed successfully!")
    except Exception as e:
        print(f"Error: An issue occurred during face swapping - {str(e)}")
        if "integer modulo b" in str(e):
            print("Try again after reducing --fps. If --fps not used, try --fps equal to source video fps.")

if __name__ == "__main__":
    main()
