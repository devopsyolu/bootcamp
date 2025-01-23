#!/bin/bash

ENV=$1
echo "Deploying to $ENV environment..."

if [ "$ENV" == "staging" ]; then
    echo "Deploy işlemi staging ortamında tamamlandı."
elif [ "$ENV" == "prod" ]; then
    echo "Deploy işlemi prod ortamında tamamlandı."
else
    echo "Bilinmeyen ortam: $ENV"
fi
