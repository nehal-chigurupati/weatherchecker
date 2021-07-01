
import pickle
#EX: "BUILD MODEL SVC WITH NAME FIRSTMODEL, TRAIN FIRSTMODEL WITH DATASET TRAININGSET_FILENAME_DIRECTORY, TEST FIRSTMODEL WITH DATASET TESTINGSET_FILENAME_DIRECTORY AND NAME SCORE TESTING_SET_SCORE, RETURN TESTING_SET_SCORE.
class Token:
    def __init__(self, name, ExpectedSuccessor=None, description="NA"):
        self.name = name
        self.ExpectedSuccessor = ExpectedSuccessor
        self.description = description

    def __str__(self):
        return str(self.name)

    def equals(self, OtherToken):
        return self.name == OtherToken.name

    def HasProperSuccessor(self, next_token):
        return next_token.equals(ExpectedSuccessor)

    def GetDescription(self):
        return self.description

    def PrintDescription(self):
        print(self.description)


class BaseTokens:
    """
    Each comma-delineated phrase in the example at the top is called an operation.
    The periods are called enders. The entire set of operations is called a sequence.
    A component of a compound operation is called a statement

    """
    def item():
        return Token("item", description="Anything that is being referenced, that is not an action. Does not need to have a successor.")
    def action():
        return Token("action", description="A specific action to be carried out on an item")
    def separator():
        return Token("separator", description="The end of a phrase")
    def ender():
        return Token("ender", description="Indicates the end of a sequence")
    def extender():
        return Token("extender",  description="Indicates a compound operation")

"""
Each of the following classes are called terms. Terms have an associated token that describe their type and role.
"""
class DataSet:
    def __init__(self, slotterm=""):
        self.keyphrase = "DATASET"
        self.name="DataSet"
        self.token = BaseTokens.item()
        self.slotterm = slotterm

    def keyphrase(self):
        return self.keyphrase

    def assignSlotterm(self, slotterm):
        self.slotterm = slotterm

    def token(self):
        return self.token

    def __str__(self):
        return "DataSet"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.keyphrase == other.keyphrase

    def retrieve(self):
        pass

class Name:
    def __init__(self, slotterm=""):
        self.keyphrase = "NAME"
        self.name='Name'
        self.token = BaseTokens.item()
        self.slotterm = slotterm

    def assignSlotterm(self, slotterm):
        self.slotterm = slotterm

    def __eq__(self, other):
        return self.keyphrase == other.keyphrase

    def __str__(self):
        return "Name"

    def __repr__(self):
        return self.__str__()

    def retrieve(self):
        pass

class Model:
    def __init__(self, slotterm=""):
        self.keyphrase = "MODEL"
        self.name="Model"
        self.token = BaseTokens.item()
        self.slotterm = slotterm

    def assignSlotterm(self, slotterm):
        self.slotterm = slotterm


    def __eq__(self, other):
        return self.keyphrase == other.keyphrase

    def __str__(self):
        return "Model"

    def __repr__(self):
        return self.__str__()

    def retrieve(self):
        pass

class Items:
    members = [DataSet, Name, Model]
    keyphrases = [DataSet().keyphrase, Name().keyphrase, Model().keyphrase]


    def identifyTerm(keyphrase):
        return Items.members[Items.keyphrases.index(keyphrase)]()

class Build:
    def __init__(self, AssociatedItem=None):
        self.name="Build"
        self.keyphrase = "BUILD"
        self.token = BaseTokens.action()
        self.AssociatedItem = AssociatedItem

    def assignAssociatedItem(self, AssociatedItem):
        self.AssociatedItem = AssociatedItem




    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.keyphrase == other.keyphrase

    def evaluate(self):
        pass

class Train:

    def __init__(self, AssociatedItem=None):
        self.name = "Train"
        self.keyphrase = "TRAIN"
        self.token = BaseTokens.action()
        self.AssociatedItem = AssociatedItem

    def assignAssociatedItem(self, AssociatedItem):
        self.AssociatedItem = AssociatedItem

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.keyphrase == other.keyphrase

    def __repr__(self):
        return self.__str__()

    def evaluate(self):
        pass

class Test:

    def __init__(self, AssociatedItem=None):
        self.name = "Test"
        self.keyphrase = "TEST"
        self.token = BaseTokens.action()
        self.AssociatedItem = AssociatedItem

    def assignAssociatedItem(self, AssociatedItem):
        self.AssociatedItem = AssociatedItem

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.keyphrase == other.keyphrase

    def __repr__(self):
        return self.__str__()

    def evaluate(self):
        pass

class With:

    def __init__(self, AssociatedItem=None):
        self.name = "With"
        self.keyphrase = "WITH"
        self.token = BaseTokens.action()
        self.AssociatedItem = AssociatedItem

    def assignAssociatedItem(self, AssociatedItem):
        self.AssociatedItem = AssociatedItem

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.keyphrase == other.keyphrase

    def __repr__(self):
        return self.__str__()

    def evaluate(self):
        pass

class Return:

    def __init__(self, AssociatedItem=None):
        self.name = "Return"
        self.keyphrase = "RETURN"
        self.token = BaseTokens.action()
        self.AssociatedItem = AssociatedItem

    def assignAssociatedItem(self, AssociatedItem):
        self.AssociatedItem = AssociatedItem

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.keyphrase == other.keyphrase

    def __repr__(self):
        return self.__str__()

    def evaluate(self):
        pass

class Actions:
    members = [Return, With, Test, Train, Build]
    keyphrases = [Return().keyphrase, With().keyphrase, Test().keyphrase, Train().keyphrase, Build().keyphrase]


    def identifyTerm(keyphrase):
        return Actions.members[Actions.keyphrases.index(keyphrase)]()

class And:

    def __init__(self):
        self.name = "And"
        self.keyphrase = "AND"
        self.token = BaseTokens.extender()

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.keyphrase == other.keyphrase

    def __repr__(self):
        return self.__str__()

class Extenders:
    members = [And]
    keyphrases = [And().keyphrase]

    def IdentifyTerm(keyphrase):
        return members[keyphrases.index(keyphrase)]()

class Operation:
    def __init__(self, text, terms=None, tokens=None, actions=None, items=None, extenders=None):
        self.text = text
        self.terms = []
        self.tokens = []
        self.actions = []
        self.items = []
        self.extenders = []

    def evaluate(self):
        pass

    def __str__(self):
        if len(self.terms) > 0:
            return ''.join(self.terms)
        else:
            return self.text

    def __repr__(self):
        return self.__str__()


class Sequence:
    def __init__(self, text):
        self.text = text
        self.operations = []

    def evaluate(self):
        pass
