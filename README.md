## Setup
1. Create a `.env` file. 
2. Copy the contents of `.env.template` to `.env`. 
3. Fill in the necessary secrets.
4. Run ``pipenv sync``
5. Run ``pipenv shell``. This ensures the environmental variables are loaded.
6. Run ``flask --app app.py run --debug`` to start the server.

## Blob Storage
`blob_manager.py` handles setting up the blob storage connections and contains the functions for interacting with the blob storage.  

- We only have $100 of free credit for blob storage, so I'm using a local image for the feed page for testing during development.
- The functions `upload_files_example_get` and `upload_files_example_post` in `app.py` are examples for uploading files to blob storage using the blob_manager.