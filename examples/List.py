from patlang import *

print("==== LIST ====")

groceries = List("get ",List.Variable("groceries"))

print(repr(groceries))

"""
'get '('groceries':)
"""

groceries[List.Variable("groceries")] = "3 bananas"
groceries[List.Variable("groceries")] += ", 5 apples"
groceries[List.Variable("groceries")].append(", 2 pineapples")

print(groceries)

"""
get 3 bananas, 5 apples, 2 pineapples
"""

print(repr(groceries))

"""
'get '('groceries':'3 bananas'', 5 apples'', 2 pineapples')
"""

print("3 bananas" in groceries) # True
print("bananas" in groceries) # False
print("5 apples" in groceries) # False
print("groceries" in groceries) # False
print(List.Variable("groceries") in groceries) # True
print("get " in groceries) # True
print("get" in groceries) # False

#groceries["groceries"] -= ", 5 apples"
#groceries["groceries"] += List(", ","5 apples")
groceries[", 5 apples"] = List(", ","5 apples")

print(repr(groceries))
print("5 apples" in groceries) # True

cpp_class = List("class ", List.Variable("ClassName"),""" {
public:
// Default constructor
""", List.Variable("ClassName"), """() {
    """, List.Variable("Constructor"), """
}

""", List.Variable("PublicFunctions"), """
};""")

cpp_class[List.Variable("ClassName")] = "SomeNewClass"
cpp_class[List.Variable("Constructor")] = 'cout << "Default constructor called!" << endl;'
cpp_class[List.Variable("PublicFunctions")] = List("""// A simple member function
void greet() {
    cout << "Hello from """, List.Variable("ClassName", str(cpp_class[List.Variable("ClassName")])), """!" << endl;
}""")

#cpp_class[List.Variable("ClassName")] = "SomeNewClass"

print(cpp_class)

"""
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
"""

print(repr(cpp_class))

"""
'class '('ClassName':'SomeNewClass')' {\npublic:\n    // Default constructor
\n    '('ClassName':'SomeNewClass')'() {\n        '('Constructor':'cout << "
Default constructor called!" << endl;')'\n    }\n    \n    '('PublicFunction
s':'// A simple member function\n    void greet() {\n        cout << "Hello
from '('ClassName':'SomeNewClass')'!" << endl;\n    }')'\n};'
"""

# short alias
P = List # P for pattern
V = List.Variable

# Create css pattern
css = P("""
/* General App Style */
QWidget {
font-family: "Segoe UI", sans-serif;
font-size: """, V(P("QWidget", "font-size")),""";
background-color: """, V(P("QWidget", "background-color")),""";
color: """, V(P("QWidget", "color")),""";
}
""")

# Set defaults
css[V(P("QWidget", "font-size"))] = "14px"
css[V(P("QWidget", "background-color"))] = "#000000"
css[V(P("QWidget", "color"))] = "#ffffff"
css[V(P("QWidget", "color"))] += "#55555"
css[V(P("QWidget", "color"))] -= "#55555"

print(repr(css))

"""
P('\n/* General App Style */\nQWidget {\n    font-family: "Segoe UI", sans-serif
;\n    font-size: 'P('QWidget''font-size'):P('14px')';\n    background-color: 'P
('QWidget''background-color'):P('#000000')';\n    color: 'P('QWidget''color'):P(
'#ffffff')';\n}\n')
"""

# flatten test
css = P(css)

print("")

# Change color
css[V(P("QWidget", "color"))] = "#252525"

print(str(css))

"""
/* General App Style */
QWidget {
    font-family: "Segoe UI", sans-serif;
    font-size: 14px;
    background-color: #000000;
    color: #252525;
}
"""

a = P(V("hello"))
a[V("hello")] = P("hallo hello ") + V("hallo")
a[V("hallo")] = P("hello hallo ") + V("hello")

print(repr(a))
print(a)

"""
('hello':'hallo hello '('hallo':'hello hallo '('hello':)))
hallo hello hello hallo 
"""

a[V("hello")] += a[V("hallo")]

print(repr(a))
print(a)

"""
('hello':'hallo hello '('hallo':'hello hallo '('hello':))('hallo':'hello hallo '('hello':)))
hallo hello hello hallo hello hallo 
"""
