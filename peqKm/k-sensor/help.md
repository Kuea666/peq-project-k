To upgrade Python to version 3.8 on your Raspberry Pi, you can follow these steps:

1. First, update the package list:

```bash
sudo apt-get update
```

2. Then, install the prerequisites:

```bash
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev tar wget vim
```

3. Download Python 3.8:

```bash
wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tgz
```

4. Extract the files:

```bash
tar zxf Python-3.8.12.tgz
```

5. Navigate to the Python directory:

```bash
cd Python-3.8.12
```

6. Configure the build:

```bash
./configure --enable-optimizations
```

7. Build and install Python:

```bash
make
sudo make altinstall
```

8. Verify the installation:

```bash
python3.8 -V
```

This should output `Python 3.8.12`, confirming that Python 3.8 is installed.


pip install -r requirements.txt