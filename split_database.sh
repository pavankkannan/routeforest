#!/bin/bash

# Delete the existing database chunks folder, if it exists
rm -rf database_chunks
# Compress the database
tar cfz compressed.db.tgz nfl_data.db
# Create a new folder for the database chunks
mkdir database_chunks
# Split the compressed database into chunks of up to 10MiB each
split -b 50m compressed.db.tgz database_chunks/db-part-
# Delete the compressed file
rm compressed.db.tgz