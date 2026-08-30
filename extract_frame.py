import cv2
import numpy as np

cap = cv2.VideoCapture(r'c:\Users\sanja\OneDrive\Desktop\codestorm\static\bg_video\animated_video.webm')
ret, frame = cap.read()
if ret:
    print("Frame shape:", frame.shape)
    
    # Let's save one frame with a white background
    # If it's 3 channels, the background is probably black.
    # We can replace near-black pixels with white.
    if frame.shape[2] == 3:
        # Luma key: if R<20 and G<20 and B<20, make it white
        mask = np.all(frame < 20, axis=2)
        frame[mask] = [255, 255, 255]
    
    cv2.imwrite(r'c:\Users\sanja\OneDrive\Desktop\codestorm\static\bg_video\animated_fallback.jpg', frame)
    print("Saved fallback image")
else:
    print("Failed to read video")
cap.release()
