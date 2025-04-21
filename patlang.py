"""
patlang.py

Author: Marijn van Tricht
Date: 2025-04-17
Description:
    Pattern language contains:
    List (& List.Variable)
    Tree (& Tree.Variable)
    String (not using variables, but token based)
"""

class List(list):
    """
    a patlang List
    """

    def __init__(self, *args):
        """
        Init a Pattern (list) with *args
        """ 
        super().__init__(args)
        
    def __getitem__(self, key, flattend = True):
        """
        will return a nested (if flattend) variable (if key is variable) or item whose name is matching the key
        """            
        if isinstance(key, slice):
            items = super().__getitem__(key)
            newPat = List()
            for item in items:
                newPat.append(item)
            return newPat

        if isinstance(key, List.Variable):
            """
            search for variable items
            """
            for item in self:
                if type(item) is List.Variable:
                    if item.name == key.name:
                        return item
                    elif flattend:
                        n = item[key]
                        if n: return n;

        else:
            """
            search for static items
            """
            for item in self:
                if item == key:
                    return item
                else:
                    if isinstance(item, List) and flattend:
                        n = item[key]
                        if n: return n;

    def __setitem__(self, key, value, flattend = True):
        """
        will set a nested (if flattend) variable (if key is variable) or item whose name is matching the key
        """

        if isinstance(key, List.Variable):
            """
            search for variable items
            """
            for index, item in enumerate(self):
                if type(item) is List.Variable:
                    if item.name == key.name:
                        item.clear()
                        if type(value) is List:
                            item.extend(value)
                        else:
                            item.append(value)
                    elif flattend:
                        item[key] = value

        else:
            """
            search for static items
            """
            for index, item in enumerate(self):
                if item == key:
                    super().__setitem__(index, value)
                else:
                    if isinstance(item, List) and flattend:
                        item[key] = value

    def __add__(self, other):
        pat = self._copy(List())
        if type(other) is List:
            pat.extend(other)
        else:
            pat.append(other)
        return pat

    def __iadd__(self, other):
        """
        return __add__
        """
        return self.__add__(other)

    def __sub__(self, other):
        pat = self._copy(List())
        if type(other) is List:
            for item in other:
                pat.remove(item)
        else:
            pat.remove(other)
        return pat

    def __isub__(self, other):
        """
        return __sub__
        """
        return self.__sub__(other)

    def __contains__(self, key):
        """
        if __getitem__ returns a valid item, this returns True
        """
        if self.__getitem__(key): return True
        return False
    
    def __str__(self):
        """
        return serialized string of self
        """
        return "" + "".join(map(str, self)) + ""

    def __repr__(self):
        """
        return serialized repr of self
        """
        return "" + "".join(map(repr, self)) + ""

    def _copy(self, newPattern):
        """
        private copy, because self_type cannot be given as default argument
        """
        for item in self:
            if hasattr(item, "copy"):
                newPattern.append(item.copy())
            else:
                newPattern.append(item)
        return newPattern

    def copy(self):
        """
        returns a copy of self as Pattern(self)
        """ 
        return self._copy(Pattern())
    
class VariableList(List):
    """
    a Variable is a Pattern with a name
    """
    
    def __init__(self, name = "", *args):
        """
        Init a variable with a name
        Rest *args will init the pattern
        """
        super().__init__(*args)
        self.name = name

    def __repr__(self):
        """
        return serialized repr of self (including name)
        """
        return "(" + repr(self.name) + ":" + "".join(map(repr, self)) + ")"
    
    def copy(self):
        """
        returns a copy of self as Variable()
        """ 
        newVariable = List.Variable(self.name)
        return self._copy(newVariable)

# propper alias
List.Variable = VariableList

if __name__ == "__main__":

    # Test & usage example

    # String

    

    

    # List

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

    cpp_class[List.Variable("Constructor")] = 'cout << "Default constructor called!" << endl;'
    cpp_class[List.Variable("PublicFunctions")] = List("""// A simple member function
    void greet() {
        cout << "Hello from """, List.Variable("ClassName"), """!" << endl;
    }""")

    cpp_class[List.Variable("ClassName")] = "SomeNewClass"
    
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

    # Tree
    
