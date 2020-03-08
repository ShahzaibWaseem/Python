import cv2
import numpy as np
import matplotlib.pyplot as plt

def imageFiltering(imagePath):
	imName=imagePath.split('/')[-1].split('.')[0]
	image=cv2.imread(imagePath, 0)

	kernel=np.ones((5, 5), np.float32)/25
	filteredImage=cv2.filter2D(image, -1, kernel)

	cv2.imwrite("../Images/"+ imName +"_filter.jpg", filteredImage)

def gaussianBlurring(imagePath, kernel):
	imName=imagePath.split('/')[-1].split('.')[0]
	image=cv2.imread(imagePath, 0)

	blurredImage = cv2.GaussianBlur(image, kernel, 0)

	cv2.imwrite("../Images/"+ imName +"_gaussianBlur.jpg", blurredImage)

def medianSmoothing(image, windowSize):
	height, width = image.shape
	padSize = windowSize // 2		# Integer Division
	newImage = np.zeros(image.shape)
	image = np.pad(image, (padSize, padSize), 'constant', constant_values=(0) )

	for x in range(padSize, height - padSize):
		for y in range(padSize, width - padSize):
			pixels = image[x-padSize:x+padSize+1, y-padSize:y+padSize+1]
			pixels = np.sort(pixels, axis=None)
			newImage[x-padSize, y-padSize] = pixels[(windowSize**2) // 2]
	return newImage

def edgesDetection(image, filter):
	height, width = image.shape
	windowSize = filter.shape[1]
	padSize = windowSize // 2		# Integer Division
	newImage = np.zeros(image.shape)
	image = np.pad(image, (padSize, padSize), 'constant', constant_values=(0) )

	for x in range(padSize, height - padSize):
		for y in range(padSize, width - padSize):
			pixels = image[x-padSize:x+padSize+1, y-padSize:y+padSize+1]
			newImage[x-padSize, y-padSize] = (np.sum(np.multiply(pixels, filter)))/3
	return newImage

def addNoise(imagePath, noiseType):
	imName=imagePath.split('/')[-1].split('.')[0]
	image=cv2.imread(imagePath, 0)
	if noiseType=="Gaussian Noise":
		row, col=image.shape
		noise=np.random.normal(0, 0.1, (row, col))
		return noise+image
	elif noiseType=="Salt and Pepper Noise":
		s_vs_p = 0.5
		amount = 0.004
		out = np.copy(image)
		# Salt mode
		num_salt = np.ceil(amount * image.size * s_vs_p)
		coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
		out[coords] = 1

		# Pepper mode
		num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
		coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
		out[coords] = 0
		return out

def main():
	footballImage="../Images/football.jpg"
	image=cv2.imread(footballImage, 0)
	imName=footballImage.split('/')[-1].split('.')[0]

	# Task 1
	imageFiltering(footballImage)

	# Task 2
	gaussianBlurring(footballImage, (3, 3))
	gaussianBlurring(footballImage, (5, 5))

	# Task 3
	gaussianNoise=addNoise(footballImage, "Gaussian Noise")
	saltPepperNoise=addNoise(footballImage, "Salt and Pepper Noise")

	# Task 4
	blurredImage = cv2.GaussianBlur(image, (5, 5), 0)

	stackedImage=np.hstack((image, gaussianNoise))
	stackedImage=np.hstack((stackedImage, blurredImage))

	plt.imshow(stackedImage, cmap='gray')
	plt.title("Image vs blurredImage vs filteredImage")
	plt.savefig("../Images/Image vs blurredImage vs filteredImage.png")
	plt.show()

	cv2.imwrite("../Images/"+ imName +"_gaussianBlur.jpg", blurredImage)

	medianSmoothenedImage = medianSmoothing(image, 3)

	stackedImage=np.hstack((image, saltPepperNoise))
	stackedImage=np.hstack((stackedImage, medianSmoothenedImage))

	plt.imshow(stackedImage, cmap='gray')
	plt.title("Image vs blurredImage (S&P) vs medianFiltering")
	plt.savefig("../Images/Image vs blurredImage (S&P) vs medianFiltering.png")
	plt.show()

	cv2.imwrite("../Images/football_medianSmoothened.jpg", medianSmoothenedImage)

	# Task 5
	sobelx = cv2.Sobel(image,cv2.CV_64F, 1, 0, ksize=5)
	sobely = cv2.Sobel(image,cv2.CV_64F, 0, 1, ksize=5)

	edges = sobely + sobelx

	cv2.imwrite("../Images/sobelx " + imName + ".png", sobelx)
	cv2.imwrite("../Images/sobely " + imName + ".png", sobely)
	cv2.imwrite("../Images/edges " + imName + ".png", edges)

	# Task 6
	canny = cv2.Canny(image, 100, 200)
	cv2.imshow("Canny", canny)
	cv2.imwrite("../Images/Canny.png", canny)
	cv2.waitKey(0)

if __name__ == '__main__':
	main()