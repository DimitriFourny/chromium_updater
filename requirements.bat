@echo off
echo Installing requirements in WSL
bash -c "sudo apt install python3 python3-pip"
bash -c "pip3 install -r requirements.txt"
pause