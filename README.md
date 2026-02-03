# DeepFake Face Swapper 

### This project is a deepfake video face swapping tool that allows users to swap faces in video clips using deep learning techniques. It leverages computer vision and neural networks to create realistic swapped faces in videos.

Got it—keeping it **super simple and clear**:


# ⚠️ Python Version ⚠️

## **Use Python 3.8 to 3.11 ONLY**


## 🚀 Features

    Face detection and alignment
    Identity extraction and transfer
    Realistic face swapping in videos
    Easy-to-use interface or script-based workflow
    GPU acceleration (if available)

## 🧠 Technologies Used

    Python 3.8
    OpenCV
    Dlib / face_recognition
    Deep learning (e.g., Autoencoders, GANs, or custom CNNs)
    FFmpeg (for video processing)
    PyTorch or TensorFlow (depending on your model)

## 📦 Installation

  ### For [google Colab](https://colab.research.google.com) .
  #### Ensure you're running this in a Google Colab environment for optimal performance.
    !git clone https://github.com/ramimK0bir/Face-swap-from-video.git
    %cd Face-swap-from-video
    !pip install -r requirements.txt

### Additional settings for cuda execution .
#### Make sure you're running it with cuda GPU.
    !pip uninstall onnxruntime -y
    !pip install onnxruntime-gpu
  ### For Regular Linux System
  
    sudo apt install ffmpeg -y
    git clone https://github.com/ramimK0bir/Face-swap-from-video.git
    cd Face-swap-from-video
    pip install -r requirements.txt
### Additional settings for cuda execution .
#### Make sure you're running it with cuda GPU.
    pip uninstall onnxruntime -y
    pip install onnxruntime-gpu

## 🧪 Usage

  ### For [google Colab](https://colab.research.google.com) .
  
    !python main.py --source testing/new.jpg --target testing/testing.mp4  --output output.mp4 --fps 30
    
  ### For Regular Linux System
  
    python main.py --source testing/new.jpg --target testing/testing.mp4  --output output.mp4 --fps 30
    
## 🆘 Help

### 🛠️ Command-Line Arguments

        When running main.py, you can pass the following arguments to control how the face swapper behaves:

        Argument	Type	Required	Default	  Description
        --source	str	✅ Yes    	—	  Path to the source image file. This image contains the face to be swapped.
        --target	str	✅ Yes   	—	  Path to the target video file where the face will be replaced.
        --fps	    int	❌ No	        30        Sets the frames per second for the output video. Useful to match original FPS.
        --output	str	❌ No	     output.mp4	  Path to save the output video.



        
## 👋 Instructions 

      --fps must be smaller or equal to target video fps 
      use colab.
[google Colab](https://colab.research.google.com)

```

````markdown
## Docker Usage

1. **Prepare input/output folder:**
```bash
mkdir -p ./input_output
````

2. **Move your source files into `input_output`:**
   Place the source image and target video inside the folder before running the container. For example:

```bash
mv new.jpg ./input_output/
mv testing.mp4 ./input_output/
```

3. **Run Docker container with a name:**
   This uses the *exact same* options as the main branch CLI (`main.py --source ... --target ... --output ... --fps ...`). ([GitHub][1])

```bash
docker run --name face_swap_job \
  -v ./input_output:/input_output \
  -e OPTIONS="--source new.jpg --target testing.mp4 --output result.mp4 --fps 30" \
  useranonymous/face_swap_from_video:0.0.1
```

4. **Monitor progress (optional — shows CMD output):**

```bash
docker logs -f face_swap_job
```

* Running in foreground like above shows live progress (downloads, processing etc.).

5. **Remove container after completion:**

```bash
docker rm face_swap_job
```

**Notes:**

* All outputs are automatically stored in `./input_output`.
* Ensure your source image and target video are in the `input_output` folder before running.
* Use the **same option names** as in the main branch CLI (`--source`, `--target`, `--output`, `--fps`).

---
        
## Demo testing 
![Face Swap Demo](https://github.com/ramimK0bir/Face-swap-from-video/blob/main/testing/test.gif?raw=true)


## Credit 

### used technologies 
[Insightface](https://github.com/deepinsight/insightface)
[FFmpeg](https://github.com/FFmpeg/FFmpeg)

### used content on testing
Lady Gaga -> image , [testing source video](https://www.youtube.com/@albertatech)



# Face Swap from Video

This project provides a tool for swapping faces within video content using machine learning and AI technologies. It is intended for responsible use in creative, research, and educational settings.

## Ethical Use Guidelines

1. **Consent**: Always ensure that individuals whose faces are being swapped have given explicit, informed consent for their likeness to be used.
   
2. **Transparency**: Clearly inform others that face-swapping technology has been used in your video or content to avoid confusion and the spread of misleading content.
   
3. **Non-Exploitation**: Do not use this tool to create content that could harm, harass, or exploit others, including impersonating individuals or spreading false information.

4. **Legal Compliance**: Follow the laws regarding privacy, copyright, and data protection in your jurisdiction. Face-swapping without consent may be illegal depending on local regulations.

## Disclaimer

The developer of this project **does not** take responsibility for any misuse of the tool, including, but not limited to, the creation of misleading, harmful, or illegal content. Users of this project are solely responsible for compliance with all applicable laws and regulations.
```
