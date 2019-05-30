import cv2
import os
from glob import glob

dst_width = 224
dst_height = 224

def resizeWithRatio():
    for imgPath in images:
        origImg = cv2.imread(imgPath)
        height, width, channel = origImg.shape[:3]
        ratio = width / float(height)
        target_width = int(width / 4)
        target_height = int(target_width / ratio)
        resizedImg = cv2.resize(origImg, (target_width, target_height))
        image_base_name = os.path.basename(imgPath).split('.')[0]
        cv2.imwrite(image_dest_path+image_base_name+".jpg", resizedImg)

def resize():
    image_src_path = "raw_data/ocr_image"
    annot_src_path = "raw_data/ocr_annot"
    image_dest_path = "raw_data/ocr_image_"+str(dst_width) +"x" + str(dst_height)+"/"
    annots_dest_path = "raw_data/ocr_annot_"+str(dst_width) +"x" + str(dst_height)+"/"

    if not os.path.exists(image_dest_path):
        os.mkdir(image_dest_path)
    if not os.path.exists(annots_dest_path):
        os.mkdir(annots_dest_path)
    images = sorted(glob(os.path.join(image_src_path, '*.jpg')))
    for imgPath in images:
        origImg = cv2.imread(imgPath)
        resizedImg = cv2.resize(origImg, (dst_width, dst_height))
        image_base_name = os.path.basename(imgPath).split('.')[0]
        height, width, channel = origImg.shape[:3]
        ratio_x = dst_width / float(width)
        ratio_y = dst_height / float(height)
        pts = open(annot_src_path + "/" +image_base_name +
                   ".txt", 'r').readline().strip().split(',')
        pts = [int(pt) for pt in pts]
        resizedPts = [None] * 8
        resizedPts[0] = int(pts[0] * ratio_x)
        resizedPts[1] = int(pts[1] * ratio_y)
        resizedPts[2] = int(pts[2] * ratio_x)
        resizedPts[3] = int(pts[3] * ratio_y)
        resizedPts[4] = int(pts[4] * ratio_x)
        resizedPts[5] = int(pts[5] * ratio_y)
        resizedPts[6] = int(pts[6] * ratio_x)
        resizedPts[7] = int(pts[7] * ratio_y)
        cv2.line(resizedImg, (resizedPts[0], resizedPts[1]),
                 (resizedPts[2], resizedPts[3]), (255, 0, 0), 1)
        cv2.line(resizedImg, (resizedPts[0], resizedPts[1]),
                 (resizedPts[4], resizedPts[5]), 1)
        cv2.line(resizedImg, (resizedPts[4], resizedPts[5]),
                 (resizedPts[6], resizedPts[7]), (255, 0, 0), 1)
        cv2.line(resizedImg, (resizedPts[2], resizedPts[3]),
                 (resizedPts[6], resizedPts[7]), (255, 0, 0), 1)
        cv2.imwrite(image_dest_path+image_base_name+".jpg", resizedImg)
        with open(annots_dest_path+image_base_name+".txt", 'w') as filetowrite:
            length = len(resizedPts)
            for i in range(length):
                filetowrite.write(str(resizedPts[i]))
                if (i != (length - 1)):
                    filetowrite.write(',')

            filetowrite.close()

    # while(1):
    #     k = cv2.waitKey(33)
    #     if (k == 27):
    #         break


if __name__ == '__main__':
    # resizeWithRatio()
    resize()
