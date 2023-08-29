
from deepface import DeepFace

# import os
# os.environ["CUDA_VISIBLE_DEVICES"]=""

objs = DeepFace.analyze(img_path = "person1.jpg", 
        actions = ['age','gender','emotion']
)

print(objs)

print(objs[0]["age"])
print(objs[0]["region"]["x"])

genders = objs[0]["gender"]
gender = max(genders, key=genders.get).lower()
print(gender)

emotions = objs[0]["emotion"]
emotion = max(emotions, key=emotions.get)
print(emotion)

possible_emotions = list(emotions)
print(possible_emotions)