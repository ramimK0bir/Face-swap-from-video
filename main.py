import os
import time
import threading
LOG_FILE = "internal_logs.log"

def follow_log(file_path=LOG_FILE, interval=10):
    """
    Continuously print new lines appended to the log file, checking every `interval` seconds.
    """
    with open(file_path, "r") as f:
        # Move to the end of file
        f.seek(0, os.SEEK_END)
        while True:
            lines = f.readlines()  # Read any new lines
            if lines:
                for line in lines:
                    if line.strip()=="exit" :
                        return 
                    print(line, end="")  # Already has newline
            time.sleep(interval)  # Wait before checking again

threading.Thread(target=follow_log).start()
def write_log(message):
    """
    Write a message to the log file immediately.
    """
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")
        f.flush() 





class videoEditor :


    def __init__(self):
        import urllib
        from tqdm import tqdm
        import os
        import subprocess
        import cv2
        import numpy as np
        import insightface
        from insightface.app import FaceAnalysis
        from concurrent.futures import ThreadPoolExecutor
        self.os=os
        self.urllib=urllib
        self.tqdm=tqdm
        self.subprocess=subprocess
        self.np=np
        self.cv2=cv2
        self.numberOfImages=0
        self.numberOfImagesSwaped=0
        self.insightface=insightface
        self.ThreadPoolExecutor=ThreadPoolExecutor
        self.app = FaceAnalysis()
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        self.conditional_download('./models', ['https://huggingface.co/CountFloyd/deepfake/resolve/main/inswapper_128.onnx'])
        self.swapper = insightface.model_zoo.get_model('./models/inswapper_128.onnx', download=False)
    def conditional_download(self,download_directory_path: str, urls: list [str]) -> None:
          if not self.os.path.exists(download_directory_path):
              self.os.makedirs(download_directory_path)
          for url in urls:
              download_file_path = self.os.path.join(download_directory_path, self.os.path.basename(url))
              if not self.os.path.exists(download_file_path):
                  request = self.urllib.request.urlopen(url)  # type: ignore[attr-defined]
                  total = int(request.headers.get('Content-Length', 0))
                  with self.tqdm(total=total, desc='Downloading', unit='B', unit_scale=True, unit_divisor=1024) as progress:
                      self.urllib.request.urlretrieve(url, download_file_path, reporthook=lambda count, block_size, total_size: progress.update(block_size))  # type: ignore[attr-defined]
 
    def swapImage(self,baseImage, face ,outputImage):
        img1 = self.cv2.imread(baseImage)
        face1 = self.app.get(img1)
        if face1 :
            face1=face1[0]
        else :
            return
        swapped_img = self.swapper.get(img1, face1, face)
        self.cv2.imwrite(outputImage, swapped_img)
        if (self.numberOfImagesSwaped < int(outputImage.split('/')[-1][0:9]) ):
            self.numberOfImagesSwaped =int(outputImage.split('/')[-1][0:9])
            log_msg=f"{  int((self.numberOfImagesSwaped/self.numberOfImages)*100)} % done ... t{self.numberOfImages} d{self.numberOfImagesSwaped}"
            write_log(log_msg)
  
    def processImage(self,file, sourcePath , face):
        sourcePath=sourcePath.replace('/','')
        img_path = f'{sourcePath }/{file}'
        self.swapImage(img_path, face,img_path)
    def swapAll(self,sourceImage, sourcePath):
        img2 = self.cv2.imread(sourceImage)
        face2 = self.app.get(img2)[0]
        image_files = sorted(
            [f for f in self.os.listdir(sourcePath) if f.endswith(('.jpg', '.png'))]
        )
        sourcePath = sourcePath.rstrip('/')  
        with self.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(self.processImage, file, sourcePath, face2)
                for file in image_files
            ]
            for future in futures:
                future.result()















    
    def videoToImages(self, videoPath, outputFolder, fps=30):
        self.os.makedirs(outputFolder, exist_ok=True)
        cap = self.cv2.VideoCapture(videoPath)
        
        if not cap.isOpened():
            return {'status': 'error', 'message': 'Failed to open video file.'}
        
        video_fps = cap.get(self.cv2.CAP_PROP_FPS)
        if video_fps <= 0:
            cap.release()
            return {'status': 'error', 'message': 'Could not determine video FPS.'}
        
        frame_interval = video_fps / fps
        frame_count = 0
        saved_count = 0
        next_capture_frame = 0.0
    
        while True:
            ret, frame = cap.read()
            if not ret:
                break
    
            if frame_count >= next_capture_frame:
                output_path = self.os.path.join(outputFolder, f'{saved_count:09}.jpg')
                self.cv2.imwrite(output_path, frame)
                saved_count += 1
                next_capture_frame += frame_interval
    
            frame_count += 1
    
        cap.release()
        self.numberOfImages = saved_count
        return {'status': 'success', 'saved_images': saved_count, 'output_folder': outputFolder}
    













    

    

    def imagesToVideo(self, outputVideoPath,imagesFolder, fps=30):
        image_files = sorted(
            [f for f in self.os.listdir(imagesFolder) if f.endswith(('.jpg', '.png'))]
        )
        if not image_files:
            return {'status': 'error', 'message': 'No images found in the specified folder.'}

        first_image = self.cv2.imread(self.os.path.join(imagesFolder, image_files[0]))
        height, width, layers = first_image.shape
        fourcc = self.cv2.VideoWriter_fourcc(*'mp4v')
        out = self.cv2.VideoWriter(outputVideoPath, fourcc, fps, (width, height))

        for image_file in image_files:
            image_path = self.os.path.join(imagesFolder, image_file)
            frame = self.cv2.imread(image_path)
            out.write(frame)

        out.release()
        return {'status': 'success', 'output_video_path': outputVideoPath, 'total_frames': len(image_files)}

    def addAudioToVideo(self, video_path, audio_source_path, output_path, video_codec="copy", audio_codec="aac", strict="experimental"):
        try:
            command = [
                'ffmpeg',
                '-y',  # force overwrite
                '-i', video_path,
                '-i', audio_source_path,
                '-c:v', video_codec,
                '-c:a', audio_codec,
                '-strict', strict,
                output_path
            ]

            self.subprocess.run(command, check=True)
            print(f"\nSuccessfully added audio from '{audio_source_path}' to video '{video_path}'. Output saved at '{output_path}'.")
        except self.subprocess.CalledProcessError as e:
            raise ValueError(f"FFmpeg processing failed: {e}. \nvideo saved as {video_path} without any audio.")
        except Exception as e:
            raise ValueError(f"Unexpected error: {e}")


    
                        

    def cleanup(self,path :str):
        if self.os.path.exists(path):
            for root, dirs, files in self.os.walk(path, topdown=False):
                for file in files:
                    self.os.remove(self.os.path.join(root, file))
                for dir in dirs:
                    self.os.rmdir(self.os.path.join(root, dir))
            self.os.rmdir(path)
        else:
            print("Folder does not exist.")
    def swapFaceFromVideo( self,faceImage,videoPath, outputPath ,videoFps):
        self.videoToImages(videoPath , 'images/',fps=videoFps)
        self.swapAll(faceImage, 'images/')
        self.imagesToVideo('internalOutput.mp4','images/',fps=videoFps)
        self.addAudioToVideo('internalOutput.mp4' , videoPath , outputPath)
        self.os.remove('internalOutput.mp4')
        self.cleanup("images/")
        print(f"\n\noutput video saved as {self.os.path.abspath(outputPath)}")

editor=videoEditor()



























import shlex
import argparse

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
        editor.swapFaceFromVideo(args.source, args.target, args.output, args.fps)
        print("Face swapping completed successfully!")
    except Exception as e:
        print(f"Error: An issue occurred during face swapping - {str(e)}")
        if "integer modulo b" in str(e):
            print("Tip: Try reducing --fps. If --fps is not used, try setting --fps equal to the source video's fps.")

# Standard Python entry point
if __name__ == "__main__":
    main()
