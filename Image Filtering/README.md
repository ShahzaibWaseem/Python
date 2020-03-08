# Lab 01: Image Filtering
## Tasks
### Task 1

- Read and display an image into the workspace. [you may use MatplotLib for image display]

- To see the distribution of intensities in the image, create a histogram by calling the `imhist` function.

- Improve the contrast in an image, you may like to use histogram equalization. If you compare the two histograms (equalized and original), you can see that the histogram of `equalized image` is more spread out over the entire range of intensities.

### Task 2
Use functions available in various python packages for convolution, which includes:
 
1. scipy method scipy.signal.convolve2d(img, kernel, 'valid')
2. OpenCV method cv2.filter2D(... , .. , ...).

Steps:
- Apply box filter using convolution, and display the resultant image
- Apply Gaussian filter to the image, with varying sigma values.
- Add Gaussian Noise and Salt and Pepper Noise to them.
- Apply Gaussian Filter and Median Filters.
- Apply Sobel operator, computer gradient magnitude and display the results (original image, gradient images and gradient magnitude image)
- Apply Canny Edge Detection Operator and display the results.

### Task 3 [optional/extra credit]
- Read the video from webcam and apply any of the filtering operation (blurring, gradient magnitude, edge detection etc on the video stream in the real time and display the resultant video stream, showing the effect of image filtering operation in real time.
- Hint: You can use `ipywebrtc` library