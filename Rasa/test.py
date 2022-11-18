import re



test = "Which is faster O(n) or O(log(n))"
test = test.split()
def tokenize(the_text):
    the_text = the_text.split()
    bigO = []
    for x in the_text:
        if x.find("(") == 1:
            bigO.append(x.lstrip("O"))
    return bigO

print(tokenize())