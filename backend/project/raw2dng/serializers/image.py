from rest_framework import serializers
import  django.core.files.images
import raw2dng.models.image
import base64
from io import BytesIO
import os
from PIL import Image
import PIL


VALID_RAW = [
    "3FR", "ARI", "ARW", "BAY", "BRAW", "CRW", "CR2", 
    "CR3","CAP","DATA", "DCS", "DCR","DRF","EIP", 
    "ERF","FFF","GPR","IIQ","K25", "KDC","MDC", "MEF", 
    "MOS", "MRW","NEF", "NRW","OBM", "ORB","PEF", "PTX", 
    "PXN","R3D", "RAF", "RAW", "RWL", "RW2", "RWZ","SR2", 
    "SRF", "SRW","TIF","X3F"]
LIMIT_SIZE = 100000000 # 100MB

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = raw2dng.models.image.Image
        fields = ('id', 'user', 'date_created', 'source', 'converted', 'converted_source')
    
    def validate_source(self, value):
        # check if the image extension is a raw image
        if value.name.split(".")[-1].upper() not in VALID_RAW:
            raise serializers.ValidationError(f"File extension incorrect. It must be either {VALID_RAW}")

        # check if the image size does not execeed the limit of the user licence
        if value.size > LIMIT_SIZE:
            raise serializers.ValidationError(f"Max file size is {LIMIT_SIZE}MB")

        if hasattr(value, 'temporary_file_path'):
            file = value.temporary_file_path()
        else:
            if hasattr(value, 'read'):
                file = BytesIO(value.read())
            else:
                file = BytesIO(value['content'])

        # check that the file is not executable
        if os.access(file, os.X_OK):
            raise serializers.ValidationError("The file must not be executable")

        # check that the file is an image
        # TODO
        

        