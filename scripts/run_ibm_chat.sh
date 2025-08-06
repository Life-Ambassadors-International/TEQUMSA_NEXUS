#!/bin/bash
# Example request to IBM Cloud text/chat endpoint using TEQUMSA sample conversation.
# Usage: set YOUR_ACCESS_TOKEN environment variable before running.

if [ -z "$YOUR_ACCESS_TOKEN" ]; then
  echo "YOUR_ACCESS_TOKEN is not set" >&2
  exit 1
fi

curl "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -H "Authorization: Bearer ${YOUR_ACCESS_TOKEN}" \
  -d @"$(dirname "$0")/ibm_chat_request.json"

