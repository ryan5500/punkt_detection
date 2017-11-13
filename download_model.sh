id=$1

curl -c /tmp/cookie.txt -s -L "https://drive.google.com/uc?export=download&id=${id}" |grep confirm |  sed -e "s/^.*confirm=\(.*\)&amp;id=.*$/\1/" | xargs -I{} \
curl -b /tmp/cookie.txt  -L -o ./data/model.100K.klm "https://drive.google.com/uc?confirm={}&export=download&id=${id}"
