# ivc
Ipython function "version control"

## Motivation
Jupyter notebooks are great for exploring data but can leave a mess as the data scientist iteratively explores data and generates the output they want. Trying to be disciplined in how code is built in these notebooks can remove the advantages of quick iteration, and from what I see of myself and others using notebooks, discipline quickly gives way to sloppy copy pasting to track different things that have been tried.

This is the mvp of my simple solution, building a decorator that tracks functions being built in a notebook, and the output they display. At any time, the user can examine and compare past versions. The only overhead is that the code has to be wrapped in a function.

I see lots of directions this can be developed into something more full-featured. I'm still exploring how I use it myself most effectively and what additional features I would want. Please let me know if you have any feedback about if and how you would use it.

## Installation
This is a very simple module, so you may want to just copy `ivc/ivc.py` and include it in your project. Alternately, clone and install with `pip install -e ./`

Required dependencies: 

```python
pandas 
IPython
matplotlib
```

## Usage
For use in an IPython (Jupyter) Notebook only. Before any tracking, use

```python
from ivc import ivc
myvc = ivc.VC()
```

For any function you want to track, add the decorator as shown below 

```python
@myvc.add_vc(comment="Optional")
def myfunc(a):
    print (a)
    print(a*a)

myfunc(2)
``` 

Then, you can see a `dict` with all the versions of your code, and the last output, if any:

```python
[n]: myvc.versions

Out[n]: {'myfunc': {'d5a0371fd02092886e966374f8adab77': {'source': '@myvc.add_vc(comment="Optional")          \ndef myfunc(a):\n    print (a)\n    print(a*a)\n',
   'timestamp': '2020-07-26T15:06:20.205288',
   'comment': 'Optional',
   'count': 1,
   'last_output': ('2\n4\n', '', [])}}}
```

The output is stored as tuple of `(stdout,stderr,IPython.utils.capture.RichOutput)`, the third entry capturing output like `matplotlib` plots or dataframes. 

Functions are indexed by their name and the hash of their code. If you have more than one version of a function, you can compare two versions using the `myvc.diff(func,hash1,hash2)` function. E.g., if I edit `myfunc` above to:

```python
@myvc.add_vc(comment="Optional")          
def myfunc(a):
    print (a)
    print(2*a*a)

``` 

then inspecting `myvc.versions` gives:

```python
{'myfunc': {'d5a0371fd02092886e966374f8adab77': {'source': '@myvc.add_vc(comment="Optional")          \ndef myfunc(a):\n    print (a)\n    print(a*a)\n',
   'timestamp': '2020-07-26T15:06:20.205288',
   'comment': 'Optional',
   'count': 1,
   'last_output': ('2\n4\n', '', [])},
  'd66195e3b90bef1985348605ea40bb04': {'source': '@myvc.add_vc(comment="Optional")\ndef myfunc(a):\n    print (a)\n    print(2*a*a)\n',
   'timestamp': '2020-07-26T15:17:38.254748',
   'comment': 'Optional',
   'count': 0}}}
```

I can compare them with:

```python
In[n]: myvc.diff(myfunc,'d5a0371fd02092886e966374f8adab77','d66195e3b90bef1985348605ea40bb04')

Out[n]: 
['- @myvc.add_vc(comment="Optional")          ',
 '?                                 ----------\n',
 '+ @myvc.add_vc(comment="Optional")',
 '  def myfunc(a):',
 '      print (a)',
 '-     print(a*a)',
 '+     print(2*a*a)',
 '?           ++\n',
 '  ']
```

The output is produced by `difflib.Differ` and follows its conventions.

See `demo.ipynb` for a more detailed demo.
