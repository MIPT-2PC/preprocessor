# preprocessor

## Run (not a guide)

```
cd server
python3 setup.py install --user
pip3 install -r requirements.txt
python3 setup.py install --user
export BALANCER_PORT=8080 # port for server to run
python3 -m swagger_server
```