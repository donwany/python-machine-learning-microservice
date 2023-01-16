MODEL_NAME = "model.pkl"
BUCKET_NAME = "youtube-demo-bkt"
ACCESS_KEY = "AKIAZTROQ2V2G4NAW123"
SECRET_KEY = "BrE4wVCrqYxRRbBC3lNwkBRIc3+5haXRsms2e123"
S3_LOCATION = "http://{0}.s3.amazonaws.com/{1}".format(BUCKET_NAME, MODEL_NAME)
MODEL_LOCAL_STORAGE_PATH = "/tmp/model.pkl"