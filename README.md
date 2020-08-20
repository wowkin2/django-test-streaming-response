# About repository:
This is a repository prepared for [answer on StackOverflow](https://stackoverflow.com/a/63452601/3722635) 
to have ability to download code and test it.

Question is about Django StreamingHttpResponse in async Django views. Look [here for more details](https://stackoverflow.com/a/63452601/3722635).

# How to use it:

### Run Django web-server using Daphne:
```bash
daphne -b 0.0.0.0 -p 8000 webapp.webapp.asgi:application
```
> NOTE: I have 2 levels folder, but this is just because copy-paste from my test project. 
> In yours it still can be `sse_demo.asgi:application`

### Run script to check view:
```bash
python test_stream.py
```
#### Sync:
Uncomment line in `test_stream.py`:
```python
r = requests.get('http://localhost:8000/sse', stream=True)
```
#### ASync:
Uncomment line in `test_stream.py`:
```python
r = requests.get('http://localhost:8000/sse_async', stream=True)
```
