from ml.TrainingEngine.Tokens import *

class Identifier:
    def isAction(word):
        return word in Actions.keyphrases

    def isItem(word):
        return word in Items.keyphrases

    def isExtender(word):
        return word in Extenders.keyphrases

    def getTerms(operation):
        wordList = operation.text.split()
        termList = []
        for i in range(len(wordList)):
            if Identifier.isAction(wordList[i]):
                termToken = Actions.identifyTerm(wordList[i])
                termItemToken = Items.identifyTerm(wordList[i+1])
                termItemToken.assignSlotterm(slotterm=wordList[i+2])
                termToken.assignAssociatedItem(termItemToken)
                termList.append(termToken)
                termList.append(termItemToken)
                operation.actions.append(termToken)
                operation.items.append(termToken)
        return termList


class Tokenizer:
    def __init__(self, sequence):
        self.sequence = Sequence(sequence)

    def GenerateOperations(self):
        raw_operations = self.sequence.text.split(",")
        raw_operations[-1].strip('.')
        operations = []
        for text in raw_operations:
            operations.append(Operation(text=text))
        self.sequence.operations = operations

        return operations

    def GenerateTerms(self):
        termsList = []
        for operation in self.sequence.operations:
            terms = Identifier.getTerms(operation)
            operation.terms = terms
            termsList.append(terms)

        return termsList
