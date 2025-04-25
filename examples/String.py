from patlang import *

print("==== STRING ====")

groceries = String("get groceries")

print(repr(groceries))

"""
get groceries
"""

groceries["groceries"] = "3 bananas"
groceries["groceries"] += ", 5 apples"
groceries["groceries"] += ", 2 pineapples"

print(groceries)

"""
get 3 bananas, 5 apples, 2 pineapples
"""

print(repr(groceries))

"""
get 'groceries':'3 bananas, 5 apples, 2 pineapples'
"""

print("3 bananas" in groceries) # True
print("bananas" in groceries) # True
print("5 apples" in groceries) # True
print("groceries" in groceries) # True
print(List.Variable("groceries") in groceries) # False
print("get " in groceries) # True
print("get" in groceries) # True

print("6 apples" in groceries) # False

groceries["5"] = "6"

print("6 apples" in groceries) # True

print(repr(groceries))

"""
'get 'groceries':"3 bananas, ''5':'6'':'6' apples, 2 pineapples"'
"""

groceries = String(groceries)
print(repr(groceries))

"""
'get 3 bananas, 6 apples, 2 pineapples'
"""

cpp_class = String("""class V_ClassName {
public:
// Default constructor
V_ClassName() {
    V_Constructor
}

V_PublicFunctions
};""")

cpp_class["V_Constructor"] = 'cout << "Default constructor called!" << endl;'
cpp_class["V_PublicFunctions"] = """// A simple member function
void greet() {
    cout << "Hello from V_ClassName!" << endl;
}"""

cpp_class["V_ClassName"] = "SomeNewClass"

print(cpp_class)

"""class SomeNewClass {
public:
// Default constructor
SomeNewClass() {
    cout << "Default constructor called!" << endl;
}

// A simple member function
void greet() {
    cout << "Hello from SomeNewClass!" << endl;
}
};"""

print(repr(cpp_class))

"""
'class 'MyClass':'SomeNewClass' {\npublic:\n    // Default constructor\n
'MyClass':'SomeNewClass'() {\n        '#Constructor':'cout << "Default const
ructor called!" << endl;'\n    }\n    \n    '#PublicFunctions':'// A simple
member function\n    void greet() {\n        cout << "Hello from SomeNewClas
s!" << endl;\n    }'\n};'
"""

a = String("hello")
a["hello"] = "hallo hello"
a["hallo"] = "hello hallo"

print(repr(a))
print(a)

"""
''hello':'hello 'hallo':'hallo hello hallo' hello''
hello hallo hello hallo hello
"""

a.flush()

print(repr(a))
print(a)

"""
''hello':'hello 'hallo':'hallo hello hallo hello hallo' hello 'hallo':'hallo hello hallo hello hallo' hello''
hello hallo hello hallo hello hallo hello hallo hello hallo hello hallo hello
"""
