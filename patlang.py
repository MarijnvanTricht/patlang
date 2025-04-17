"""
patlang.py

Author: Marijn van Tricht
Date: 2025-04-17
Description:
    Contains Pattern class which is a list which can have static items and dynamic (variable) items
    Variable items are created with the Variable class (which is a Pattern with a name)
"""

class Pattern(list):
    """
    Pattern is a list of items that is serialized into a string
    """

    def __init__(self, *args):
        super().__init__(args)
        
    def __getitem__(self, key, flattend = True):
        """
        if not slice,
        will return a nested (if flattend) variable whose name is matching the key
        """            
        if isinstance(key, slice):
            items = super().__getitem__(key)
            newPat = Pattern()
            for item in items:
                newPat.append(item)
            return newPat

        """
        Search for variables in the pattern
        """
        for item in self:
            if type(item) is Variable:
                if item.name == key:
                    return item
                elif flattend:
                    n = item[key]
                    if n: return n;

        """
        Second wind - expand search for items
        """
        for item in self:
            if item == key:
                return item
            else:
                if type(item) == Pattern and flattend:
                    n = item[key]
                    if n: return n;

    def __setitem__(self, key, value, flattend = True):
        """
        will set a nested (if flattend) variable whose name is matching the key
        """
        
        """
        Search for variables in the pattern
        """
        for index, item in enumerate(self):
            if type(item) is Variable:
                if item.name == key:
                    item.clear()
                    if type(value) is Pattern:
                        item.extend(value)
                    else:
                        item.append(value)
                elif flattend:
                    item[key] = value

        """
        Second wind - expand search for items
        """
        for index, item in enumerate(self):
            if item == key:
                super().__setitem__(index, value)
            else:
                if type(item) == Pattern and flattend:
                    item[key] = value

    def __add__(self, other):
        pat = self._copy(Pattern())
        if type(other) is Pattern:
            pat.extend(other)
        else:
            pat.append(other)
        return pat

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        pat = self._copy(Pattern())
        if type(other) is Pattern:
            for item in other:
                pat.remove(item)
        else:
            pat.remove(other)
        return pat

    def __isub__(self, other):
        return self.__sub__(other)

    def __contains__(self, key):
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
        private copy, cause self_type cannot be as default argument
        """
        for item in self:
            if hasattr(item, "copy"):
                newPattern.append(item.copy())
            else:
                newPattern.append(item)
        return newPattern

    def copy(self):
        return self._copy(Pattern())
    
class Variable(Pattern):
    """
    a Variable is a Pattern with a name
    """
    
    def __init__(self, name = ""):
        super().__init__()
        self.name = name

    def __repr__(self):
        """
        return serialized repr of self (including name)
        """
        return "(" + repr(self.name) + ":" + "".join(map(repr, self)) + ")"
    
    def copy(self):
        newVariable = Variable(self.name)
        return self._copy(newVariable)

if __name__ == "__main__":

    groceries = Pattern("get ",Variable("groceries"))

    print(repr(groceries))

    """
    'get '('groceries':)
    """

    groceries["groceries"] = "3 bananas"
    groceries["groceries"] += ", 5 apples"
    groceries["groceries"].append(", 2 pineapples")

    print("3 bananas" in groceries) # True
    print("bananas" in groceries) # False
    print("5 bananas" in groceries) # False
    print("groceries" in groceries) # True
    print("get " in groceries) # True
    print("get" in groceries) # False

    """
    get 3 bananas, 5 apples, 2 pineapples
    """

    print(repr(groceries))

    """
    'get '('groceries':'3 bananas'', 5 apples'', 2 pineapples')
    """
    
    cpp_class = Pattern("class ", Variable("ClassName"),""" {
public:
    // Default constructor
    """, Variable("ClassName"), """() {
        """, Variable("Constructor"), """
    }
    
    """, Variable("PublicFunctions"), """
};""")

    cpp_class["Constructor"] = 'cout << "Default constructor called!" << endl;'
    cpp_class["PublicFunctions"] = Pattern("""// A simple member function
    void greet() {
        cout << "Hello from """, Variable("ClassName"), """!" << endl;
    }""")

    cpp_class["ClassName"] = "SomeNewClass"
    
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
    P = Pattern
    V = Variable

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
    css[P("QWidget", "font-size")] = "14px"
    css[P("QWidget", "background-color")] = "#000000"
    css[P("QWidget", "color")] = "#ffffff"
    css[P("QWidget", "color")] += "#55555"
    css[P("QWidget", "color")] -= "#55555"

    print(repr(css))

    """
    P('\n/* General App Style */\nQWidget {\n    font-family: "Segoe UI", sans-serif
    ;\n    font-size: 'P('QWidget''font-size'):P('14px')';\n    background-color: 'P
    ('QWidget''background-color'):P('#000000')';\n    color: 'P('QWidget''color'):P(
    '#ffffff')';\n}\n')
    """

    print("")

    # Change color
    css[P("QWidget", "color")] = "#252525"

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

    a = Pattern(Variable("hello"))
    a["hello"] = Pattern("hallo hello") + Variable("hallo")
    a["hallo"] = Pattern("hello hallo") + Variable("hello")

    print(repr(a))
    print(a)
    
    """
    ('hello':'hallo hello'('hallo':'hello hallo'('hello':)))
    hallo hellohello hallo
    """

    a["hello"] += a["hallo"]

    print(repr(a))
    print(a)

    """
    ('hello':'hallo hello'('hallo':'hello hallo'('hello':))('hallo':'hello hallo'('hello':)))
    hallo hellohello hallohello hallo
    """
