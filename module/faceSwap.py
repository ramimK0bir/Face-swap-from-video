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
            print(f"\r{  int((self.numberOfImagesSwaped/self.numberOfImages)*100)} % done ... t{self.numberOfImages} d{self.numberOfImagesSwaped}" ,end="")
  
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
        with self.ThreadPoolExecutor(max_workers=15) as executor:
            futures = [
                executor.submit(self.processImage, file, sourcePath, face2)
                for file in image_files
            ]
            for future in futures:
                future.result()

    def videoToImages(self,videoPath, outputFolder, fps=30):
        self.os.makedirs(outputFolder, exist_ok=True)
        cap = self.cv2.VideoCapture(videoPath)
        if not cap.isOpened():
            return {'status': 'error', 'message': 'Failed to open video file.'}
        video_fps = cap.get(self.cv2.CAP_PROP_FPS)
        frame_interval = int(video_fps / fps)
        frame_count = 0
        saved_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % frame_interval == 0:
                output_path = self.os.path.join(outputFolder, f'{saved_count:09}.jpg')
                self.cv2.imwrite(output_path, frame)
                saved_count += 1
            frame_count += 1

        cap.release()
        self.numberOfImages=saved_count
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

    def interpolate_frame(self,frame1, frame2, alpha):
        gray1 = self.cv2.cvtColor(frame1, self.cv2.COLOR_BGR2GRAY)
        gray2 = self.cv2.cvtColor(frame2, self.cv2.COLOR_BGR2GRAY)
        flow = self.cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        h, w = gray1.shape[:2]
        flow_map_x, flow_map_y = self.np.meshgrid(self.np.arange(w), self.np.arange(h))
        flow_map = self.np.stack((flow_map_x, flow_map_y), axis=-1).astype(self.np.float32)
        intermediate_flow1 = flow_map - alpha * flow
        intermediate_flow2 = flow_map + (1 - alpha) * flow
        warp1 = self.cv2.remap(frame1, intermediate_flow1[..., 0], intermediate_flow1[..., 1], interpolation=self.cv2.INTER_LINEAR)
        warp2 = self.cv2.remap(frame2, intermediate_flow2[..., 0], intermediate_flow2[..., 1], interpolation=self.cv2.INTER_LINEAR)
        
        interpolated_frame = self.cv2.addWeighted(warp1, 1 - alpha, warp2, alpha, 0)
        return interpolated_frame

    def increase_fps_with_interpolation(self,input_video_path, output_video_path, scale_factor):
        cap = self.cv2.VideoCapture(input_video_path)
        fps = int(cap.get(self.cv2.CAP_PROP_FPS))
        width = int(cap.get(self.cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(self.cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = self.cv2.VideoWriter_fourcc(*'mp4v')
        new_fps = int(fps * scale_factor)

        out = self.cv2.VideoWriter(output_video_path, fourcc, new_fps, (width, height))
        ret, prev_frame = cap.read()
        if not ret:
            print("Error reading the video.")
            return
        while True:
            ret, next_frame = cap.read()
            if not ret:
                break
            out.write(prev_frame)
            for i in range(1, int(scale_factor)):
                alpha = i / scale_factor
                interpolated_frame = self.interpolate_frame(prev_frame, next_frame, alpha)
                out.write(interpolated_frame.astype(self.np.uint8))
            prev_frame = next_frame
        out.write(prev_frame)
        cap.release()
        out.release()











    # def addAudioToVideo(self, video_path, audio_source_path, output_path,
    #                     crf=23, preset="medium", audio_codec="aac", strict="experimental"):
    #     try:
    #         command = [
    #             'ffmpeg',
    #             '-y',  # Overwrite output
    #             '-i', video_path,
    #             '-i', audio_source_path,
    #             '-c:v', 'libx264',         # Compress video
    #             '-crf', str(crf),          # Quality setting
    #             '-preset', preset,         # Compression speed
    #             '-c:a', audio_codec,       # Audio codec
    #             '-strict', strict,         # Compatibility flag
    #             output_path
    #         ]
    
    #         self.subprocess.run(command, check=True)
    #         print(f"\nSuccessfully added audio and compressed video. Output saved at '{output_path}'.")
    
    #     except self.subprocess.CalledProcessError as e:
    #         raise ValueError(f"FFmpeg processing failed: {e}. \nVideo saved as {video_path} without any audio.")
    #     except Exception as e:
    #         raise ValueError(f"Unexpected error: {e}")
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
            raise ValueError(f"FFmpeg processing failed: {e}. \nvideo saved as {video_path} withut any audio.")
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
