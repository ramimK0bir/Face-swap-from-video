from module import faceSwap
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="DeepFake Face Swapper")
    
    parser.add_argument('--source', type=str, required=True, help='Path to the source image (face to swap in)')
    parser.add_argument('--target', type=str, required=True, help='Path to the target video (face to be replaced)')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second for output video')
    
    args = parser.parse_args()

    print(f"Source Image Path: {args.source}")
    print(f"Target Video Path: {args.target}")
    print(f"FPS: {args.fps}")
    editor=faceSwap.editor
    editor.swapFaceFromVideo( args.source , args.target ,args.fps)
if __name__ == "__main__":
    main()
