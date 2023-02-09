# Updates EC2 instance after app updates pushed
ssh -i ~/aws/fantasy-ubuntu-rsa.pem ubuntu@encinitasdynasty.com "cd dynasty; 
git pull; 
sudo systemctl stop fantasy.service;
sudo systemctl daemon-reload;
sudo systemctl start fantasy.service;
sudo systemctl enable fantasy.service;
echo 'App updated!'"