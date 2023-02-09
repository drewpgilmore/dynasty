# Updates EC2 instance after app updates pushed
ssh -i ~/aws/fantasy-ubuntu-rsa.pem ubuntu@encinitasdynasty.com
cd dynasty
git pull
sudo systemctl stop fantasy.service # stops serving app -- url will return 502 bad gateway
sudo systemctl daemon-reload
sudo systemctl start fantasy.service
sudo systemctl enable fantasy.service
echo "App updated!"