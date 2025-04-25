from patlang import *

print("==== TREE ====")

# short alias
T = Tree
P = T() # P for pattern
V = Tree.Variable

P["groceries"]["get"][" "][V("groceries")][" "]["@"][" "]["the"][" "][V("market", "Market")]

print(repr(P))
print(repr(P["groceries"]))

"""
'groceries''get'' ''groceries':' ''@'' ''the'' ''market':'Market'
'get'' ''groceries':' ''@'' ''the'' ''market':'Market'
"""

P.setVariable("groceries", Tree("3 bananas"))
P.getVariable("groceries")[Tree(","," ","5 apples")]
P.setVariable("groceries", P.getVariable("groceries") + Tree(","," ","2 pineapples"))

P.setVariable("market", "fleemarket")
P.setVariable("market", P.getVariable("market") + " or " + "supermarket")

print(repr(P["groceries"]))
print(str(P["groceries"]))

"""
'get'' ''groceries':'3 bananas'','' ''5 apples'','' ''2 pineapples'' ''@'' ''the'' ''market':'fleemarket or supermarket'
get 3 bananas, 5 apples, 2 pineapples @ the fleemarket or supermarket
"""

P.setItem(" ","-")

print(str(P["groceries"]))

"""
get-3 bananas,-5 apples,-2 pineapples-@-the-fleemarket or supermarket
"""

#P.setItem("-"," ")

#print(str(P["groceries"]))

"""
get 3 bananas,-2 pineapples @ the fleemarket or supermarket
"""

#P["groceries"][" "]["a"][V("market")]
#P["groceries"][" "]["b"][V("groceries")]

#P.setVariable("market", P.getVariable("market"))
#P.setVariable("groceries", P.getVariable("groceries"))

#print(repr(P["groceries"]))

"""
'get'' ''groceries':'3 bananas,-2 pineapples'' ''@'' ''the'' ''market':'fleemarket or supermarket''__''a''market':'fleemarket or supermarket''__''b''groceries':'3 bananas,-2 pineapples'
"""

print("3 bananas" in P["groceries"]) # True
print("bananas" in P["groceries"]) # False
print("5 apples" in P["groceries"]) # True
print("groceries" in P["groceries"]) # False
print(V("groceries") in P["groceries"]) # True
print("get " in P["groceries"]) # False
print("get" in P["groceries"]) # True

P.setVariable("groceries", P.getVariable("groceries") - Tree(","," ","5 apples"))

P.setItem(" ","-")

print(str(P["groceries"]))

"""
get-3 bananas, 2 pineapples-@-the-fleemarket or supermarket-afleemarket or supermarket-b3 bananas, 2 pineapples
"""
print("3 bananas" in P["groceries"]) # False

P.setVariable("groceries", P.getVariable("groceries") + V("groceries"))

# print(str(P["groceries"])) recursion error
