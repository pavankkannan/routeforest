#!/bin/bash

# Concatenate the compressed database chunks into a single file
cat database_chunks/db-part-* > compressed.db.tgz
# Uncompress the combined file, which will output nfl_data.db
tar -xf compressed.db.tgz
# Delete the compressed file
rm compressed.db.tgz