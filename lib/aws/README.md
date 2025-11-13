# Aws

## Classes
- **`S3UrlCache`** (aws/s3/cachekeys.py) - Cache management object for url of object stored in Amazon S3
- **`S3Manager`** (aws/s3/utils.py) - S3Manager is an interface/wrapper for boto to Amazon S3

## Functions
- **`get_s3_key`** (aws/s3/models.py) - Computes the S3 Key for this object
- **`store_file`** (aws/s3/models.py) - Stores file `f`
- **`store_uploaded_file`** (aws/s3/models.py) - Store the uploaded file
- **`copy_stored_file_to`** (aws/s3/models.py) - Copies the stored file on S3 into the `dest_obj`'s bucket/key
- **`delete_thumbnail`** (aws/s3/models.py) - Convenience wrapper around `self.delete_stored_file()` to delete a thumbnail, if one exists
- **`clone`** (aws/s3/models.py) - Makes a clone of this S3MediaAsset with a copied file on S3
- **`put_file`** (aws/s3/utils.py) - Stores a file
- **`copy_file`** (aws/s3/utils.py) - Copies a file
- **`delete_file`** (aws/s3/utils.py) - Deletes a file
- **`get_url`** (aws/s3/utils.py) - Generates the URL for a file
