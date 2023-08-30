from math import floor
from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image
import torch
import requests
import detector
import os
from fastai.vision.all import *
from PIL import Image
from deepface import DeepFace


import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

source_image_path = './person1.jpg'

# person_detector = detector.PersonDetector()

# inference_result = person_detector.run(source_image_path)

# print(inference_result)

# closest = person_detector.find_closest(inference_result)

# print(closest)
# result_image = person_detector.crop_image(closest, source_image_path)

# result_image.show()

# Emotion

learn_emotion = load_learner('./emotions_vgg19.pkl')
learn_emotion_labels = learn_emotion.dls.vocab

# Sentiment
learn_sentiment = load_learner('./sentiment_vgg19.pkl')
learn_sentiment_labels = learn_sentiment.dls.vocab

def predict(img):
    img = PILImage.create(img)
    
    pred_emotion, pred_emotion_idx, probs_emotion = learn_emotion.predict(img)
    
    pred_sentiment, pred_sentiment_idx, probs_sentiment = learn_sentiment.predict(img)
    
    #emotions = {f'emotion_{learn_emotion_labels[i]}': float(probs_emotion[i]) for i in range(len(learn_emotion_labels))}
    #sentiments = {f'sentiment_{learn_sentiment_labels[i]}': float(probs_sentiment[i]) for i in range(len(learn_sentiment_labels))}
    
    emotions = {learn_emotion_labels[i]: float(probs_emotion[i]) for i in range(len(learn_emotion_labels))}

    print(emotions)
    sentiments = {learn_sentiment_labels[i]: float(probs_sentiment[i]) for i in range(len(learn_sentiment_labels))}
        
    print(sentiments)
    return [emotions, sentiments] #{**emotions, **sentiments}

result = predict(source_image_path)