from module import faceSwap
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="DeepFake Face Swapper")
    
    parser.add_argument('--source', type=str, required=True, help='Path to the source image (face to swap in)')
    parser.add_argument('--target', type=str, required=True, help='Path to the target video (face to be replaced)')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second for output video')
    parser.add_argument('--output', type=str, default='output.mp4', help='Path to save the output video (default: output.mp4)')
    
    args = parser.parse_args()

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
            print("try again after reducing --fps.if --fps not used then try --fps {source video fps}.")
if __name__ == "__main__":
    main()
