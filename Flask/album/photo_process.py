import cv2
import numpy as np

def video_photo(video_path,out_path):
	max_width=150

	cap = cv2.VideoCapture(video_path)
	video_width = int(cap.get(3))

	ratio = max_width * 1.0 / video_width

	ret, frame = cap.read()
	image=cv2.resize(frame, None, fx=ratio, fy=ratio)
	cap.release()

	cv2.imwrite(out_path, image)

def fill_photo(img,out_path):

	h,w=img.shape[0],img.shape[1]
	side=max(h,w)
	new = np.zeros((side,side,3), np.uint8)
	new.fill(255)
	if w>h:
		center=((side-h)/2.0)
		for i in range(img.shape[0]):
			for j in range(img.shape[1]):			
				new[int(i+center),j]=img[i,j]
	else:
		center=((side-w)/2.0)
		for i in range(img.shape[0]):
			for j in range(img.shape[1]):			
				new[i,int(j+center)]=img[i,j]

	print("save video")
	cv2.imwrite(out_path, new)
