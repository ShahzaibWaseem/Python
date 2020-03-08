import cv2
import matplotlib.pyplot as plt

def enhanceImage(imagePath):
	imName=imagePath.split('/')[-1].split('.')[0]
	image=cv2.imread(imagePath, 0)

	# Show Image
	cv2.imshow(imName, image)
	cv2.waitKey(0)

	# View and Save the Histogram
	plt.hist(image.ravel(), 256, [0, 256])
	plt.savefig("../Images/"+ imName +"_Histogram.png")
	plt.show()

	# Histogram Equalization and Save the Image
	equalizedImage = cv2.equalizeHist(image)
	cv2.imwrite("../Images/"+ imName +"_equalized.jpg", equalizedImage)

	# Show Equalized Image
	cv2.imshow("Equalized" + imName, equalizedImage)
	cv2.waitKey(0)

	# View and Save the Equalized Histogram
	plt.hist(equalizedImage.ravel(), 256, [0, 256])
	plt.savefig("../Images/"+ imName +"_equalized_Histogram.png")
	plt.show()

def main():
	footballImage="../Images/football.jpg"
	enhanceImage(footballImage)

	cameramanImage="../Images/cameraman.tif"
	enhanceImage(cameramanImage)

	gantrycrane="../Images/gantrycrane.png"
	enhanceImage(gantrycrane)


if __name__ == '__main__':
	main()