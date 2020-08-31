# README #

### What is this repository for? ###

This is a POC demonstrating a small web service that checks whether URLs are
malicious or not, responding accordingly.

This is built in python using the Flask framework, and is therefore relatively
lightweight and straight forward.

### How do I get set up? ###

#### Run Docker Container ####

1) Make a ```.env``` file at the project root, and add your Virus Total API
key to the environment variable ```VT_API_KEY```.
2) ```docker build -t url-lookup-service .```
3) ```docker run -p5000:5000 url-lookup-service```
4) Server should be running on ```127.0.0.1```

#### Testing ####
```python -m pytest```

### Who do I talk to? ###

Lauren Williams [<laurenwilliamssoftwareengineer@gmail.com>](mailto:laurenwilliamssoftwareengineer@gmail.com)