<p align="center">
  <a href="https://api.loopy5418.dev/">
    <img width="200" src="https://i.postimg.cc/sXxL02Y1/android-chrome-512x512.png" alt="loopy-ts">
  </a>
</p>

<div align="center">
  <b>The official Python wrapper for api.loopy5418.dev.</b>
</div>

---

<br/>

<div align="center">

[![Discord Server][loopypy-server]][loopypy-server-url] &nbsp; &nbsp;
![Website](https://img.shields.io/website?url=https%3A%2F%2Fapi.loopy5418.dev%2F&label=api.loopy5418.dev) &nbsp; &nbsp;

[loopypy-server]: https://img.shields.io/discord/1365258638222164008?color=5865F2&logo=discord&logoColor=white

[loopypy-server-url]: https://api.loopy5418.dev/support

  </div>

<br />

<div align = "center">

**[ Documentation ](https://api.loopy5418.dev/)** | **[ Support Server ](https://api.loopy5418.dev/support)** | **[ PyPi ](https://pypi.org/project/loopypy/)** | **[ GitHub ](https://github.com/api-loopy5418-dev/loopypy)**

</div>

---

## About

loopypy is a wrapper for api.loopy5418.dev made in Python.

It's easy for people that don't know how to make HTTP requests.

## Setup

First install the package with 
```bash
pip install loopypy
```

Then paste this into you app.py (or whatever you call it!)
```python
import loopypy
# Or you can just do 
# from 'loopypy' import setApiKey, getApiKey, ai

loopypy.setApiKey("Secret!")
# You can get your api key at our server
# https://discord.gg/ZwK2W7GxhA


# Open AI
ask = loopy.ai("Hello, how are you! What's the weather in New York?")
print(ask.response)

# After running check your terminal!
# It should say something like:
# "Hello! I'm just a program, so I 
# don't have feelings, but I'm here to help you. 
# I don't have real-time data on the weather. 
# For the most accurate and current weather 
# information in New York, please check a 
# reliable weather website or app."
```


<details><summary><h3>Function List</h3></summary>
  
|Name|Description|API Key|
|----|-----------|-------|
|`setApiKey(key)`|Sets the API key for automated gathering later on.|x|
|`getApiKey()`|Returns the API key|Required|
|`ai(prompt, speed)`|Uses the /openai/text endpoint to generate text from ChatGPT.|Required|
|`owoify(text)`|Owoifies the text and returns it|Optional|
|`emojify(text)`|Turns the text into regional indicators in Discord format.|Optional|
|`qr(data)`|Turns the given data into a QR code and returns the image buffer.|Required|
|`currency(base, target, amount)`|Converts  one currency to another.|Required|
|`seconds_to_time(seconds)`|Converts given seconds into formatted time (HH\:MM:SS)|Optional|
|`pick(*args)`|Picks an option off of the given ones.|Optional|
|`ascii_art(text)`|Returns multiline ascii art off of the given text.|Optional|
|`Coming Soon`|More functions are coming soon.|
</summary></details>

<details><summary><h3>Function Usages</h3></summary>

```python
setApiKey(key)
```
Sets the API key for later use. Required for most endpoints.

**Syntax:**
- `key`: string, required

**Example Usage:**
```python
import loopypy
loopypy.setApiKey("xxxxx-xxxxxx-xxxxx-xxxxx")
print(loopypy.getApiKey()) # Prints the key you set
```
---
```python
getApiKey()
```
Retrieves and returns the current API key.

**Example Usage:**
```python
import loopypy
loopypy.setApiKey("xxxxx-xxxxxx-xxxxx-xxxxx")
print(loopypy.getApiKey()) # Prints the key you set
```
---
```python
ai(prompt, speed)
```
Uses the /openai/text endpoint to generate text from ChatGPT.

**Syntax:**
- `prompt`: String, required
- `speed`: Integer, optional, defaults to 1. (0: large, 1: balanced, 2: fast)

**Children:**
- `.response`
- `.model`
- `.prompt`
- `.success`

**Example Usage:**
```python
import loopypy
loopypy.setApiKey("xxxxx-xxxxxx-xxxxx-xxxxx")
ask = loopypy.ai("What's the capital of France?")
print(f"Response: {ask.response}")
print(f"Model: {ask.model}")
```
---
```python
owoify(text)
```
Owoifies the text and returns it.

**Syntax:**
- `text`: string, required

**Example Usage:**
```python
import loopypy
print(loopypy.owoify("Hello!"))
```
---
```python
emojify(text)
```
Turns the text into regional indicators in Discord format.

**Syntax:**
- `text` string, required

**Example Usage:**
```python
import loopypy
print(loopypy.emojify("Hello")) # Prints the key you set
```
---
```python
qr(data)
```
Turns the given data into a QR code and returns the image buffer.

**Syntax:**
- `data`: string, required

**Example Usage:**
```python
import loopypy
loopypy.setApiKey("xxxxx-xxxxxx-xxxxx-xxxxx")
buffer = loopypy.qr("Hello!") # get image buffer
with open("image.png", "wb") as f:
    f.write(buffer)
    print("QR Code image saved to file!")
```
---
```python
currency(base, target, amount)
```
Converts  one currency to another.

**Syntax:**
- `base`: string, required
- `target`: string, required
- `amount`: integer, required

**Children:**
- `.rate`
- `.converted`
- `.success`

**Example Usage:**
```python
import loopypy
loopypy.setApiKey("xxxxx-xxxxxx-xxxxx-xxxxx")
cur = loopypy.currency("USD", "EUR", 1)
print(f"Converted Money: {cur.converted}")
print(f"Rate: {cur.rate}")
```
---
```python
seconds_to_time(seconds)
```
-# This function will soon be changed to fit the children system. E.g. print(seconds_to_time.seconds)

Converts given seconds into formatted time (HH\:MM:SS)

**Syntax:**
- `seconds` integer, required

**Example Usage:**
```python
import loopypy
seconds = 260 # is 4 minutes and 20 seconds
print(loopypy.seconds_to_time(seconds)) # prints 00:04:20
```
---
```python
pick(*args)
```
Picks one of the given options.

**Syntax:**
- `args`: multiple objects, required

**Example Usage:**
```python
import loopypy
print(loopypy.pick("Hello", "Hi", 1, 5)) # Outputs one of the options.
```
---
```python
ascii_art(text)
```
Generates multiline ascii art.

**Syntax:**
- `text`: string, required

**Example Usage:**
```python
import loopypy
print(loopypy.ascii_art("Hello")) # Prints the multiline ascii text
```
</summary></details>
