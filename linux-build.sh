#!/bin/bash
# this shell script may only work on Linux distributions.

# install packages and python libs.
sudo apt install gcc binutils clang-format python3 python3-pip make \
    pkg-config autoconf automake \
    python3-docutils \
    libseccomp-dev \
    libjansson-dev \
    libyaml-dev \
    libxml2-dev \
    valgrind

sudo pip3 install pandas altair streamlit flask

# install ctags
mkdir deps; cd deps
git clone https://github.com/universal-ctags/ctags
cd ctags
./autogen.sh
./configure
make
sudo make install

# install nodejs
curl -sL https://deb.nodesource.com/setup_15.x | sudo -E bash -
sudo apt-get install -y nodejs

# frontend nodejs and build
cd ../..
cd frontend/profiler
npm install

