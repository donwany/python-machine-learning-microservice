### How to RUN
```shell
docker build -t grammar-checker .
docker run -p 5000:5000 grammar-checker
```

### Visit
```shell
http://0.0.0.0:5000

# Test with:
A sentence with a error in the Hitchhiker’s Guide tot he Galaxy
Me and friend is going to the store
I done my homework
```