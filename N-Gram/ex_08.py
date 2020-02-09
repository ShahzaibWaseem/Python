import re
import random

class Ngram:
    """
    A class for n-gram models based on a text file.

    :attr filename: the name of the file  that the model is based on
    :type filename: str
    :attr n: the number of tokens in the tuples
    :type n: int
    :attr raw_counts: the raw counts of the n-gram tuples
    :type raw_counts: dict[tuple[str*], int]
    :attr prob: the probabilities of the n-gram tuples
    :type prob: dict[tuple[str*], int]
    :attr cond_prob: the probability distributions over the respective next tokens for each n-1-gram
    :type cond_prob: dict[tuple[str*], dict[str, int]]
    """

    # Task 1
    def __init__(self, filename="", n=0):
        """
        Initialize an Ngram object.

        :param filename: The name of the file to base the model on.
        :param n: The number of tokens in the n-gram tuples.
        """
        self.filename=filename
        self.n=n
        self.raw_counts={}
        self.prob={}
        self.cond_prob={}

    # Task 2
    def extract_raw_counts(self):
        """
        Compute the raw counts for each n-gram occurring in the text.
        """
        tokens=[]
        file=open(self.filename, "r", encoding="utf-8")
        fileContent=file.readlines()

        for line in fileContent:
        	line=line[:-1]						# delete trailing newline character
        	lineToken=tokenize_smart(line)
        	N=len(lineToken)

        	tokens.append(lineToken)

        	for i in range(self.n - 1):
        		lineToken.append("EOS")			# adding BOS and EOS
        		lineToken.insert(0, "BOS")

        	for i in range(N + self.n - 1):
        		nGram=tuple(lineToken[i:i+self.n])
        		if nGram not in self.raw_counts:
        			self.raw_counts[nGram]=1
        		else:
        			self.raw_counts[nGram]+=1

        file.close()

    # Task 3
    def extract_probabilities(self):
        """
        Compute the probability of an n-gram occurring in the text.
        """
        sumAllCount=sum(self.raw_counts.values())
        for key in self.raw_counts:
        	self.prob[key]=self.raw_counts[key]/sumAllCount

    # Task 4
    def extract_conditional_probabilities(self):
        """
        Compute the probability distribution over the next tokens given an n-1-gram.
        """
        for key in self.prob:
        	mgram=tuple(key[:self.n-1])
        	unigram=tuple(key[-1:])

        	if mgram not in self.cond_prob:
        		self.cond_prob[mgram]={}
        	self.cond_prob[mgram][unigram]=self.prob[key]

        for dictionary in self.cond_prob:
        	dictSum=sum(self.cond_prob[dictionary].values())

        	for unigramValues in self.cond_prob[dictionary]:
        		self.cond_prob[dictionary][unigramValues]/=dictSum

    # Task 5
    def generate_random_token(self, mgram):
        """
        Generate a random next token based on an n-1 gram,
        taking into account the probability distribution over the possible next tokens for that n-1-gram.

        :param mgram: the n-1 gram to generate the next token for.
        :type mgram: a tuple (of length n-1) of strings.
        :return a random next token for the n-1-gram.
        :rtype str
        """
        return random.choices(list(self.cond_prob[mgram].keys()), weights=list(self.cond_prob[mgram].values()), k=1)[0]

    # Task 6
    def generate_random_sentence(self):
        """
        Generate a random sentence.

        :return a random sentence
        :rtype list[str]
        """
        sentence=[]
        mgram=tuple()


        for i in range(self.n - 1):
        	mgram+=("BOS",)
        	sentence.insert(0, "BOS")

        while True:
        	mgram=self.generate_random_token(mgram)
        	sentence.append(mgram[0])
        	if "EOS" in mgram:
        		break

        for i in range(self.n - 1):
        	sentence.pop(0)			# remove "BOS"
        	sentence.pop()			# remove "EOS"

        return sentence

def tokenize_smart(sentence):
    """
    Tokenize the sentence into tokens (words, punctuation).

    :param sentence: the sentence to be tokenized
    :type sentence: str
    :return: list of tokens in the sentence
    :rtype: list[str]
    """
    tokens = []

    for word in re.sub(r" +", " ", sentence).split():
        word = re.sub(r"[\"„”“»«`\(\)]", "", word)
        if word != "":
            if word[-1] in ".,!?;:":
                if len(word) == 1:
                    tokens += [word]
                else:
                    tokens += [word[:-1], word[-1]]
            else:
                tokens.append(word)

    return tokens


def list2str(sentence):
    """
    Convert a sentence given as a list of strings to the sentence as a string separated by whitespace.

    :param sentence: the string list to be joined
    :type sentence: list[str]
    :return: sentence as a string, separated by whitespace
    :rtype: str
    """
    sentence = ' '.join(sentence)
    sentence = re.sub(r" ([\.,!\?;:])", r"\1", sentence)
    return sentence


if __name__ == '__main__':
    # Task 1
    ngram_model = Ngram("de-sentences-tatoeba.txt", 2)
    print(ngram_model.n, ngram_model.filename)
    print(ngram_model.raw_counts, ngram_model.prob, ngram_model.cond_prob)
    # Task 2
    ngram_model.extract_raw_counts()
    print(ngram_model.raw_counts[("kaltes", "Land")])
    print(ngram_model.raw_counts[("schönes", "Land")])
    # Task 3
    ngram_model.extract_probabilities()
    print(ngram_model.prob[("kaltes", "Land")])
    print(ngram_model.prob[("schönes", "Land")])
    # Task 4
    ngram_model.extract_conditional_probabilities()
    print(ngram_model.cond_prob[("beobachteten",)])
    print(ngram_model.cond_prob[("schönes",)][("Land",)])
    # Task 5
    print(ngram_model.generate_random_token(("den",)))
    print(ngram_model.generate_random_token(("den",)))
    print(ngram_model.generate_random_token(("den",)))
    # Task 6
    print(list2str(ngram_model.generate_random_sentence()))
    print(list2str(ngram_model.generate_random_sentence()))