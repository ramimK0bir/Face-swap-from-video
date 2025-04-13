DeepFake Face Swapper 

This project is a deepfake video face swapping tool that allows users to swap faces in video clips using deep learning techniques. It leverages computer vision and neural networks to create realistic face-swapped videos.



🚀 Features

        Face detection and alignment
        
        Identity extraction and transfer
        
        Realistic face swapping in videos
        
        Easy-to-use interface or script-based workflow
        
        GPU acceleration (if available)

🧠 Technologies Used

        Python 3.x
        
        OpenCV
        
        Dlib / face_recognition
        
        Deep learning (e.g., Autoencoders, GANs, or custom CNNs)
        
        FFmpeg (for video processing)
        
        PyTorch or TensorFlow (depending on your model)


📦 Installation


        
        It's will only run in google colab.
        
        !git clone https://github.com/ramimK0bir/Face-swap-from-video.git
        
        %cd Face-swap-from-video
        
        !pip install -r requirements.txt

🧪 Usage

        python main.py --source path/to/source.jpg --target path/to/target.mp4  --output path/to/output.mp4
        
🆘 Help

🛠️ Command-Line Arguments

        When running main.py, you can pass the following arguments to control how the face swapper behaves:

        Argument	Type	Required	Default	  Description
        --source	str	✅ Yes   	—	  Path to the source image file. This image contains the face to be swapped.
        --target	str	✅ Yes  	—	  Path to the target video file where the face will be replaced.
        --fps	int	❌ No	        30        Sets the frames per second for the output video. Useful to match original FPS.
        --output	str	❌ No	     output.mp4	  Path to save the output video.

        
👋 Instructions 

      --fps must be smaller or equal to target video fps 
      use colab.
[google Colab](https://colab.research.google.com)
        
