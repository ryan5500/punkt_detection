# punkt_detection

## Requirement
* Docker
* model file(*.klm)
### Download model file to data dir
```
mkdir data
./download_model.sh 1bgUTnUp7BZd3Q_TW-soplmSMBvg512c6
```

## Installation
``
### Build docker image and launch from it
```
% cd dockerfiles
% sudo docker build ubuntu --tag ubuntu
% sudo docker build python --tag python
% sudo docker build kenlm --tag kenlm
% cd ..
```

```
% docker run -it --rm -p 8888:8888 kenlm /bin/bash
% source activate jupyterenv
% python -c 'from notebook.auth import passwd;print(passwd())'
Enter password: 
Verify password: 
sha1:hogehoge
```

## Usage
### Launch Jupyter daemon through docker run
* assume that you execute this in the root of this repository
* $(pwd)/data should contain *.klm which you use
```
% sudo docker run -d -v $(pwd)/data:/punkt_detection/data -p 8888:8888 kenlm /bin/bash /punkt_detection/start.sh --NotebookApp.password = 'sha1:hogehoge'
```

### Kill Jupyter
```
docker exec kenlm pkill jupyter
```
