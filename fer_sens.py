import os

import cv2
from tensorflow.keras.models import model_from_json 
import numpy as np
from PIL import Image, ImageFont, ImageDraw


from sensor import SensorWithVisual


class FerSensor(SensorWithVisual):
    """
    В случае FerSensor visualization - это квадратик
    вокруг лица распознаваемого человека
    и прямоугольник с подписью наиболее вероятной эмоции над ним
    """
    def __init__(self, names, icon_locations,
                 resource, min_possible, max_possible,
                 dir_, model_name = 'fer.json', weights_name = 'fer.h5'):
        super().__init__(names, icon_locations,
                         resource, min_possible, max_possible)
        self._model = FerSensor._load_nn(dir_, model_name, weights_name)
        self._face_detector = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
        self._face_coords = None
        self.visualization = np.zeros(
            self.resource.visualization.shape, dtype=np.uint8)

    
        
    def _get_rect_area(rect):
        _,_,w,h = rect
        return w*h

    def get_dark_overlay(img_width_and_height):
        n_channels = 4
        transparent_img = np.zeros(
            (*img_width_and_height, n_channels), dtype=np.uint8)
        transparent_img[:,:,3] = np.ones(
            img_width_and_height, dtype=np.uint8) * 91
        transparent_img[:,:,0] = np.ones(
            img_width_and_height, dtype=np.uint8) * 19
        transparent_img[:,:,1] = np.ones(
            img_width_and_height, dtype=np.uint8) * 20
        transparent_img[:,:,2] = np.ones(
            img_width_and_height, dtype=np.uint8) * 22
        return transparent_img 

    def init_viz_with_detection(self, img_width_and_height, face_coords):
        # Затемняю фон. Также можно рассмотреть:
        #     * засветление квадрата с лицом
        #     * отсутствие затемнения или засветления
        transparent_img = FerSensor.get_dark_overlay(img_width_and_height) 
        
        (x,y,w,h) = face_coords
        
        face_frame_color = (23, 33, 43, 255)

        # Сделаем участок с лицом прозрачным
        transparent_img[y:y+h, x:x+w, 3] = np.zeros(
            (w, h), dtype=np.uint8)

        cv2.rectangle(
            transparent_img, (x,y), (x+w,y+h), face_frame_color, thickness=4)

        font_height = 20
        font_padding = 3

        # создадим контур и заливку рамки для текста
        cv2.rectangle(
            transparent_img, (x,y), (x + w, y - font_height - font_padding*2),
            face_frame_color, thickness=-1)
        
        cv2.rectangle(
            transparent_img, (x,y), (x + w, y - font_height - font_padding*2),
            face_frame_color, thickness=4)

        self.visualization = transparent_img


    def visualize_prediction(self, results):
        font_height = 20
        font_padding = 3

        (x,y,_,_) = self._face_coords

        max_index = np.argmax(results)  # номер наиболее вероятной эмоции
    
        predicted_emotion = self.names[max_index]  # наиболее вероятная эмоция        
        font = ImageFont.truetype("arial.ttf", font_height)
        img_pil = Image.fromarray(self.visualization)
        draw = ImageDraw.Draw(img_pil)
        draw.text(
            (int(x + font_padding), int(y - font_height - font_padding)),
            f"{predicted_emotion}  {results[max_index]*100:.0f}%",
            font = font, fill = (255, 255, 255, 255))
        self.visualization = np.array(img_pil)


    def get_results(self, input):
        results = self._model.predict(input)[0]
        self.visualize_prediction(results)
        return results

    def preprocess(self, cam_img):
        all_faces_rects = self._face_detector.detectMultiScale(cam_img, 1.32, 5)

        if len(all_faces_rects) == 0:
            # сбросим визуализацию. Иначе будет рендериться старая рамка
            # self.visualization = np.zeros(
            #     self.resource.visualization.shape, dtype=np.uint8)

            # решил, что лучше затемнять весь кадр
            self.visualization = FerSensor.get_dark_overlay(
                self.resource.visualization.shape[:2])
            return None
        
        # Для распознавания используется самое большое лицо:
        # предполагается, что польователь будет находиться ближе всех к камере
        largest_face_rect = max(all_faces_rects, key=FerSensor._get_rect_area)
        self._face_coords = largest_face_rect 
        (x,y,w,h) = largest_face_rect
        
        # cv2.imshow('f', face_img)
        face_img = cam_img[y:y+h, x:x+w]
        gray_face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        cut_gray_face =cv2.resize(gray_face_img,(48,48))

        cut_gray_face_normed = cut_gray_face / 255

        # добавляем размерность, отвечющую за число каналов. (48, 48, 1)
        nn_input = np.expand_dims(cut_gray_face_normed, axis = 2)

        # добавляем размерность, отвечющую за число элементов батча.
        # (1, 48, 48, 1) 
        nn_input = np.expand_dims(nn_input, axis = 0)


        self.init_viz_with_detection(cam_img.shape[:2], largest_face_rect)

        return nn_input
    
    def _load_nn(dir_, model_name = 'fer.json', weights_name = 'fer.h5'):
        # загрузим модель
        model = model_from_json(open(os.path.join(dir_, model_name), "r").read())
        # загрузим веса
        model.load_weights(os.path.join(dir_, weights_name))
        return model


icons_dir = 'icons/emojis/'
# emotions = ["happy", "sad", "angry", "neutral", "surprised"]
emotions = ["angry", "disgusted", "fearful", "happy", "sad", "surprised", "neutral"]
emotions_icons = [os.path.join(icons_dir, f"{emotion}.svg") for emotion in emotions]
KMU_dir = 'models/KMUnet/KmuNet_drop_0.5/'


def alpha_compose(background, foreground):
    alpha_background = background[:,:,3] / 255.0
    alpha_foreground = foreground[:,:,3] / 255.0

    # set adjusted colors
    for color in range(0, 3):
        background[:,:,color] = alpha_foreground * foreground[:,:,color] + \
            alpha_background * background[:,:,color] * (1 - alpha_foreground)

    # set adjusted alpha and denormalize back to 0-255
    background[:,:,3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255