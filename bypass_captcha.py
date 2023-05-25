import time
import requests as rq
import cv2

print(cv2.__version__)

import numpy as np
import threading
import multiprocessing

# Cái này để tính toán song song -> tăng speed -> từ 1.1s -> 0.45s (4 core)
NUM_PROCESS = multiprocessing.cpu_count()
# Cái này để chuyển đổi từ độ -> pixel
TI_LE = 1.5262201462308829


def download_img(url, path):
    with open(path, 'wb') as f:
        f.write(rq.get(url).content)


def link_to_img(link: str):
    return cv2.imdecode(np.frombuffer(rq.get(link).content, np.uint8), -1)[:, :, :3]


class Bypass_captcha():
    def slice(self, image):
        print('Performed')

    def object(self, image):
        img = image.copy()

        def delete_background(img):
            img_new = cv2.inRange(img, (180, 180, 180), (250, 250, 250)) * 1
            return img_new

        def detect_yelow(img):
            img_new = cv2.inRange(img, (200, 200, 100), (255, 230, 150)) & (img[:, :, 1] - img[:, :, 2] > 50) & (
                    img[:, :, 0] - img[:, :, 2] > 75)
            return cv2.medianBlur(img_new * 1, 5)

        def detect_red(img):
            img_new = cv2.inRange(img, (220, 150, 130), (255, 200, 160)) & (img[:, :, 0] - img[:, :, 1] > 30) & (
                    img[:, :, 1] > img[:, :, 2])
            return cv2.medianBlur(img_new * 1, 5)

        def detect_gray(img):
            img_new = cv2.inRange(img, (170, 150, 140), (201, 181, 180)) & (
                    (img[:, :, 0] - (img[:, :, 0] * 0.5 + img[:, :, 2] * 0.5)) < 30)
            return cv2.medianBlur(img_new * 1, 5)

        def detect_violet(img):
            img_new = cv2.inRange(img, (160, 90, 170), (220, 160, 225)) & (img[:, :, 0] - img[:, :, 1] > 30) & (
                    img[:, :, 2] - img[:, :, 1] > 30)
            return cv2.medianBlur(img_new * 1, 5)

        def detect_green(img):
            img_new = cv2.inRange(img, (140, 160, 120), (180, 230, 180)) & (img[:, :, 1] - img[:, :, 0] > 30) & (
                    img[:, :, 1] - img[:, :, 2] > 30)
            return cv2.medianBlur(img_new * 1, 5)

        def detect_blue(img):
            img_new = cv2.inRange(img, (120, 180, 220), (160, 210, 255)) & (img[:, :, 1] > img[:, :, 0]) & (
                    img[:, :, 2] > img[:, :, 1])
            return cv2.medianBlur(img_new * 1, 5)

        def contour_box(contour):
            con = contour[:, 0]
            x1, x2, y1, y2 = con[:, 0].min(), con[:, 0].max(), con[:, 1].min(), con[:, 1].max()
            return x1, y1, x2, y2

        yelow = detect_yelow(img)
        red = detect_red(img)
        gray = detect_gray(img)
        violet = detect_violet(img)
        green = detect_green(img)
        blue = detect_blue(img)
        z = np.zeros(img.shape[:2])
        list_image_mini = []
        list_rectangle = []
        for img_threshold in [yelow, red, gray, violet, green, blue]:
            # for con in cv2.findContours(img_threshold,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]:
            for con in cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
                if cv2.contourArea(con) > 300:
                    x1, y1, x2, y2 = contour_box(con)
                    cv2.rectangle(z, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    list_image_mini.append(np.uint8(
                        cv2.threshold(cv2.cvtColor(img[y1 - 5:y2 + 5, x1 - 5:x2 + 5], cv2.COLOR_BGR2GRAY), 0, 255,
                                      cv2.THRESH_OTSU)[1] == 0))
                    list_rectangle.append([x1, y1, x2, y2])
        p_min = {'%': 0, 'box1': '', 'box2': ''}
        # plt.imshow(list_image_mini[1])
        for i in range(len(list_image_mini)):
            h, w = list_image_mini[i].shape[:2]
            im1 = cv2.resize(list_image_mini[i], (w, h))
            x1, y1, x2, y2 = list_rectangle[i]
            cv2.putText(img, str(i), (x1, y1), 1, 2, (255, 0, 255), 2)
            cv2.rectangle(img, (x1, y1), (x2, y2), (128, 128, 128))
            for j in range(i + 1, len(list_image_mini)):
                im2 = cv2.resize(list_image_mini[j], (w, h))
                x1, y1, x2, y2 = list_rectangle[i]
                v1 = (x2 - x1) / (y2 - y1)
                x1, y1, x2, y2 = list_rectangle[j]
                v2 = (x2 - x1) / (y2 - y1)
                pre2 = v1 / v2 if v1 < v2 else v2 / v1
                pse_sub = (im1 == im2).sum() / (im1.shape[0] * im1.shape[1])
                pse = np.max(cv2.matchTemplate(im1, im2, cv2.TM_CCOEFF_NORMED))
                pre_result = (pse ** 2) * (pre2 ** 2) * (pse_sub ** 2)
                # print([i,j],np.round(pse,3),'%', np.round(pre2,3),'%', np.round(pse_sub,3), '%')
                if pre_result > p_min['%']:
                    p_min['%'] = pre_result
                    x1, y1, x2, y2 = list_rectangle[i]
                    p_min['box1'] = (x1, y1, x2, y2)
                    x1, y1, x2, y2 = list_rectangle[j]
                    p_min['box2'] = (x1, y1, x2, y2)
        # <<< Trả về img
        # color = (255,0,0)
        # x1,y1,x2,y2 = p_min['box1']
        # cv2.rectangle(img,(x1-3,y1-3),(x2+3,y2+3),color,3) 
        # x1,y1,x2,y2 = p_min['box2']
        # cv2.rectangle(img,(x1-3,y1-3),(x2+3,y2+3),color,3)
        # cv2.putText(img,str(np.round(p_min['%']*100,2))+'%',(30,50),1,2,(255,0,0),2)
        # return img
        # >>>
        # Chạy 5 dòng ở dưới thì ẩn 7 dòng trên, chạy trên thì ẩn 5 dòng dưới
        # <<< Trả về 2 điểm
        x1, y1, x2, y2 = p_min['box1']
        point_1 = (x1 + x2) // 2, (y1 + y2) // 2
        x1, y1, x2, y2 = p_min['box2']
        point_2 = (x1 + x2) // 2, (y1 + y2) // 2
        return point_1, point_2
        # >>>

    def rotate(self, img_boder, img_in, min_angle: int = 20, max_angle: int = 180, range_angle: int = 1):
        global NUM_PROCESS, TI_LE
        mask = np.zeros([347, 347])
        cv2.circle(mask, (173, 173), 105, 1, 2)

        def rotate_img(img, angle):
            height, width = img.shape[:2]
            center = (width // 2, height // 2)
            rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=1)
            rotated_image = cv2.warpAffine(src=img, M=rotate_matrix, dsize=(width, height))
            return rotated_image

        def group_img(img_boder, img_in, angle: int = 0):
            img_boder_new = img_boder.copy()
            img_in_new = img_in.copy()
            if angle != 0:
                img_boder_new = rotate_img(img_boder_new, angle)
                img_in_new = rotate_img(img_in_new, -angle)
            img_boder_new[68:279, 68:279][img_in_new[:, :] != [0, 0, 0]] = img_in_new[img_in_new[:, :] != [0, 0, 0]]
            return img_boder_new

        # <<< Đã update speed
        list_angle = list(range(min_angle, max_angle + 1))
        len_angle = len(list_angle)
        score_success = [None for i in range(NUM_PROCESS)]

        def map_temp(do: int):
            img_temp = group_img(img_boder, img_in, do)
            img_temp = cv2.medianBlur(img_temp, 5)
            cany = cv2.Canny(img_temp, 128, 128, L2gradient=True)
            score = cany[mask != 0].sum()
            return score

        def start_map(angles: list, index_thread: int):
            # print(angles[0],'->',angles[-1])
            score_success[index_thread] = list(map(map_temp, angles))

        list_thread = [threading.Thread(target=start_map, args=(
            list_angle[int((i / NUM_PROCESS) * len_angle):int(((i + 1) / NUM_PROCESS) * len_angle)], i)) for i in
                       range(NUM_PROCESS)]
        # start thread
        for th in list_thread:
            th.start()
        while not np.all([not th.is_alive() for th in list_thread]):
            time.sleep(0.001)
        # kill thread
        del list_thread
        do = np.argmin([i for item in score_success for i in item]) + min_angle
        return do * TI_LE
        # >>>
        # ===== Ẩn trên thì hiện dưới và ngược lại =====
        # << Chưa update speed
        # info = {'min':999999999999, 'do':0}
        # for i in range(min_angle,max_angle+1,range_angle):
        #     img_temp = group_img(img_boder, img_in, i)
        #     img_temp = cv2.medianBlur(img_temp, 5)
        #     cany = cv2.Canny(img_temp, 128, 128, L2gradient=True)
        #     score = cany[mask!=0].sum()
        #     if(score<info['min']):
        #         info['min'] = score
        #         info['do'] = i
        # return info['do'] * TI_LE
        # return group_img(img_boder, img_in), cv2.medianBlur(group_img(img_boder, img_in, info['do']), 5), info['do']
        # >>>

    # def hide():
    #     pass
