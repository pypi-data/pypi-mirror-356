cleanlang let's you filter out profane and/or offensive language with customizable options! This includes things like threshold, a line between whether something is close to profane or not profane!
___

**DISCLAIMER**

Our module's results vary depending on your settings. This module is also in beta as of 6/10/25. We are also not responsible for any harm according to the MIT license.
___

profanityfilter: (Creates a profanity filter class)
```python
import cleanlang

profanebot = cleanlang.profanityfilter(['bad', 'word'], threshold=80) # (bad word list) (threshold at default set to 70)
```
Output:
```
No output
```
___

boolscan: (Determines whether or not a string contains profane language or not based on a boolean [True/False])
```python
import cleanlang

pb = cleanlang.profanityfilter(['bad', 'word'], threshold=70)

print(pb.scan('this Woard is b@d'))
```
Output:
```
True
```
___

percentscan: (Determines whether or not a string contains profane language or not based on an integer percentage from 0-100)
```python
import cleanlang

pb = cleanlang.profanityfilter(['word']) # (threshold won't do anything in this case)

print(pb.percentscan('werd'))
```
Output:
```
75
```
___

fillerscan: (Replaces any profane words with a filler of your choosing)
```python
import cleanlang

pb = cleanlang.profanityfilter(['word'])

print(pb.fillerscan("Hello! Isn't this a cool word?", '[_]')) # _ (Filler)
```
Output:
```
Hello! Isn't this a cool [_]
```
___

Extras:
If you would like a preset list of profanities, just do:
```python
from cleanlang.extras import profanitylist

print(profanitylist)
```
Output:
```
view output at your own discretion 
```
___

dependencies:
- fuzzywuzzy[speedup]
___

Thanks for reading, and enjoy cleanlang! :)
