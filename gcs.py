from google.cloud import storage

def mk_blob_to_GCS(target_name):
    gcs = storage.Client() # put credentials into GOOGLE_APPLICATION_CREDENTIALS

    bucket = gcs.get_bucket(gcs.project)

    return bucket.blob(target_name)

if __name__ == "__main__":
    mk_blob_to_GCS('test/filename').upload_from_filename('test.py')
    mk_blob_to_GCS('test/file').upload_from_file(open('test.py'))
    mk_blob_to_GCS('test/string').upload_from_string('hello world')
