source .virtualenvs/dhp/bin/activate
cd dhp
git pull

pip install -q -r requirements.txt

./manage.py migrate

npm update
compass clean
compass compile -e production
./manage.py collectstatic --noinput --ignore *.sass --ignore *.scss

touch configuration/wsgi.py

ENVIRONMENT=production
LOCAL_USERNAME=`whoami`
REVISION=`git log -n 1 --pretty=format:"%H"`

curl https://api.rollbar.com/api/1/deploy/ \
  -F access_token=$DHP_ROLLBAR_ACCESS_TOKEN \
  -F environment=$ENVIRONMENT \
  -F revision=$REVISION \
  -F local_username=$LOCAL_USERNAME

cd -
echo 'flush_all' | nc localhost 11211
