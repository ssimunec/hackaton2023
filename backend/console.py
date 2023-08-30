
from faceanalytics import FaceAnalytics
from detector import PersonDetector

source_image_path = "./person1.jpg"

person_detector = PersonDetector()

inference_result = person_detector.run(source_image_path)

print(inference_result)

closest = person_detector.find_closest(inference_result)

print(closest)
result_image = person_detector.crop_image(closest, source_image_path)

# result_image.show()

fa = FaceAnalytics()

fa_result = fa.run(source_image_path)

print(fa_result)