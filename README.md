# README #

### What is this repository for? ###

This is a POC demonstrating a small web service that checks whether websites are
malicious or not, responding accordingly.

This is built in python using the Flask framework, and is therefore relatively
lightweight and straight forward.

### How do I get set up? ###

#### Run Docker Container ####

1) Make a ```.env``` file at the project root, and add the follow environment variables:
 ```VT_API_KEY```, ```MYSQL_ROOT_PASSWORD```, ```DB_USER```, ```DB_PASS```

2) ```docker-compose up --build```

3) Server should be running on ```127.0.0.1:5000```

#### Testing ####
```python -m pytest```

### Who do I talk to? ###

Lauren Williams [<laurenwilliamssoftwareengineer@gmail.com>](mailto:laurenwilliamssoftwareengineer@gmail.com)