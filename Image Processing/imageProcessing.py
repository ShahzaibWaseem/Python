import cv2
import numpy as np
import matplotlib.pyplot as plt

gammaValues=[0.1, 0.5, 1.2, 2.2]
kernel1=np.array([1])
kernel2=(1.0 / 5.0) * np.array([[0, 1, 0],
								[1, 1, 1],
								[0, 1, 0]])
kernel3=(1.0 / 9.0) * np.array([[1, 1, 1],
								[1, 1, 1],
								[1, 1, 1]])

kernels=[kernel1, kernel2, kernel3]

def gammaCorrection(image, gamma):
	gamma_corrected = np.array(255 * (image / 255) ** gamma, dtype = 'uint8')
	return gamma_corrected

def HistogramEqualization(image):
	equalizedImage = cv2.equalizeHist(image)
	return equalizedImage

def unsharpEnhancement(image):
	unsharp_image = np.zeros(shape=image.shape)

	gaussian_3 = cv2.GaussianBlur(image, (9, 9), 10.0)
	unsharp_image = cv2.addWeighted(image, 1.5, gaussian_3, -0.5, 0, image)
	return unsharp_image

def main():
	imagePath="Images/"
	underExposedImage=cv2.imread(imagePath+"UnderExposed.jpg")
	overExposedImage=cv2.imread(imagePath+"OverExposed.jpg")

	underExposedImage = cv2.cvtColor(underExposedImage, cv2.COLOR_BGR2GRAY)
	overExposedImage = cv2.cvtColor(overExposedImage, cv2.COLOR_BGR2GRAY)

	stackedImages=np.hstack((underExposedImage, overExposedImage))
	cv2.imshow("Images", stackedImages)
	cv2.waitKey(0)
	cv2.imwrite(imagePath+"Image.jpg", stackedImages)

	corrected_underExposedImage = gammaCorrection(underExposedImage, 0.5)
	corrected_overExposedImage = gammaCorrection(overExposedImage, 4.5)

	stackedImages=np.hstack((corrected_underExposedImage, corrected_overExposedImage))
	cv2.imshow("Images", stackedImages)
	cv2.waitKey(0)
	cv2.imwrite(imagePath+"correctedImage.jpg", stackedImages)

	plt.hist([underExposedImage.ravel(), overExposedImage.ravel()], 256, [0, 256], stacked=True)
	plt.show()

	equalized_underExposedImage=HistogramEqualization(underExposedImage)
	equalized_overExposedImage=HistogramEqualization(overExposedImage)

	stackedImages=np.hstack((equalized_underExposedImage, equalized_overExposedImage))
	cv2.imshow("Images", stackedImages)
	cv2.waitKey(0)
	cv2.imwrite(imagePath+"equalizedImage.jpg", stackedImages)


	for i, kernel in enumerate(kernels):
		kernel_underExposedImage=cv2.filter2D(underExposedImage, -1, kernel)
		kernel_overExposedImage=cv2.filter2D(overExposedImage, -1, kernel)

		stackedImages=np.hstack((kernel_underExposedImage, kernel_overExposedImage))
		cv2.imshow("Kernel: " + str(i+1), stackedImages)
		cv2.imwrite(imagePath+"Kernel_"+str(i+1)+".jpg", stackedImages)
		cv2.waitKey(0)
		plt.hist([kernel_underExposedImage.ravel(), kernel_overExposedImage.ravel()], 256, [0, 256], stacked=True)
		plt.show()

	gaussian_underExposedImage= cv2.GaussianBlur(underExposedImage, (9, 9), 10.0)
	gaussian_overExposedImage = cv2.GaussianBlur(overExposedImage, (9, 9), 10.0)

	stackedImages=np.hstack((gaussian_underExposedImage, gaussian_overExposedImage))
	cv2.imshow("Gaussian Blur", stackedImages)
	cv2.waitKey(0)
	cv2.imwrite(imagePath+"gaussianImage.jpg", stackedImages)

	sobel_underExposedImage=cv2.Sobel(equalized_underExposedImage, -1,1,0,ksize=5) + cv2.Sobel(equalized_underExposedImage, -1,0,1,ksize=5)
	sobel_overExposedImage=cv2.Sobel(equalized_overExposedImage, -1,1,0,ksize=5) + cv2.Sobel(equalized_overExposedImage, -1,0,1,ksize=5)

	stackedImages=np.hstack((sobel_underExposedImage, sobel_overExposedImage))
	cv2.imshow("First Order Derivative (Sobel)", stackedImages)
	cv2.waitKey(0)
	cv2.imwrite(imagePath+"sobelImage.jpg", stackedImages)

	laplacian_underExposedImage = cv2.Laplacian(equalized_underExposedImage, -1)
	laplacian_overExposedImage = cv2.Laplacian(equalized_overExposedImage, -1)
	stackedImages=np.hstack((laplacian_underExposedImage, laplacian_overExposedImage))
	cv2.imshow("Second Order Derivative (Laplacian)", stackedImages)
	cv2.waitKey(0)
	cv2.imwrite(imagePath+"laplacianImage.jpg", stackedImages)

	unsharp_underExposedImage = unsharpEnhancement(equalized_underExposedImage)
	unsharp_overExposedImage = unsharpEnhancement(equalized_overExposedImage)

	stackedImages=np.hstack((unsharp_underExposedImage, unsharp_overExposedImage))
	cv2.imshow("Unsharp Image", stackedImages)
	cv2.waitKey(0)
	cv2.imwrite(imagePath+"unsharpImage.jpg", stackedImages)

if __name__ == '__main__':
	main()