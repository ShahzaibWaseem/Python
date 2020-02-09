import unittest
import os
from ex_08 import *

file_name = "de-sentences-tatoeba.txt"
model = None


class TestTask1(unittest.TestCase):

    def setUp(self):
        print("Setting up TestTask1...")
        global model
        if not model:
            model = Ngram(file_name, 2)

    def test_model_class(self):
        global model
        self.assertIsInstance(model, type(Ngram()))

    def test_model_fields(self):
        global model
        self.assertEqual(model.filename, file_name)
        self.assertEqual(model.n, 2)
        self.assertEqual(model.raw_counts, dict())


class TestTask2(unittest.TestCase):

    def setUp(self):
        print("Setting up TestTask2...")
        global model
        if not model:
            model = Ngram(file_name, 2)
        if not model.raw_counts:
            model.extract_raw_counts()

    def test_raw_counts(self):
        global model
        self.assertEqual(model.raw_counts[('ein', 'Krimineller')], 10)
        self.assertEqual(model.raw_counts[('schaute', 'hinein')], 4)
        self.assertEqual(model.raw_counts[('Nacht', 'drei')], 2)
        self.assertEqual(model.raw_counts[(':', 'Russland')], 1)
        self.assertEqual(model.raw_counts[('!', 'Allerdings')], 1)


class TestTask3(unittest.TestCase):

    def setUp(self):
        print("Setting up TestTask3...")
        global model
        if not model:
            model = Ngram(file_name, 2)
        if not model.raw_counts:
            model.extract_raw_counts()
        if not model.prob:
            model.extract_probabilities()

    def test_prob(self):
        global model
        self.assertAlmostEqual(model.prob[('Voraussetzungen', 'sind')], 6.794386025306823e-07)
        self.assertAlmostEqual(model.prob[('Illustrierte', 'gesehen')], 2.264795341768941e-07)
        self.assertAlmostEqual(model.prob[('Vorerkrankungen', '?')], 2.264795341768941e-07)
        self.assertAlmostEqual(model.prob[('Das', 'Jahr')], 1.8118362734151528e-06)


class TestTask4(unittest.TestCase):

    def setUp(self):
        print("Setting up TestTask4...")
        global model
        if not model:
            model = Ngram(file_name, 2)
        if not model.raw_counts:
            model.extract_raw_counts()
        if not model.prob:
            model.extract_probabilities()
        if not model.cond_prob:
            model.extract_conditional_probabilities()

    def test_cond_prob(self):
        self.assertAlmostEqual(model.cond_prob[('Alltagshosen',)][('.',)], 1.0)
        self.assertAlmostEqual(model.cond_prob[('begrüße',)][('deine',)], 0.125)
        self.assertAlmostEqual(model.cond_prob[('begrüße',)][('dich',)], 0.25)
        self.assertAlmostEqual(model.cond_prob[('BOS',)][('Das',)], 0.041034422805316925)
        self.assertAlmostEqual(model.cond_prob[('!',)][('EOS',)], 0.8417396673484352)


class TestTask5(unittest.TestCase):

    def setUp(self):
        print("Setting up TestTask5...")
        global model
        if not model:
            model = Ngram(file_name, 2)
        if not model.raw_counts:
            model.extract_raw_counts()
        if not model.prob:
            model.extract_probabilities()
        if not model.cond_prob:
            model.extract_conditional_probabilities()

    def test_generate_random_token(self):
        global model
        self.assertIn(model.generate_random_token(('Ich',)), model.cond_prob[('Ich',)].keys())
        self.assertIn(model.generate_random_token((',',)), model.cond_prob[(','),].keys())
        self.assertIn(model.generate_random_token(('habe',)), model.cond_prob[('habe',)].keys())
        self.assertIn(model.generate_random_token(('Tom',)), model.cond_prob[('Tom',)].keys())


class TestTask6(unittest.TestCase):

    def setUp(self):
        print("Setting up TestTask6...")
        global model
        if not model:
            model = Ngram(file_name, 2)
        if not model.raw_counts:
            model.extract_raw_counts()
        if not model.prob:
            model.extract_probabilities()
        if not model.cond_prob:
            model.extract_conditional_probabilities()

    def test_generate_random_sentence(self):
        global model
        test_sent = model.generate_random_sentence()
        # 'BOS' and 'EOS' tags are removed
        self.assertNotIn('BOS', test_sent)
        self.assertNotIn('EOS', test_sent)
        # first and last tokens in the sentence are valid first/last tokens
        self.assertIn((test_sent[0],), model.cond_prob[('BOS',)])
        self.assertIn(('EOS',), model.cond_prob[(test_sent[-1],)])


if __name__ == '__main__':
    unittest.main()
