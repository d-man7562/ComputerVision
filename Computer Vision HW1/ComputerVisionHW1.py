import numpy as np
import cv2 as cv
FRAME_RATE = 24
# Step 1: Read all frames and store them for reversed video 
# Change to your personal directory 
cap_rev = cv.VideoCapture("video.mp4")
# Asterisk * converts XVID into four separate objects
fourcc = cv.VideoWriter_fourcc(*'XVID')
# We will be saving the 2x2 video and the original video at three different speeds
out = cv.VideoWriter('outputfinal.avi', fourcc, FRAME_RATE, (1280,  720))
out4x = cv.VideoWriter('output4x.avi', fourcc, FRAME_RATE*4, (1280,  720))
out2x = cv.VideoWriter('output2x.avi', fourcc, FRAME_RATE*2, (1280,  720))
outhalfx = cv.VideoWriter('outputhalfx.avi', fourcc, FRAME_RATE/2, (1280,  720))


if not cap_rev.isOpened():
    print("Error: Could not open video file.")
    exit()

all_frames = []
while True:
    ret, frame = cap_rev.read()
    if not ret:
        break
    if frame is not None and frame.ndim == 3:
        # Save to array so we can put it in reverse
        all_frames.append(frame)
        # Save videos
        out4x.write(frame)
        out2x.write(frame)
        outhalfx.write(frame)

cap_rev.release()
if not all_frames:
    print("No frames were loaded. Check your video file.")
    exit()

all_frames.reverse()
frame_count = len(all_frames)
print(f"Loaded {frame_count} frames for reverse playback.")

# Step 2: Start the main video processing loop 
#change to your personal directory 
cap = cv.VideoCapture("video.mp4")
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

frame_index = 0
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Video stream has ended.")
        break

    if frame_index >= frame_count:
        frame_index = 0 
    
    backwrd_img = all_frames[frame_index]
    frame_index += 1

    # Get the video dimensions to resize
    h, w, chan = frame.shape
    new_w, new_h = w // 2, h // 2
    
    # Resize all videos 
    resized_forward = cv.resize(frame, (new_w, new_h))
    resized_backward = cv.resize(backwrd_img, (new_w, new_h))
    
    # 1 Top-Left: Grayscale
    gray = cv.cvtColor(resized_forward, cv.COLOR_BGR2GRAY)
    top_left = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

    # 2 Top-Right: Watermarked
    top_right = resized_forward.copy()
    cv.putText(top_right, "Sample Text", (50, new_h - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv.LINE_AA)

    # 3 Bottom-Left: Backward Video
    bottom_left = resized_backward

    # 4 Bottom-Right: Subtitled Video
    bottom_right = resized_forward.copy()
    if 2<= frame_index/FRAME_RATE <=7:
        cv.putText(bottom_right, "this is the first sentence!", (50, new_h - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv.LINE_AA)
    if 9<= frame_index/FRAME_RATE <=11:
         cv.putText(bottom_right, "this is the second!", (50, new_h - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv.LINE_AA)
    
    # Stack the images to create the 2x2 grid
    grid_top = np.hstack((top_left, top_right))
    grid_bottom = np.hstack((bottom_left, bottom_right))
    final = np.vstack((grid_top, grid_bottom))
    # Save as output.avi
    out.write(final)
    cv.imshow('2x2 Video Grid', final)
    
    if cv.waitKey(FRAME_RATE) & 0xFF == ord('q'):
        break
# Release videos
cap.release()
out.release()
out2x.release()
out4x.release()
outhalfx.release()

cv.destroyAllWindows()