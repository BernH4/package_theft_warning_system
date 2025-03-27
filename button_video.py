import time
import subprocess
import RPi.GPIO as GPIO
from picamera import PiCamera
from azure.storage.blob import BlobServiceClient
import json

def setup_gpio(button_pin):
    """Set up the GPIO pin for the button."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def initialize_camera():
    """Initialize and configure the camera."""
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.rotation = 0
    return camera

def record_video(camera, duration=5, filename='video.h264'):
    """Record a video using the PiCamera."""
    print("Button Pressed! Recording video for {} seconds...".format(duration))
    camera.start_recording(filename)
    time.sleep(duration)
    camera.stop_recording()
    print("Recording stopped. Video saved as '{}'".format(filename))
    return filename

def convert_video(input_file='video.h264', output_file='video.mp4'):
    """Convert the recorded .h264 video to .mp4 format using ffmpeg with reduced verbosity."""
    result = subprocess.run(
        ['ffmpeg', '-y', '-loglevel', 'warning', '-i', input_file, '-c:v', 'copy', output_file], 
        stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        print("FFmpeg error:", result.stderr.decode())
    else:
        print("Conversion complete. Video saved as '{}'".format(output_file))

def load_credentials(filename='credentials.json'):
    """Load storage credentials from a JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)

def upload_to_blob_storage(video_filename, credentials):
    """Upload video to Azure Blob Storage and return its URL."""
    blob_service_client = BlobServiceClient.from_connection_string(credentials["AZURE_STORAGE_CONNECTION_STRING"])
    container_client = blob_service_client.get_container_client(credentials["CONTAINER_NAME"])
    
    with open(video_filename, "rb") as data:
        blob_client = container_client.get_blob_client(video_filename)
        blob_client.upload_blob(data, overwrite=True)
    
    blob_url = f"{credentials['BLOB_BASE_URL']}/{credentials['CONTAINER_NAME']}/{video_filename}"
    print(f"Video uploaded successfully. Accessible at: {blob_url}")
    return blob_url

def main():
    BUTTON_PIN = 19  # Adjust as necessary
    setup_gpio(BUTTON_PIN)
    camera = initialize_camera()
    
    # Load credentials from external file
    credentials = load_credentials()
    
    print("Press the button...")
    try:
        #while True:
        #    if GPIO.input(BUTTON_PIN) == GPIO.LOW:
        video_file = record_video(camera)
        convert_video(video_file)
        video_url = upload_to_blob_storage("video.mp4", credentials)
        print(f"Video available at: {video_url}")
        time.sleep(0.2)  # Debounce delay
    finally:
        GPIO.cleanup()
        print("GPIO cleaned up.")

if __name__ == "__main__":
    main()