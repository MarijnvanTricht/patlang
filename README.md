# patlang

Pattern language.

Contains the class `Pattern` which is derived from the class `list` which can contain Variables which are derived from the class `Pattern` (also checkout toklang, the string based counterpart)

## example usage

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

### C++ Class template

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

Note: that className is assigned after assigning PublicFunctions where the ClassName variable is used (If a variable is added later this value is replaced when the variable is assigned a new value.) *May need to be updated to update variables when added to a pattern if of the same name*

### CSS template

Short aliases can be created to make it easier to create patterns

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

### Recursion

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

## Build

To build as python package from this source, use

```
pip install build
python -m build
```