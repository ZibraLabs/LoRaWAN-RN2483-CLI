#/bin/bash

echo Setting up python environment
python3 -m venv pyenv
pyenv/bin/pip3 install -r requirements.txt

echo Creating launcher script
cat > RN2483-CLI <<TXT
#!/bin/bash
$PWD/pyenv/bin/python3 $PWD/RN2483-CLI.py "\$*"
TXT
chmod +x RN2483-CLI

echo Making symlink in /usr/local/bin, might prompt for a password
sudo ln -sf $PWD/RN2483-CLI /usr/local/bin

echo All done. remember to run rebase and then try something like: RN2483-CLI /dev/tty.usbserial-144110
