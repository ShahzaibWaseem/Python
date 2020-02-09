# Experiments with German N-grams
In this assignment, you arc going to use conditional probability distributions over word N-grams extracted from a collection of German sentences to produce random (and sometimes amusing) German sentences. As a preview. here are sonic random "sentences" generated from trigrams from our solution:

- "Maria schlug eine Warrnflasc.he in ein Verzeic.hnis."
- "Der Winterschlussverkauf hat wieder geheiratet."
- "Dieser Wein ist stark wie eine Miin2e werfen."
- "Toms AuBening mass wieder lherstuncien gesanunelt and getrocknet hat."
- "Unsere Epoche ist eine enigmatische, seltsaine and anspornende Dichterin."

As a reminder! an N-gram is a sequence of N consecutive tokens in a sequence, which we are going to model as tuples of strings. To extract the N-grains from a sentence, the option we take here is to append N-1 dummy tokens to both the beginning of the sentence ("BOS" = "beginning of sentence") and to the end ("EOS" = "end of sentence").

With this extension, the bigram	(2-grams) in the sentence "This is the second last assignment.", tokenized to ['This", " is", "the", "second", "last", "assignment", "."], will be ("BOS", "This"), ("This", "is"), ("is", "the"), ("the" "second"), ("second","last"), ("last", "assignment"), ("assignment", ".”), and (“.”, “EOS”).

The trigrarms	 (3-grams) are	("BOS", "BOS", "This"), ("BOS", "This", "is").	("This", "is", 'the"), ("is", "the","second"), 	("the","second", "last "). ("second", "last", "assignment"), ("last ", "assignment", "."), ("assignment", “.”, “EOS"), and	(".”, “EOS", "EOS").

The code you will write in this assignment should be general enough to support any N > 1.

## Task 1: A Class for Storing N-gram Models

Your first step is to define a class which will be used to model the N-gram model over a text. The class must be called __Ngram__, and it needs a constructor with arguments filename (the path to a file from which the model will be extracted) and n (representing N). The default value for filename must be the empty string, and n will be zero if not specified otherwise, In addition to the filename and N, the class must. have three dictionaries as instance variables, which need to be initialized by the constructor, but are going to be filled during the later tasks. Their names must be __raw_counts__, __prob__, and __cond_prob__.

Example Usage:
![A Class for Storing N-gram Models](https://github.com/ShahzaibWaseem/Python/blob/master/N-Gram/images/1.png?raw=true)

## Task 2: Extracting N-grain Counts

The first step towards modeling the conditional distribution is to extract the raw N-gram counts from the sentence collection. This time. we are providing you with an adapted smart tokenization function tokenize_smart (sentence) which already splits the input sentences well enough into tokens. Use this function in a method extract_raw_counts 0 of your class, which fills the dictionary assigned to the raw_counts instance variable with raw N-gram counts. The logical structure of your code should he as follows:

```
for each line in the file
	cut off the trailing newline character
	tokenize the sentence (= the line) using the function provided
	append N-1 instances of "BOS" and "EOS" to the beginning and the end of the token list
	starting at each position i in the token list
		put the tokens from i to i+N into a new tuple (= the N-gram)
		increase the count of the N-grain in raw_counts by 1
		(adding the N-gram as a key if previously not present)
```

Example Usage:
![Extracting N-grain Counts](https://github.com/ShahzaibWaseem/Python/blob/master/N-Gram/images/2.png?raw=true)

## Task 3: Computing N-gram Probabilities

The next step is to convert the raw frequency counts into probabilities. For the implementation of the class method __extract_probabilities()__, you need to compute the sum of all raw counts (= the total number of N-grams in the sentence list), and then fill the dictionary assigned to the _prob_ instance variable with the raw counts divided by the sum of all counts.

Example Usage:
![Computing N-gram Probabilities](https://github.com/ShahzaibWaseem/Python/blob/master/N-Gram/images/3.png?raw=true)

## Task 4: Computing Conditional Unigram Probabilities

Now we can build the model giving us the conditional probabilities of the next token given the N-1 previous tokens. The implementation of the required class method __extract_conditional_probabilities()__ amounts to building and storing a probability distribution over all possible following tokens for each N-1-gram which occurred in the corpus. The lookup structure will be stored in the value of the __cond_prob__ instance variable. For our example with N = 2, looking up how likely the token "viele" is after "sehe" is done via model. __cond_prob [("sehe", )]["viele"]__ (BTW: the notation (token.) is necessary in the bigram case to enforce that a unary tuple is looked up, because (token) = token in Python). The recommended local structure of your implementation is as follows:


```
for each N-gram contained as a key in prob
	split the N-gram into the first N-1 tokens (the "mgram") and the final unigram
	if the mgram is not yet a key in cond_prob, store a new dictionary under that key
	set the value for the unigram in cond_prob[mgram] to the probability of the N-gram
for every dictionary in the values of cond_prob
	add up the values assigned to all unigram keys
	divide the value under each unigram by the sum of values
```

Example Usage:
![Computing Conditional Unigram Probabilities](https://github.com/ShahzaibWaseem/Python/blob/master/N-Gram/images/4.png?raw=true)

## Task 5: Generating Random Tokens in Context

Finally, we have the probability distribution that can he used to sample plausible next token given the previous N-1 tokens. Implement this functionality in a new class method __generate_random_token(mgram)__, which takes a N-1-gram in the tuple encoding, and randomly generates a plausible next token by sampling from the probability distribution you stored in __cond_prob[mgram]__ . In Python 3.6 or higher (the version you should he using), this can easily be done using the __choices()__ function from the package _random_. Compare the documentation, or the slides of Session 11. for usage examples. All you really need to do for this task is to prepare two lists, and feed them to choices() as arguments.

Example Usage:
![Generating Random Tokens in Context](https://github.com/ShahzaibWaseem/Python/blob/master/N-Gram/images/5.png?raw=true)


## Task 6: Generating Random Sentences

The last step is to implement the method __generate_random_sentence()__ for generating a random sentence with the help of the __generate_random_token(mgram)__ function. The key idea is to initialize the sentence with a list of N-1 instances of "EOS", and adding random words based on the last N-1 of the current list until "EOS" is generated for the first time. Removing the "BOS" and "EOS" dummy tokens from the resulting list gives you the final sentence to return. You can use the provided helper function __list2str(sentence)__ to format the generated sentence list as a string.
Example Usage:
![Generating Random Sentences](https://github.com/ShahzaibWaseem/Python/blob/master/N-Gram/images/6.png?raw=true)