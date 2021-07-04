#!/bin/bash
pip install virtualenv
virtualenv vpath

# Activate the virtual environment
case "$OSTYPE" in
  darwin*)  source vpath/bin/activate ;; 
  linux*)   source vpath/bin/activate ;;
  msys*)    vpath\Scripts\activate ;;
  *)        echo "unknown: $OSTYPE" ;;
esac

pip install -r requirements.txt
python url_extractor.py
python metadata.py

deactivate