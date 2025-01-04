import cv2
import os
import yaml
import numpy as np

debug = True

images_path = "./"  # Directory where images are stored
images = [f for f in os.listdir(images_path) if f.endswith((".png", ".jpg", ".jpeg"))]

# read calibration data
data = np.load("camera_calibration_data.npz")
camera_matrix = data["camera_matrix"]
dist_coeffs = data["dist_coeffs"]

# Undistort an example image to see the effect of the calibration
img = cv2.imread(
    os.path.join(images_path, images[150])
)  # Load any image from the calibration set
h, w = img.shape[:2]
new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
    camera_matrix, dist_coeffs, (w, h), 1, (w, h)
)

# Undistort the image
undistorted_img = cv2.undistort(
    img, camera_matrix, dist_coeffs, None, new_camera_matrix
)

# Crop the image to the region of interest (ROI)
x, y, w, h = roi
undistorted_img = undistorted_img[y : y + h, x : x + w]

# Show the original and undistorted images
cv2.imshow("Original Image", img)
cv2.imshow("Undistorted Image", undistorted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# start visual data acquisition
cap = cv2.VideoCapture(0)  # Change 0 to the index of the IMX219 camera


print("Press 'q' to exit.")
# camera recording
while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
        camera_matrix, dist_coeffs, (w, h), 1, (w, h)
    )

    undistorted_frame = cv2.undistort(
        frame, camera_matrix, dist_coeffs, None, new_camera_matrix
    )
    if debug:
        cv2.imshow("Original", frame)
    cv2.imshow("Undistorted", undistorted_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
