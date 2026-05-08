

class FaceNotFoundError(Exception):
    "Face not found"


class videoEditor:
    def __init__(self):
        import urllib
        from tqdm import tqdm
        import os
        import subprocess
        import cv2
        import insightface
        from insightface.app import FaceAnalysis
        self.os = os
        self.urllib = urllib
        self.tqdm = tqdm
        self.subprocess = subprocess
        self.cv2 = cv2
        self.insightface = insightface
        self.app = FaceAnalysis()
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        self.conditional_download('./models',
                                  ['https://huggingface.co/CountFloyd/deepfake/resolve/main/inswapper_128.onnx'])
        self.swapper = insightface.model_zoo.get_model('./models/inswapper_128.onnx', download=False)

    def conditional_download(self, download_directory_path: str, urls: list[str]) -> None:
        if not self.os.path.exists(download_directory_path):
            self.os.makedirs(download_directory_path)
        for url in urls:
            download_file_path = self.os.path.join(download_directory_path, self.os.path.basename(url))
            if not self.os.path.exists(download_file_path):
                request = self.urllib.request.urlopen(url)  # type: ignore[attr-defined]
                total = int(request.headers.get('Content-Length', 0))
                with self.tqdm(total=total, desc='Downloading', unit='B', unit_scale=True,
                               unit_divisor=1024) as progress:
                    self.urllib.request.urlretrieve(url, download_file_path,
                                                    reporthook=lambda count, block_size, total_size: progress.update(
                                                        block_size))

    def addAudioToVideo(self, video_path, audio_source_path, output_path, video_codec="copy", audio_codec="aac",
                        strict="experimental"):
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
            print(
                f"\nSuccessfully added audio from '{audio_source_path}' to video '{video_path}'. Output saved at '{output_path}'.")
        except self.subprocess.CalledProcessError as e:
            raise ValueError(f"FFmpeg processing failed: {e}. \nvideo saved as {video_path} without any audio.")
        except Exception as e:
            raise ValueError(f"Unexpected error: {e}")

    def swap_from_frame(self, frame):

        print(f"\r{int((self.done_fps / self.total_fps) * 100)} % done ... t{self.total_fps} d{self.done_fps}", end="")

        face1 = self.app.get(frame)
        if face1:
            face1 = face1[0]
        else:
            return
        frame = self.swapper.get(frame, face1, self.sourceFaces)

        self.done_fps += 1

    def swap_all_faces_from_video(self, face_image, input_video, output_video, fps):
        cv2 = self.cv2
        img2 = self.cv2.imread(face_image)
        self.sourceFaces = self.app.get(img2)
        if self.sourceFaces:
            self.sourceFaces = self.sourceFaces[0]
        else:
            raise FaceNotFoundError(f"No face found in {face_image}.")
        cap = cv2.VideoCapture(input_video)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
        duration_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
        if fps > video_fps:
            fps = video_fps
        total_frames = int((duration_ms / 1000) * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.total_fps = total_frames + 1
        self.done_fps = 1
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
        frame_interval = video_fps / fps
        frame_count = 0
        next_frame = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count >= next_frame:
                self.swap_from_frame(frame)
                out.write(frame)
                next_frame += frame_interval
            frame_count += 1
        cap.release()
        out.release()

    def swapFaceFromVideo(self, faceImage, videoPath, outputPath, videoFps):

        self.swap_all_faces_from_video(faceImage, videoPath, 'internalOutput.mp4', videoFps)
        self.addAudioToVideo(f'internalOutput.mp4', videoPath, outputPath)
        self.os.remove(f'internalOutput.mp4')
        print(f"\n\noutput video saved as {self.os.path.abspath(outputPath)}")


editor = videoEditor()






