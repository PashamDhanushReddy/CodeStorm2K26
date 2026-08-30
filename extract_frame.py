import cv2
import numpy as np

cap = cv2.VideoCapture(r'c:\Users\sanja\OneDrive\Desktop\codestorm\static\bg_video\animated_video.webm')
ret, frame = cap.read()
if ret:
    # We want to convert black background to transparent
    # Add alpha channel
    b_channel, g_channel, r_channel = cv2.split(frame)
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255 # opaque
    
    # Luma key: if R<20 and G<20 and B<20, make alpha 0
    mask = (r_channel < 20) & (g_channel < 20) & (b_channel < 20)
    alpha_channel[mask] = 0
    
    # Optional: soften edges
    # blurred_mask = cv2.GaussianBlur((~mask * 255).astype(np.uint8), (3,3), 0)
    # alpha_channel = blurred_mask
    
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    
    cv2.imwrite(r'c:\Users\sanja\OneDrive\Desktop\codestorm\static\bg_video\animated_fallback.png', img_BGRA)
    print("Saved transparent PNG fallback")
else:
    print("Failed to read video")
cap.release()
