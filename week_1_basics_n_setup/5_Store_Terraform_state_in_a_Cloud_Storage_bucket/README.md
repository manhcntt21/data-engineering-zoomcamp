https://cloud.google.com/docs/terraform/resource-management/store-state
Store Terraform state in a Cloud Storage bucket

- Configure Terraform to store state in a Cloud Storage bucket

  - Create the bucket
  - Make the bucket name unique
  - Change the backend configuration

- Test Resource String, output: https://www.phillipsj.net/posts/random-things-with-terraform/

- backend in terraform setting: https://www.terraform.io/language/settings/backends/gcs

  - Stores the state as an object in a configurable prefix in a pre-existing bucket on Google Cloud Storage (GCS). The bucket must exist prior to configuring the backend.
  - Set Object Versioning on a bucket: https://cloud.google.com/storage/docs/using-object-versioning#set
