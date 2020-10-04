#/bin/bash


python3 -m venv pyenv
pyenv/bin/pip3 install -r requirements.txt


cat > RN2483-CLI <<TXT
#!/bin/bash

$PWD/pyenv/bin/python3 $PWD/RN2483-CLI.py "\$*"
TXT
chmod +x RN2483-CLI

echo Installing
sudo ln -sf $PWD/RN2483-CLI /usr/local/bin

echo Created symlink to RN2483-CLI in usr/local/bin, remember to run rehash
