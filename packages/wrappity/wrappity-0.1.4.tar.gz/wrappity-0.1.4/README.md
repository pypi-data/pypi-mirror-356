# Wrappity

_Wrappity is a Python package for easier access to deeply nested dictionaries._  
_Pure Python, no dependencies, lightweight (200 LOC)._

## What does it do

Wrappity allows you to access deeply nested dictionaries and combinations of `dicts` and `lists` using simple attribute 'dot' notation.
It is especially useful when your input are volatile json structures that unexpectedly change case by case.

Instead of...
```python
value = my_dict['foo'][3]['bar'][5]['baz']['this_is_what_I_want']
```

...you can write
```python
import wrappity
wrapped_dict = wrappity.wrap(my_dict)
value = wrapped_dict.foo[3].bar[5].baz.this_is_what_I_want._
```

### Why bother?

Because if you want to properly account for errors, you might end up with something like:
```python
if 'foo' in my_dict \
	and len(my_dict['foo']) >= 3 \
	and 'bar' in my_dict['foo'][3] \
	and len(my_dict['foo'][3]['bar']) >= 5 \
	and 'baz' in my_dict['foo'][3]['bar'][5]:
	value = my_dict['foo'][3]['bar'][5]['baz'].get('this_is_what_I_want','my default value')
```

With Wrappity you don't need to explicitely care about all the elements in the path to be there or not (or have enough items), if anything is missing on the way, Wrappity just gives you `None` at the end.

This allows (more elegant) constructs like this:
```python
value = wrapped_dict.foo[3].bar[5].baz.this_is_what_I_want._ or "my default value"
print(value)
'my default value' # in case any of the foo, bar or baz are not there
```

### Example use case

Let's say you're processing employee data from your company's HR system and want to write a function that greets their kids.

You look at some sample data on your input:

```python
>>> person1 = {'name':'John','surname':'Doe','age':40,'personal_details': {'kids':['Minnie','Moe'], 'wife':'Jane'},'address':{'street':'Rosemary Road 5','city':'Flower City','state':'Kansas'}}
>>> person2 = {'name':'Jack','surname':'Doe','age':35,'personal_details': {'partner': 'Juan'},'address':{'street':'Dead end','city':'Forgotten City','state':'Oklahoma'}}
```

You notice that for people without kids, the `kids` list is missing in `personal_details` completely.  
That's ok, with Wrappity you can implement your function as follows:

```python
>>> def greet_kids(person):
...     for kid in wrap(person).personal_details.kids._ or []:
...         print(f'Hi {kid}!')
...
>>> greet_kids(person1)
Hi Minnie!
Hi Moe!
>>> greet_kids(person2)
>>>
```

Next you need a function that greets their significant other. Some people have wifes, some have partners (and some might have none).
With Wrappity that would be:

```python
>>> def greet_significant_other(person):
...     pd = wrap(person).personal_details
...     significant_other = (pd.wife or pd.partner)._
...     if significant_other:
...         print(f'Greetings dear {significant_other}!')
...
>>> greet_significant_other(person1)
Greetings dear Jane!
>>> greet_significant_other(person2)
Greetings dear Juan!
>>>
```

But what if there's a new joiner to your company and HR colleagues have not yet added their personal details?  
No worries, your functions will still work:

```python
>>> person3 = {'name':'Jill','surname':'Newjoiner'}
>>> greet_kids(person3)
>>> greet_significant_other(person3)
>>>
```

You can find this example in full [here](examples/example1.py).

To learn more about why Wrappity was created and what use cases it's good for see [here](docs/why.md).

## Installation

Install Wrappity with `pip` or `uv`:

```bash
pip install wrappity

uv pip install wrappity
```

## Basic usage

There are 3 key functions in Wrappity:
1. `wrap()` - takes an object and wraps it for easy access
2. `unwrap()` - reverse function - give it a wrapped object and it gives you the original back
2. `inspect()` - for introspection - gives you a list of all paths to all leaves in your object incl. their values

### Wrap, unwrap & the ._ notation

Wrap any object to receive a wrapped version of it. Unwrap it to receive back the original.  
With the wrapper, you can access members of the original object using the 'dot' notation:

```python
>>> from wrappity import wrap, unwrap
>>>
>>> obj = {'foo': {'bar': 'baz'}}
>>> wrapped_obj = wrap(obj)
>>>
>>> wrapped_obj
wrapped(<class 'dict'>): {'foo': wrapped(<class 'dict'>): {'bar': wrapped(<class 'str'>): baz}}
>>> unwrap(wrapped_obj)
{'foo': {'bar': 'baz'}}
>>> assert unwrap(wrapped_obj) == obj # same thing
>>>
>>> print(wrapped_obj.foo.bar._)
baz
```

Use the `_` attribute of the wrapped object to access the original element wrapped at that place:

```python
>>> wrapped_obj._
{'foo': wrapped(<class 'dict'>): {'bar': wrapped(<class 'str'>): baz}}
>>> wrapped_obj.foo._
{'bar': wrapped(<class 'str'>): baz}
>>> wrapped_obj.foo.bar._
'baz'
```

If you try to access an element that does not exist, you get a wrapped object wrapping `None`, even if you go deeper into the void:

```python
>>> wrapped_obj.foo.hip # Note: hip was not in the original object
wrapped(<class 'NoneType'>): None
>>> print(wrapped_obj.foo.hip._)
None
>>> wrapped_obj.foo.hip.hap
wrapped(<class 'NoneType'>): None
>>> wrapped_obj.foo.hip.hap.hop
wrapped(<class 'NoneType'>): None
```

### Inspect

The `inspect()` function gives you all paths that exist in a wrapped object, incl. the values of the final leaves. This is esp. useful when you want to interactively examine a complex structure:

```python
>>> from wrappity import inspect
>>>
>>> person = {'name':'John','surname':'Doe','age':40,'kids':['Minnie','Moe'],'address':{'street':'Rosemary Road 5','city':'Flower City','state':'Kansas'}}
>>> print('\n'.join(
...     inspect(wrap(person))
... ))
name=John
surname=Doe
age=40
kids[0]=Minnie
kids[1]=Moe
address.street=Rosemary Road 5
address.city=Flower City
address.state=Kansas
```

## Where can I learn more?

See [Wrappity Guide](docs/guide.md).

## Why is it called Wrappity?

Because you do _wrappity wrap_ and that's it! 😉

## License

Licensed under the
[MIT](https://github.com/tomasrollo/wrappity/blob/main/LICENSE) License.

