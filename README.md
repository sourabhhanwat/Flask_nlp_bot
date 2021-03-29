# Contextual Chatbot
## Simple chatbot implementation with PyTorch, NLP and Flask.
- The implementation is straightforward with a Feed Forward Neural net with 2 hidden layers.
- Customization for your own use case is super easy. Just modify intents.json with possible patterns and responses and re-run the training.
## Watch the Demo

![demo1](https://user-images.githubusercontent.com/28641642/112828503-68631d00-90ad-11eb-9361-da12835295dd.gif)
![demo2](https://user-images.githubusercontent.com/28641642/112828517-6b5e0d80-90ad-11eb-842a-c88ecf51d88e.gif)

## Installation

### Create an environment.

```sh
mkdir Flask_Bot
$ cd Flask_Bot
$ python3 -m venv venv
```
### Activate it
Mac / Linux:
```sh
. venv/bin/activate
```
Windows:
```sh
venv\Scripts\activate
```

### Install PyTorch and other dependencies

to know all about PyTorch see [official website][pyto].

install all required dependencies

```sh
pip3 install -r requirements.txt
```

### File Structure
- app.py - flask file used to run the project.
- train.py - used for train the model after some preprocessing of the sentence.
- model.py - file where the neural net class is written.
- cuisines.json - cuisines list used to match user cuisine input (or you can ignore this file using zomato API).
- intents.json - some predefine user and bot replied. will change this file according to our requirements.
- data.pth - after training, the model will save with this filename.
- list_of_cities_and_towns_in_india.csv - Indian cities name (or you can ignore this file using zomato API).

### Usage

Train the Model

```sh
python3 train.py
```
This will dump data.pth file. And then run

```sh
python3 app.py
```

### Customize

- Checkout intents.json file. You can customize it according to your own use case. Just define a new tag, possible patterns, and possible responses for the chatbot. You have to re-run the training whenever this file is modified
```sh
{
  "intents": [
    {
      "tag": "greeting",
      "patterns": [
        "Hi",
        "Hey",
        "How are you",
        "Is anyone there?",
        "Hello",
        "Good day"
      ],
      "responses": [
        "Hey :-)",
        "Hello, thanks for visiting",
        "Hi there, what can I do for you?",
        "Hi there, how can I help?"
      ]
    },
    ...
  ]
}
```
- app.py - Zomato search API is calling, based on the user input API will run and show you the top 3 results. you can see the API calling function in this file. in headers, you have to change the API key to run the system.API key is required for calling zomato APIs you can know more about API here [zomato-api][api]. city id is required in zomato search API. you can get city id from city_id function.
 

  [pyto]: <https://pytorch.org/>
  [api]: <https://app.swaggerhub.com/apis-docs/Vivek-Raj/zomato-api/1.0.0#/Restaurant%20Search/get_search/>
