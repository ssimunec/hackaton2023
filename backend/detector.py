import torch
from math import floor
from PIL import Image
from transformers import YolosImageProcessor, YolosForObjectDetection


class PersonDetector:
    def __init__(self):
        self.model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')   
        self.image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

    def run_inference(self, image):
        inputs = self.image_processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)

        logits = outputs.logits
        bboxes = outputs.pred_boxes

        target_sizes = torch.tensor([image.size[::-1]])

        results = self.image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]

        data =  list(zip(results["scores"], results["labels"], results["boxes"]))

        return data 

    def map_inference_result(self, item):
        score, label, box = item
        box = [round(i, 2) for i in box.tolist()]
        score = round(score.item(), 3)
        label = self.model.config.id2label[label.item()]
        size_p =  floor(abs(box[0] - box[2])  * abs(box[1] - box[3]))
        return label, box, score, size_p
    
    def take_size(self, element):
        return element[len(element)-1]

    def take_people(self, element):
        return element[0] == 'person'

    def run(self, source_image_path):
        source_image = Image.open(source_image_path)

        inference_result_raw = self.run_inference(source_image)

        inference_result = list(map(self.map_inference_result, inference_result_raw))

        inference_result = filter(self.take_people, inference_result)

        inference_result = sorted(inference_result, key=self.take_size, reverse=True)

        return inference_result
    
    def find_closest(self, inference_result):
        inference_result = sorted(inference_result, key=self.take_size, reverse=True)
        return next(iter(inference_result or []), None)


