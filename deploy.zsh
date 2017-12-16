cd dhp
git pull

pipenv install

pipenv run python manage.py makemigrations thumbnail
pipenv run python manage.py migrate

npm update
compass clean
compass compile -e production
pipenv run python manage.py collectstatic --noinput --ignore *.sass --ignore *.scss

touch configuration/wsgi.py

ENVIRONMENT=production
LOCAL_USERNAME=`whoami`
REVISION=`git log -n 1 --pretty=format:"%H"`

pipenv run curl https://api.rollbar.com/api/1/deploy/ \
  -F access_token=$DHP_ROLLBAR_ACCESS_TOKEN \
  -F environment=$ENVIRONMENT \
  -F revision=$REVISION \
  -F local_username=$LOCAL_USERNAME

cd -
echo 'flush_all' | nc localhost 11211
