
import numpy as np
import cv2


class ImagePreprocess:

    def __init__(self, image) -> None:
        self.image = image


    # apply all preprocessing methods

    # def preprocess(self):
    #     self.image = self._get_grayscale(self.image)
    #     self.image = self._remove_noise(self.image)
    #     self.image = self._thresholding(self.image)
    #     self.image = self._dilate(self.image)
    #     self.image = self._erode(self.image)
    #     self.image = self._opening(self.image)
    #     self.image = self._canny(self.image)
    #     self.image = self._deskew(self.image)
    #     # self.image = self._match_template(self.image)

        # return self.image

    # get grayscale image
    def _get_grayscale(self):
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    # noise removal
    def _remove_noise(self):
        return cv2.medianBlur(self.image,5)
    
    #thresholding
    def _thresholding(self):
        return cv2.threshold(self.image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #dilation
    def _dilate(self):
        kernel = np.ones((5,5),np.uint8)
        return cv2.dilate(self.image, kernel, iterations = 1)
        
    #erosion
    def _erode(self):
        kernel = np.ones((5,5),np.uint8)
        return cv2.erode(self.image, kernel, iterations = 1)

    #opening - erosion followed by dilation
    def _opening(self):
        kernel = np.ones((5,5),np.uint8)
        return cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)

    #canny edge detection
    def _canny(self):
        return cv2.Canny(self.image, 100, 200)

    # #skew correction
    # def _deskew(self):
    #     coords = np.column_stack(np.where(self.image > 0))
    #     coords = coords.astype(np.int)
    #     angle = cv2.minAreaRect(coords)[-1]
    #     if angle < -45:
    #         angle = -(90 + angle)
    #     else:
    #         angle = -angle
            
    #     h, w = self.image.shape[:2]
    #     center = (w // 2, h // 2)
    #     M = cv2.getRotationMatrix2D(center, angle, 1.0)
    #     rotated = cv2.warpAffine(self.image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    #     return rotated

    # #template matching
    # def _match_template(self, template):
    #     return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)