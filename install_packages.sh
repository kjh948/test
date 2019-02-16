sudo apt-get update
sudo apt-get install -y build-essential cmake pkg-config
sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev
sudo apt-get install -y libgtk2.0-dev libgtk-3-dev
sudo apt-get install -y libcanberra-gtk*
sudo apt-get install -y libatlas-base-dev gfortran
sudo apt-get install -y python2.7-dev

sudo apt-get install -y python-pip
su
pip install -U pip
sudo pip install numpy
sudo pip install imutils

cd ~
unzip opencv.zip
unzip opencv_contrib.zip

cd ~/opencv-3.3.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF ..

make -j3
sudo make install
sudo ldconfig


#for pyaudio
sudo apt-get install portaudio19-dev
