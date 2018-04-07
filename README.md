# README

MorphoDiTa Flask app using [czech-morfflex-pdt-161115](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-1836)
language model.

## Usage / minimal example

1. build docker image
```
docker build -t mordor .
```

2. run docker
```
docker run -p 4000:80 mordor
```

3. tag text
```
curl localhost:4000/?text=Karel
```
