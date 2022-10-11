from ffpyplayer.player import MediaPlayer
import cv2

def PlayVideo(title: str, video_path: str):
    # Define the stuff that will happen.
    video=cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    # Loop the content while the video plays.
    while True:
        grabbed, frame=video.read()
        audio_frame, val = player.get_frame()
        if not grabbed:
            # Do something after the video ends.
            break
        if cv2.waitKey(28) & 0xFF == ord("q"):
            break
        cv2.namedWindow(title, flags=cv2.WND_PROP_FULLSCREEN) # Define the GUI mode.
        cv2.setWindowProperty(title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        # cv2.resizeWindow(title, 768, 432) # Define the Window Resolution.
        cv2.imshow(title, frame) # Show the frame.
        if val != 'eof' and audio_frame is not None: # Attempt to sync the movie with the audio.
            img, t = audio_frame
    # Finish the task if the video ends.
    video.release()
    cv2.destroyAllWindows()