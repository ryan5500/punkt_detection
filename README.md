# punkt_detection

## Requirement
* docker
* model file(*.klm)
### Download model file
* copy the id of google drive(id=1bgUTnUp7BZd3Q_TW-soplmSMBvg512c6)
* run this:
``
./download_model.sh 1bgUTnUp7BZd3Q_TW-soplmSMBvg512c6
``
### Build docker image and launch from it
``
cd dockerfiles
sudo docker build ubuntu --tag ubuntu_kenlm
sudo docker build kenlm --tag kenlm
cd ..
sudo docker run -itd kenlm
``

### Launch Jupyter daemon through docker run
* assume that you execute this in the root of this repository
* `pwd`/data should contain *.klm which you use
* HTTP access is redirected to Jupyter port (8888)
``
sudo docker run -d -v `pwd`/data:/punkt_detection/data -p 8888:80 kenlm /punkt_detection/start.sh
``

### Kill Jupyter
``
docker exec kenlm pkill jupyter
``
