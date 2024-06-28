# Bilbot README File

## Configure and Run Bot
sgamgee is the username used throughout the process.
Change this to whatever your actual username is.
### Setup Virtual Environment
```bash
cd /home/<user>/bots/
git https://github.com/Ka5pyr/Bilbot-Baggins.git
cd Bilbot-Baggins
python3 -m venv venv
python3 -m pip install -r requirements.txt
```

### Add DISCORD_TOKEN into .venv file
```bash
cd /home/sgamgee/bots/Bilgot-Baggins
touch .venv
```
Copy Key into the .venv with the following format
```DISCORD_TOKEN=<KEY>```

### Run the But
```python3 main.py```

## Setup Bot as a Process (Linux)
```bash
cd /home/sgamgee/bots/Bilgot-Baggins
sudo mkdir /run/bilbot
sudo chown sgamgee:sgamgee /run/bilbot
sudo cp bilbot.service /etc/systemd/system/bilbot.service
sudo systemctl daemon-reload
sudo systemctl enable --now bilbot.service
```