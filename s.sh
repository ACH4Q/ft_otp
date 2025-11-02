cd /goinfre/machaq
wget https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tgz
tar -xzf Python-3.10.12.tgz
cd Python-3.10.12
./configure --prefix=$HOME/.local/python3.10 --enable-optimizations
make -j4
make install
