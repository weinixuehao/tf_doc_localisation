import cv2
import os
from glob import glob

dst_width = 224
dst_height = 224

def resizeImg():
    image_src_path = "raw_data/rec_imgs"
    image_dest_path = "raw_data/rec_imgs_"+str(dst_width) +"x" + str(dst_height)+"/"
    if not os.path.exists(image_dest_path):
        os.mkdir(image_dest_path)
    images = sorted(glob(os.path.join(image_src_path, '*.jpg')))
    for imgPath in images:
        origImg = cv2.imread(imgPath)
        height, width, channel = origImg.shape[:3]
        ratio = width / float(height)
        target_width = int(width / 4)
        target_height = int(target_width / ratio)
        resizedImg = cv2.resize(origImg, (target_width, target_height))
        image_base_name = os.path.basename(imgPath).split('.')[0]
        cv2.imwrite(image_dest_path+image_base_name+".jpg", resizedImg)

def resizeBackgroundImg():
    # image_src_path = "raw_data/ocr_train_image_background"
    # image_dest_path = "raw_data/ocr_train_image_background_"+str(dst_width) +"x" + str(dst_height)+"/"
    image_src_path = "raw_data/other_bgs"
    image_dest_path = "raw_data/other_bgs"+str(dst_width) +"x" + str(dst_height)+"/"
    if not os.path.exists(image_dest_path):
        os.mkdir(image_dest_path)
    images = sorted(glob(os.path.join(image_src_path, '*.jpg')))
    for imgPath in images:
        origImg = cv2.imread(imgPath)
        resizedImg = cv2.resize(origImg, (dst_width, dst_height))
        image_base_name = os.path.basename(imgPath).split('.')[0]
        cv2.imwrite(image_dest_path+image_base_name+".jpg", resizedImg)
  

def resizeWithAnnot():
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
        # cv2.line(resizedImg, (resizedPts[0], resizedPts[1]),
        #          (resizedPts[2], resizedPts[3]), (255, 0, 0), 1)
        # cv2.line(resizedImg, (resizedPts[0], resizedPts[1]),
        #          (resizedPts[4], resizedPts[5]), 1)
        # cv2.line(resizedImg, (resizedPts[4], resizedPts[5]),
        #          (resizedPts[6], resizedPts[7]), (255, 0, 0), 1)
        # cv2.line(resizedImg, (resizedPts[2], resizedPts[3]),
        #          (resizedPts[6], resizedPts[7]), (255, 0, 0), 1)
        cv2.imwrite(image_dest_path+image_base_name+".jpg", resizedImg)
        with open(annots_dest_path+image_base_name+".txt", 'w') as filetowrite:
            length = len(resizedPts)
            for i in range(length):
                filetowrite.write(str(resizedPts[i]))
                if (i != (length - 1)):
                    filetowrite.write(',')

            filetowrite.close()

def resizeMidv_500():
    src_dir = "/Users/user/Downloads/midv_500"
    dst_dir = "/Users/user/Downloads/midv_500_"+str(dst_width) +"x" + str(dst_height)+"/"
    images = sorted(glob(os.path.join(src_dir, '*.jpg')))
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    for imgPath in images:
        origImg = cv2.imread(imgPath)
        resizedImg = cv2.resize(origImg, (dst_width, dst_height))
        image_base_name = os.path.basename(imgPath).split('.')[0]
        height, width, channel = origImg.shape[:3]
        ratio_x = dst_width / float(width)
        ratio_y = dst_height / float(height)
        pts = open(src_dir + "/" +image_base_name +
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
        # cv2.line(resizedImg, (resizedPts[0], resizedPts[1]),
        #          (resizedPts[2], resizedPts[3]), (255, 0, 0), 1)
        # cv2.line(resizedImg, (resizedPts[0], resizedPts[1]),
        #          (resizedPts[4], resizedPts[5]), 1)
        # cv2.line(resizedImg, (resizedPts[4], resizedPts[5]),
        #          (resizedPts[6], resizedPts[7]), (255, 0, 0), 1)
        # cv2.line(resizedImg, (resizedPts[2], resizedPts[3]),
        #          (resizedPts[6], resizedPts[7]), (255, 0, 0), 1)
        cv2.imwrite(dst_dir+image_base_name+".jpg", resizedImg)
        with open(dst_dir+image_base_name+".txt", 'w') as filetowrite:
            length = len(resizedPts)
            for i in range(length):
                filetowrite.write(str(resizedPts[i]))
                if (i != (length - 1)):
                    filetowrite.write(',')

            filetowrite.close()


if __name__ == '__main__':
    # resizeImg()
    # resizeWithAnnot()
    # resizeBackgroundImg()
    resizeMidv_500()
