<!--TOC-->

# patlang

**Pattern language.**

A generic way of creating patterns or templates. 

A **pattern** can be devided into **2 parts**, a **static** part and a **dynamic** part, and can be **serialized** into a **string**. Each type has at least the following functions to set the static and or dynamic, but can also be accessed through `__getitem__` `__setitem__` this will call the functions below depending on the type of key (variable or not), except for the String based pattern. In this pattern static parts are converted to variables when accessed or set.

- `setItem(key, value)` 

- `getItem(key)`

- `setVariable(key, value)`

- `getVariable(key)`

-----

## Types

- String based pattern

*The String based pattern called*  `String` *is derived from* `str` *and uses tokens to set variables in a string*

- List based pattern

*The List based pattern called* `List` *is derived from* `list` *and uses variables to set variables in the list, Variables are defined within* `List` *and are derived from* `List`.

- Tree based pattern

*The List based pattern called* `Tree` *and acts as a node of a 2D linked list it also uses variables to set variables and can be serialized to a string*

---

## Example usage

### String

Create a new pattern

```python
groceries = patlang.String("get groceries")
```

Assign values

```python
groceries["groceries"] = "3 bananas"
groceries["groceries"] += ", 5 apples"
groceries["groceries"] += ", 2 pineapples"
```

Now this

```python
print(repr(groceries))
print(groceries)
```

Outputs

```
get 'groceries':'3 bananas, 5 apples, 2 pineapples'
get 3 bananas, 5 apples, 2 pineapples
```

Calling the string representation will replace the key with its corresponding value for each variable created.

Which can be usefull when creating code templates or templates of anykind, but can be prone to bugs, because there is no difference between text and a variable, for this the patlang.List is better.

#### Manipulation

```python
print("3 bananas" in groceries) # True
print("bananas" in groceries) # True
print("5 apples" in groceries) # True
print("groceries" in groceries) # True
print("get " in groceries) # True
print("get" in groceries) # True
```

And items can be changed using the variables

```python
print("6 apples" in groceries) # False
groceries["5"] = "6"
print("6 apples" in groceries) # True
```

But keep in mind that strings in python are officially immutable, and changing values will add variables, this means that `print(repr(groceries))` will now output

```
'get 'groceries':"3 bananas, ''5':'6'':'6' apples, 2 pineapples"'
```

And '5' is now changed into a variable. This can be frozen when copied to a new String.

```python
groceries = String(groceries)
print(repr(groceries))
```

Will now output

```
'get 3 bananas, 6 apples, 2 pineapples'
```

#### C++ class template

A basic c++ class template

```python
cpp_class = patlang.String("""class V_ClassName {
public:
    // Default constructor
    V_ClassName() {
        V_Constructor
    }

    V_PublicFunctions
};""")
```

Setting variables

```python
cpp_class["V_ClassName"] = "SomeNewClass"
cpp_class["V_Constructor"] = 'cout << "Default constructor called!" << endl;'
cpp_class["V_PublicFunctions"] = """// A simple member function
void greet() {
    cout << "Hello from V_ClassName!" << endl;
}"""
cpp_class["V_ClassName"] = cpp_class["V_ClassName"] # to update V_className
print(cpp_class)
```

will output

```cpp
class SomeNewClass {
public:
    // Default constructor
    SomeNewClass() {
        cout << "Default constructor called!" << endl;
    }

    // A simple member function
    void greet() {
        cout << "Hello from SomeNewClass!" << endl;
    }
};
```

#### Recursion

Because of the ability to replace values inside the value of the other variables, recursion can occur. For example:

```python
a = Pattern("hello")
a["hello"] = "hallo hello"
a["hallo"] = "hello hallo"

print(repr(a))
print(a)
```

Will return

```
''hello':''hallo':'hello hallo' hello''
hello hallo hello
```

These values can also be replace before outputting to `str` with the flush function.

```python
a.flush()

print(repr(a))
print(a)
```

Will return

```
''hello':'hello 'hallo':'hallo hello hallo' hello''
hello hallo hello hallo hello
```

### List

Create aliases

```python
Pattern = patlang.List
Variable = patlang.List.Variable # or patlang.VariableList
```

Create a new pattern

```python
groceries = Pattern("get ",Variable("groceries"))
```

Assign values

```python
groceries[Variable("groceries")] = "3 bananas"
groceries[Variable("groceries")] += ", 5 apples"
groceries[Variable("groceries")].append(", 2 pineapples")
```

Now this

```python
print(repr(groceries))
print(groceries)
```

Outputs

```
'get '('groceries':'3 bananas'', 5 apples'', 2 pineapples')
get 3 bananas, 5 apples, 2 pineapples
```

Calling the string representation will replace the variable with its corresponding value.

#### Manipulation

Checking on content can be done with the keyword `in`

```python
print("3 bananas" in groceries) # True
print("bananas" in groceries) # False
print("5 apples" in groceries) # False
print("groceries" in groceries) # False
print(Variable("groceries") in groceries) # True
print("get " in groceries) # True
print("get" in groceries) # False
```

Note that `5 apples` is not recognized because the pattern entered also includes a comma and a whitespace. This can be fixed with the following code

```python
groceries[Variable("groceries")] -= ", 5 apples"
groceries[Variable("groceries")] += Pattern(", ","5 apples")
```

Where the pattern output will look like:

```
'get '('groceries':'3 bananas'', 2 pineapples'', ''5 apples')
```

Or just

```python
groceries[", 5 apples"] = Pattern(", ","5 apples")
```

Where the pattern output will look like:

```
'get '('groceries':'3 bananas'', ''5 apples'', 2 pineapples')
```

Atleast now

```python
print("5 apples" in groceries) # True
```

#### C++ Class template

A basic class template

```python
cpp_class = Pattern("class ", Variable("ClassName"),""" {
public:
    // Default constructor
    """, Variable("ClassName"), """() {
        """, Variable("Constructor"), """
    }

    """, Variable("PublicFunctions"), """
};""")
```

Adding and setting values

```python
cpp_class[Variable("Constructor")] = 'cout << "Default constructor called!" << endl;'
cpp_class[Variable("PublicFunctions")] = Pattern("""// A simple member function
void greet() {
    cout << "Hello from """, Variable("ClassName"), """!" << endl;
}""")
cpp_class[Variable("ClassName")] = "SomeNewClass"

print(cpp_class)
```

Will output

```cpp
class SomeNewClass {
public:
    // Default constructor
    SomeNewClass() {
        cout << "Default constructor called!" << endl;
    }

    // A simple member function
    void greet() {
        cout << "Hello from SomeNewClass!" << endl;
    }
};
```

Note: that className is assigned after assigning PublicFunctions where the ClassName variable is used (If a variable is added later this value is replaced when the variable is assigned a new value.)

#### CSS template

Shorter aliases can be created to make it easier to create patterns

```python
P = Pattern
V = Variable
```

A basic CSS template (for QWidget)

```python
css = P("""
/* General App Style */
QWidget {
    font-family: "Segoe UI", sans-serif;
    font-size: """, V(P("QWidget", "font-size")),""";
    background-color: """, V(P("QWidget", "background-color")),""";
    color: """, V(P("QWidget", "color")),""";
}
""")
```

Values (defaults) can be set

```python
css[V(P("QWidget", "font-size"))] = "14px"
css[V(P("QWidget", "background-color"))] = "#000000"
css[V(P("QWidget", "color"))] = "#ffffff"
```

And changed

```python
css[V(P("QWidget", "color"))] = "#252525"
```

Where `print(css)` will now output

```css
/* General App Style */
QWidget {
    font-family: "Segoe UI", sans-serif;
    font-size: 14px;
    background-color: #000000;
    color: #252525;
}
```

#### Recursion

Recursion can only happen when values are assigned. Each time they are assigned all variables are assigned.

For example for

```python
a = P(V("hello"))
a[V("hello")] = P("hallo hello ") + V("hallo")
a[V("hallo")] = P("hello hallo ") + V("hello")

print(repr(a))
print(a)
```

Will return

```
('hello':'hallo hello '('hallo':'hello hallo '('hello':)))
hallo hello hello hallo 
```

But `a["hello"] = a["hello"]` will result in a recursion error. You can use `a["hello"] = str(a["hello"])`

To update variables they can also be added to

```python
a[V("hello")] += a[V("hallo")]

print(repr(a))
print(a)
```

Which will output

```
('hello':'hallo hello '('hallo':'hello hallo '('hello':))('hallo':'hello hallo '('hello':)))
hallo hello hello hallo hello hallo 
```

### Tree

Create aliases

```python
T = patlang.Tree
V = patlang.Tree.Variable # or patlang.VariableTree
P = T() # P for pattern
```

Create a new pattern

```python
P["groceries"]["get"][" "][V("groceries")][" "]["@"][" "]["the"][" "][V("market", "Market")]
```

Assign values (as Tree or as a 'normal' string value)

```python
P.setVariable("groceries", Tree("3 bananas"))
P.getVariable("groceries")[Tree(","," ","5 apples")]
P.setVariable("groceries", P.getVariable("groceries") + Tree(","," ","2 pineapples"))

P.setVariable("market", "fleemarket")
P.setVariable("market", P.getVariable("market") + " or " + "supermarket")
```

Now this

```python
print(repr(P["groceries"]))
print(P["groceries"])
```

Outputs

```
'get'' ''groceries':'3 bananas'','' ''5 apples'','' ''2 pineapples'' ''@'' ''the'' ''market':'fleemarket or supermarket'
get 3 bananas, 5 apples, 2 pineapples @ the fleemarket or supermarket
```

Calling the string representation will replace the variable with its corresponding value.

#### Manipulation

`setItem` can be used to change static items, for example, change space into a dash

```python
P.setItem(" ","-")
print(str(P["groceries"]))
```

Will output

```
get-3 bananas,-5 apples,-2 pineapples-@-the-fleemarket or supermarket
```

Note that only the spaces entered as seperate node to the patlang.Tree are replaced

Checking on content can be done with the keyword `in`

```python
print("3 bananas" in P["groceries"]) # True
print("bananas" in P["groceries"]) # False
print("5 apples" in P["groceries"]) # True
print("groceries" in P["groceries"]) # False
print(V("groceries") in P["groceries"]) # True
print("get " in P["groceries"]) # False
print("get" in P["groceries"]) # True
```

Remove from and 'freeze' variables

```python
P.setVariable("groceries", P.getVariable("groceries") - Tree(","," ","5 apples"))
P.setVariable("groceries", str(P.getVariable("groceries")))
P.setItem(" ","-")
```

Now `print(str(P["groceries"]))` will output

```
get-3 bananas, 2 pineapples-@-the-fleemarket or supermarket
```

This will ofcourse lose the ability to find the seperate nodes in the variable value which is of type Tree

```python
print("3 bananas" in P["groceries"]) # False
```

#### Recursion

```python
P.setVariable("groceries", P.getVariable("groceries") + V("groceries"))
print(str(P["groceries"]))
```

Will result in a recursion <mark>error</mark>.

## Build

To build as python package from the source, use

```
pip install build
python -m build
```

## Install from pip

Or just install from pip with

```
pip install patlang
```