import os
import cv2
from PIL import Image
import numpy as np

import tensorflow as tf
from django.conf import settings
from django.template.response  import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError

from django.core.files.storage import FileSystemStorage

class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name

def index(request):
    message = ""
    prediction = ""
    fss = CustomFileSystemStorage()
    try:
        image = request.FILES["image"]
        print("Name", image.file)
        _image = fss.save(image.name, image)
        path = str(settings.MEDIA_ROOT) + "/" + image.name
        #image details
        image_url = fss.url(_image)
        #Read the image
        imag = cv2.imread(path)
        img_from_ar = Image.fromarray(imag, 'RGB')
        resized_image = img_from_ar.resize((150, 150))

        test_image = np.expand_dims(resized_image, axis=0)

        #load model
        model = tf.keras.models.load_model(os.getcwd() + '/model.h5')

        result = model.predict(test_image)
    
        print("Prediction: " + str(np.argmax(result)))

        if (np.argmax(result) == 0):
            prediction = "No"
        elif (np.argmax(result) == 1):
            prediction = "Yes"
        else:
            prediction = "Unknown"

        return TemplateResponse(
            request,
            "tumorApp/index.html",
            {
                "message": message,
                "image": image,
                "image_url": image_url,
                "prediction": prediction,
            },
        )
    except MultiValueDictKeyError:

        return TemplateResponse(
            request,
            "tumorApp/index.html",
            {"message": "No Image Selected"},
        )




