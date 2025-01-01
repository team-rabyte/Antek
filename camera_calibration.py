import cv2
import numpy as np
import os

# Step 1: Set up criteria for corner refinement (for sub-pixel accuracy)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Step 2: Prepare the 3D points of the calibration pattern (checkerboard pattern)
# Change (7, 6) according to the number of inner corners on the checkerboard
checkerboard_size = (8, 5)  # Change this to match your checkerboard
square_size = (
    20  # mm # Size of a square in your checkerboard (can be 1 if units aren't needed)
)

# Create a grid of points in the (x, y, 0) plane
objp = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0 : checkerboard_size[0], 0 : checkerboard_size[1]].T.reshape(
    -1, 2
)
objp *= square_size  # Scale the points according to the size of the squares

# Arrays to store object points and image points from all images
objpoints = []  # 3D points in the real world
imgpoints = []  # 2D points in the image plane

# Step 3: Load images for calibration
images_path = "./"  # Directory where images are stored
images = [f for f in os.listdir(images_path) if f.endswith((".png", ".jpg", ".jpeg"))]

for image_file in images:
    img_path = os.path.join(images_path, image_file)
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 4: Find the corners of the checkerboard
    ret, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)

    # print(f"ret: {ret}")
    # print(f"corners: {corners}")

    if ret:
        objpoints.append(objp)  # 3D points
        corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners_refined)  # 2D points

        # Draw and display the corners for visual confirmation
        cv2.drawChessboardCorners(img, checkerboard_size, corners_refined, ret)
        cv2.imshow("Checkerboard Corners", img)
        cv2.waitKey(500)  # Wait 500 ms to see the corners

cv2.destroyAllWindows()

# Step 5: Calibrate the camera
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)

# Save the calibration results to a file for future use

try:
    np.savez(
        "camera_calibration_data.npz",
        camera_matrix=camera_matrix,
        dist_coeffs=dist_coeffs,
        rvecs=rvecs,
        tvecs=tvecs,
    )
    print(f"Saving successful.")
except:
    print(f"Camera calibration data saving FAILED.")


# Print the camera calibration results
print("Error in projection : \n", ret)
print("Camera matrix:\n", camera_matrix)
print("Distortion coefficients:\n", dist_coeffs)
print("Rotation Vectors:\n", rvecs)
print("Translation Vectors:\n", tvecs)

# Undistort an example image to see the effect of the calibration
img = cv2.imread(
    os.path.join(images_path, images[0])
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


data = np.load("camera_calibration_data.npz")
camera_matrix = data["camera_matrix"]
dist_coeffs = data["dist_coeffs"]

cap = cv2.VideoCapture(0)  # Change 0 to the index of the IMX219 camera

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
    cv2.imshow("Original", frame)
    cv2.imshow("Undistorted", undistorted_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
