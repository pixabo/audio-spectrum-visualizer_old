import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from moviepy.editor import VideoFileClip, AudioFileClip
from matplotlib.patheffects import withStroke, SimpleLineShadow

def create_audio_visualization(audio_path, output_path='output.mp4', fps=30):
    # Load the audio file
    print("Loading audio file...")
    y, sr = librosa.load(audio_path)
    
    # Calculate the spectrogram with more temporal resolution
    print("Calculating spectrogram...")
    hop_length = int(sr/fps)  # Match hop length to frame rate
    D = librosa.feature.melspectrogram(
        y=y, 
        sr=sr, 
        n_mels=128,
        hop_length=hop_length
    )
    D_db = librosa.power_to_db(D, ref=np.max)
    
    # Create figure
    print("Setting up visualization...")
    fig = plt.figure(figsize=(12, 8))
    ax = plt.axes()
    
    # Set black background
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.set_axis_off()
    
    # Create lines with glow effects
    x = np.linspace(0, 100, 100)
    
    # Define colors for each wave
    wave_colors = [
        '#FF00FF',  # Magenta
        '#00FFFF',  # Cyan
        '#FF1493'   # Deep Pink
    ]
    
    lines = []
    for color in wave_colors:
        # Create multiple lines with different widths for glow effect
        widths = [4, 6, 8]
        alphas = [1.0, 0.6, 0.3]
        for w, a in zip(widths, alphas):
            line, = ax.plot([], [], color=color, lw=w, alpha=a)
            line.set_path_effects([
                SimpleLineShadow(offset=(0, 0), alpha=0.2),
                withStroke(linewidth=w+1, foreground='white', alpha=0.1)
            ])
            lines.append(line)
    
    # Set the plot limits
    ax.set_xlim(0, 100)
    ax.set_ylim(-2, 2)
    
    def get_wave_data(frame_data, frame, index):
        amplitude = np.mean(frame_data) * 2
        base_freq = 2 * np.pi / 100
        
        # Create more complex wave patterns
        wave = (
            amplitude * np.sin(x * base_freq * (index + 1) + frame/10) +
            amplitude/2 * np.sin(x * base_freq * 2 * (index + 1) + frame/5) +
            amplitude/4 * np.sin(x * base_freq * 4 * (index + 1) + frame/2.5)
        )
        return wave
    
    def animate(frame):
        if frame < D_db.shape[1]:
            # Get frequency data and normalize
            frame_data = D_db[:, frame]
            frame_data = (frame_data - frame_data.min()) / (frame_data.max() - frame_data.min())
            
            # Update each set of lines
            for i in range(len(wave_colors)):
                wave = get_wave_data(frame_data, frame, i)
                
                # Update all lines for this wave (including glow effects)
                for j in range(3):
                    line_idx = i * 3 + j
                    lines[line_idx].set_data(x, wave + 0.1*j)
        
        return lines
    
    # Create animation
    print("Creating animation...")
    anim = FuncAnimation(
        fig, 
        animate,
        frames=D_db.shape[1],
        interval=1000/fps,
        blit=True
    )
    
    # Save video with higher quality
    print("Saving video...")
    writer = animation.FFMpegWriter(fps=fps, bitrate=5000)
    anim.save('temp_video.mp4', writer=writer)
    plt.close()
    
    # Add audio with precise sync
    print("Adding audio...")
    video = VideoFileClip('temp_video.mp4')
    audio = AudioFileClip(audio_path)
    final_video = video.set_audio(audio)
    final_video.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac'
    )
    
    print(f"Video saved as {output_path}")

if __name__ == "__main__":
    audio_file = "test.m4a"
    create_audio_visualization(audio_file, 'visualization.mp4')
