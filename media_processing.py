from PIL import Image
import cv2

SUPPORTED_FILE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


def convert_webp_to_gif(input_path: str) -> str:
    """Convert a WebP file to a GIF file."""
    # Convert the WebP file to a GIF file
    im = Image.open(input_path)
    new_path = input_path.split('.')[0] + '.gif'
    im.info.pop('background', None)
    im.save(new_path, 'gif', save_all=True)
    return new_path


def get_screenshot_from_mp4(input_path: str) -> str:
    """Get a screenshot from an MP4 file.
    try to get middle frame of the video
    """
    output_path = input_path.split('.')[0] + '.png'
    # Get the video capture object
    cap = cv2.VideoCapture(input_path)
    # Get the total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # Get the middle frame
    middle_frame = total_frames // 2
    # Set the frame number to the middle frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
    # Read the frame
    _, frame = cap.read()
    # Save the frame as an image
    cv2.imwrite(output_path, frame)
    # Release the video capture object
    cap.release()
    return output_path


def process_media(input_path: str) -> str:
    """Process a media file."""
    # Get the file extension
    file_extension = input_path.split('.')[-1]
    # Process the media file based on the file extension
    if file_extension == 'webp':
        new_path = convert_webp_to_gif(input_path)
    elif file_extension == 'mp4':
        new_path = get_screenshot_from_mp4(input_path)
    elif file_extension not in SUPPORTED_FILE_EXTENSIONS:
        new_path = None
    else:
        new_path = input_path
    return new_path
