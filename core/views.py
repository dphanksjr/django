import numpy as np
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render
from keras.applications import vgg16
from keras.applications.imagenet_utils import decode_predictions
from tensorflow.keras.utils import img_to_array, load_img
from tensorflow.python.keras.backend import set_session


def index(request):
    return render(request, "index.html")