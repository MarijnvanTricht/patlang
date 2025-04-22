"""
patlang.py

Author: Marijn van Tricht
Date: 2025-04-17
Description:
    Pattern language, contains:
    String
    List (& List.Variable)
    Tree (& Tree.Variable)
"""

class String(str):
    """
    a patlang String
    """
    
    def __new__(cls, value = ""):
        """
        new Pattern (String) with value, because string is immutable
        """ 
        pat = super().__new__(cls, value)
        pat.variables = dict()
        return pat

    def __getitem__(self, key):
        return self.variables[key]
    
    def __setitem__(self, key, value):
        self.variables.update({key: value})    

    def __add__(self, other):
        pat = Pattern(super().__add__(other))
        pat.variables = self.variables
        if isinstance(other, String):
            pat.variables.update(other.variables)
        return pat

    def __eq__(self, other, strict=True):
        if not strict:
            return str(self) == str(other)
        if isinstance(other, String):   
            return repr(self) == repr(other)
        return False
    
    def __str__(self):
        out = super().__str__()
        variables = dict(self.variables)

        for key in variables:
            for otherKey in variables:
                if key != otherKey:
                    variables[otherKey] = variables[otherKey].replace(str(key), str(self.variables[key]))
        
        for key in variables:
            out = out.replace(str(key), str(variables[key]))
            
        return out

    def __contains__(self, key):
        if isinstance(key, str):
            if (key in str(self)):
                return True
            elif (key in self.variables):
                return True
        elif isinstance(key, String):
            if (str(key) in str(self)):
                return True
            elif (key in self.variables):
                return True
        return False

    def __repr__(self):
        out = super().__repr__()
        variables = dict(self.variables)

        for key in variables:
            for otherKey in variables:
                if key != otherKey:
                    variables[otherKey] = variables[otherKey].replace(str(key), repr(key) + ":" + repr(variables[key]))
        
        for key in variables:
            out = out.replace(str(key), repr(key) + ":" + repr(variables[key]))
            
        return out

    def flush(self):
        variables = dict(self.variables)
        
        for key in variables:
            for otherKey in variables:
                if key != otherKey:
                    variables[otherKey] = variables[otherKey].replace(str(key), str(self.variables[key]))
                    
        self.variables = variables

    # for compatiblity accross other patlang types
    def setItem(self, key, value):
        """
        set 'static' item
        """
        self.setVariable(key, value)

    # for compatiblity accross other patlang types
    def getItem(self, key):
        """
        get static item
        """  
        if key in self:
            return key

    # for compatiblity accross other patlang types
    def setVariable(self, key, value):
        """
        set variable item
        """ 
        self[key] = value

    # for compatiblity accross other patlang types
    def getVariable(self, key):
        """
        get variable item
        """  
        return self[key]
        
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
            return self.getVariable(key.name, flattend)
        else:
            return self.getItem(key, flattend)

    def __setitem__(self, key, value, flattend = True):
        """
        will set a nested (if flattend) variable (if key is variable) or item whose name is matching the key
        """
        if isinstance(key, List.Variable):
            self.setVariable(key.name, value, flattend)
        else:
            self.setItem(key, value, flattend)

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

    def setItem(self, key, value, flattend=True):
        """
        set static item
        """ 
        for index, item in enumerate(self):
            if item == key:
                super().__setitem__(index, value)
            else:
                if isinstance(item, List) and flattend:
                    item[key] = value

    def getItem(self, key, flattend=True):
        """
        get static item
        """  
        for item in self:
            if item == key:
                return item
            else:
                if isinstance(item, List) and flattend:
                    n = item[key]
                    if n: return n;

    def setVariable(self, key, value, flattend=True):
        """
        set variable item
        """ 
        for item in self:
            if type(item) is List.Variable:
                if item.name == key:
                    item.clear()
                    if type(value) is List:
                        item.extend(value)
                    else:
                        item.append(value)
                elif flattend:
                    item.setVariable(key, value)

    def getVariable(self, key, flattend=True):
        """
        get variable item
        """  
        for item in self:
            if type(item) is List.Variable:
                if item.name == key:
                    return item
                elif flattend:
                    n = item.getVariable(key)
                    if n: return n;
    
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

class Tree():
    """
    Tree is a node to a 2D tree
    """

    def __init__(self, value="", *args):
        self._lower_node = None
        self._next_node = None
        self.value = value
        if len(args) > 0: self._addmerge(*args);

    # add if not there
    def _addnext(self, value):
        if self._next_node == None:
            self._next_node = Tree(value)
            return self._next_node
        else:
            if isinstance(value, VariableTree):
                if isinstance(self._next_node, VariableTree):
                    if self._next_node.name == value.name:
                        return self._next_node
            elif self._next_node.value == value:
                return self._next_node
            return self._next_node._addbelow(value)

    # add if not there
    def _addbelow(self, value):
        if self._lower_node == None:
            self._lower_node = Tree(value)
            return self._lower_node
        else:
            if self._lower_node.value == value:
                return self._lower_node
            return self._lower_node._addbelow(value)

    def _addmerge(self, *args):
        node = self
            
        for arg in args:
            node = node._addnext(arg)

        return node
        
    def __getitem__(self, key):
        return self._addmerge(key)

    def __setitem__(self, key, value):
        node = self._addmerge(key)
        node.value = value
        return node

    def __add__(self, other):
        return ""

    def __sub__(self, other):
        return ""

    def __contains__(self, key):
        return False

    def __iter__(self):
        self.routes = [(self,[])]
        return self

    def __next__(self):
        if len(self.routes) > 0:
            node, path = self.routes.pop()
            while node != None:
                if node._lower_node != None:
                    self.routes.append((node._lower_node, list(path)))
                path.append(node)

                node = node._next_node
            return path
        else:
            raise StopIteration
    
    def __str__(self, endline=""):
        """
        return serialized string of self
        """
        out = ""
        
        for path in self:
            for item in path:
                out += str(item.value)
            out += str(endline)
                
        return out

    def __repr__(self, endline=""):
        """
        return serialized repr of self
        """
        out = ""
        
        for path in self:
            for item in path:
                if isinstance(item, VariableTree):
                    out += repr(item.name) + ":"
                out += repr(item.value)
            out += repr(endline)
        
        return out

    def _copy(self, newPattern):
        """
        private copy, cause self_type cannot be as default argument
        """
        return ""

    def copy(self):
        return self._copy(Pattern())

    def setItem(self, key, value, flattend=True):
        """
        set static item
        """ 
        for path in self:
            for item in path:
                if item.value == key:
                    item.value = value

    def getItem(self, key, flattend=True):
        """
        get static item
        """
        for path in self:
            for item in path:
                if item.value == key:
                    return item

    def setVariable(self, key, value, flattend=True):
        """
        set variable item
        """
        for path in self:
            for item in path:
                if isinstance(item.value, VariableTree):
                    if item.value.name == key:
                        item.value.value = value
                if isinstance(item.value, Tree) and flattend:
                    item.value.setVariable(key, value, flattend)
        
    def getVariable(self, key, flattend=True):
        """
        get variable item
        """  
        for path in self:
            for item in path:
                if isinstance(item.value, VariableTree):
                    if item.value.name == key:
                        return item.value
                if isinstance(item.value, Tree) and flattend:
                    n = item.value.getVariable(key, flattend)
                    if n: return n;
    
class VariableTree(Tree):
    """
    a Variable is a Pattern with a name
    """
    
    def __init__(self, name = "", *args):
        super().__init__(*args)
        self.name = name
    
    def copy(self):
        newVariable = VariableTree(self.name)
        return self._copy(newVariable)

# propper alias
Tree.Variable = VariableTree

if __name__ == "__main__":

    # Test & usage example

    # String

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

    cpp_class["V_ClassName"] = "SomeNewClass"
    cpp_class["V_Constructor"] = 'cout << "Default constructor called!" << endl;'
    cpp_class["V_PublicFunctions"] = """// A simple member function
    void greet() {
        cout << "Hello from V_ClassName!" << endl;
    }"""
    
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

    
