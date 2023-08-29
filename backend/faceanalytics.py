
from deepface import DeepFace


class FaceAnalytics:
    def run_inference(self, image):
        inputs = self.image_processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)

        logits = outputs.logits
        bboxes = outputs.pred_boxes

        target_sizes = torch.tensor([image.size[::-1]])

        results = self.image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]

        data =  list(zip(results["scores"], results["labels"], results["boxes"]))

        return data 

    def map_inference_result(self, raw_result):
        print(raw_result)

        age = raw_result[0]["age"]

        genders = raw_result[0]["gender"]
        gender = max(genders, key=genders.get).lower()

        emotions = raw_result[0]["emotion"]
        emotion = max(emotions, key=emotions.get)

        possible_emotions =list(emotions)
        possible_genders =  list(map(lambda key: key.lower(), genders))

        return age, gender, emotion, possible_genders, possible_emotions
    
    def run(self, source_image_path):
        raw_result = DeepFace.analyze(img_path = source_image_path, 
            actions = ['age','gender','emotion']
        )

        result = self.map_inference_result(raw_result)

        return result





        
    


