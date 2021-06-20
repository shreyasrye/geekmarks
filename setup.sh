# This bash script will setup a virtual environment and install all the dependencies using the 
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

deactivate