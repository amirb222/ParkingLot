TIMESTART=$EPOCHSECONDS

mkdir templates
mv index.html templates/
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt install python3-pip -y
sudo pip3 install --upgrade pip
sudo pip3 install awscli
pip3 install flask boto3 pillow

echo "Setup took $((EPOCHSECONDS - TIMESTART)) seconds"

aws configure

echo "Now execute..."
echo "export FLASK_APP=lpr.py; python3 -m flask run --host=0.0.0.0"