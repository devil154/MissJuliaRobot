indent() {
  sed -u 's/^/       /'
}

echo "-----> Install ffmpeg"
BUILD_DIR=$1
VENDOR_DIR="vendor"
DOWNLOAD_URL="https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz"

echo "DOWNLOAD_URL = " $DOWNLOAD_URL | indent

cd $BUILD_DIR
mkdir -p $VENDOR_DIR
cd $VENDOR_DIR
mkdir -p ffmpeg
cd ffmpeg
curl -L --silent $DOWNLOAD_URL | tar xJ --strip-components=1

echo "exporting PATH" | indent
PROFILE_PATH="$BUILD_DIR/.profile.d/ffmpeg.sh"
mkdir -p $(dirname $PROFILE_PATH)
echo 'export PATH="$PATH:${HOME}/vendor/ffmpeg"' >> $PROFILE_PATH

rm -rf *
mkdir MissJuliaRobot 
cd MissJuliaRobot
git clone https://github.com/MissJuliaRobot/MissJuliaRobot.git
cd MissJuliaRobot 
python3 -m julia
