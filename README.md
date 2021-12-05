# Preprocessor

## This is preprocessor server. 
See [Swagger API definition](https://app.swaggerhub.com/apis/ProValdi/preprocessor/1.0.0#/) for more details.




## Run (Linux)

Create virtual env in root directory:

```
python3 -m venv ./venv
```

and activate it:

```
source ./venv/bin/activate
```

now you are ready to install requirements.txt

```
cd server
pip3 install -r requirements.txt
python3 setup.py install
python3 -m swagger_server
```