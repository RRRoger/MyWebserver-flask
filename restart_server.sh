Port=5000  # Or 5000
PyPath="$PWD/miniconda3/envs/py36/bin"

pid=`ps ax | grep gunicorn | grep $Port | awk '{split($0,a," "); print a[1]}' | head -n 1`
if [ -z "$pid" ]; then
  echo "No gunicorn deamon on port $Port"
else
  kill $pid
  echo "Killed gunicorn deamon on port $Port"
fi

cd ~/sap_oa_broker
git pull

$PyPath/python $PyPath/gunicorn -c gunicorn.conf.py hello:app --preload -b 0.0.0.0:$Port --daemon

cd ~

pid=`ps ax | grep gunicorn | grep $Port | awk '{split($0,a," "); print a[1]}' | head -n 1`
if [ -z "$pid" ]; then
  echo "[!-_-!] ...Restart Fail..."
else
  ps -ef|grep gunicorn
  echo "......"
  echo "......"
  echo "[*^_^*] ...Restart Successfully..."
fi
