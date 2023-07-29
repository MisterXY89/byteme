# ByteMe

Match researchers/participants with each other based on their research interests.

`app.py` is the main file. It contains the Flask app and the routes. 

See the `templates/` folder for the HTML templates.

## Getting Started

1. Create `.env` file in the root directory with the following content:

```bash
APP_NAME='byteme'
FLASK_SECRET='Your Secret' 
PORT='8080'                 # or any other port
DEBUG='True'                # or False
```

2. Run the following commands:
```bash
# install dependencies
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
# run the app
$ python3 app.py
```

Visit http://localhost:8080/ to view the app.


## For nerwork-based recommendations
https://zhoushengisnoob.github.io/papers/TOIS.pdf


## Agenda:
1. Decide whether App comes up with Recommendations or Group Decisions
2. Do we swipe...
    1. SICSS Participants (Persons)
        - Each participant needs individual card with academic & social preferences
        - Swipe based on similarities with person (yes/no) or (percentage of preferences)
        - Recommendations based on resulting preference graph
    2. Research Topics & Method Interests (Interests)
        - Topic Collection for Research & Method Interest 
        - Swipe interest for each topic
        - Recommendations based on topic overlap
3. What Topics should be included in the card?
4. How should the model recommend, and how many rounds do we need?



## LICENSE: MIT License

Copyright 2023 SICSS Munich, Tilman Kerl

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.