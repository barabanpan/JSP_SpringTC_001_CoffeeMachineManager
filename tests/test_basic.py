import sys
import unittest

sys.path.append('../')

from coffee_machine import CoffeeMachine


class TestCoffeeMachineClass(unittest.TestCase):
    def setUp(self):  # before each
        self.COFFEE = 100
        self.MILK = 1000
        self.c = CoffeeMachine(coffee=self.COFFEE, milk=self.MILK)

    def test_init(self):
        self.assertEqual(self.c.coffee, self.COFFEE)
        self.assertEqual(self.c.milk, self.MILK)
        self.assertGreater(len(self.c.beverages), 0,
                           "Should start with at least 1 beverage")

    def test_return_bevs(self):
        self.assertIsInstance(self.c.get_dict_of_available_beverages(), dict)

    def test_add_ingredients(self):
        self.c.add_coffee(5)
        self.c.add_milk(10)

        self.assertEqual(self.c.coffee, self.COFFEE + 5,
                         "Should add more coffee to the machine")
        self.assertEqual(self.c.milk, self.MILK + 10,
                         "Should add more milk to the coffee machine")

    def test_good_order(self):
        first = list(self.c.beverages.keys())[0]  # first key
        try:
            self.c.prepare_beverage(first)
        except Exception as e:
            self.fail(f"An unexpected exception '{e}' was raised!")

        self.assertEqual(self.c.coffee,
                         self.COFFEE - self.c.beverages[first].coffee,
                         "Should subtract coffee")
        self.assertEqual(self.c.milk,
                         self.MILK - self.c.beverages[first].milk,
                         "Should subtract milk")

    def test_bad_order(self):
        first = list(self.c.beverages.keys())[0]  # first key

        del self.c.beverages[first]
        self.assertRaises(Exception, self.c.prepare_beverage, first,
                          "Should not prepare non-existing beverages")

    def tearDown(self):
        import os

        # delete .sqltite from tests directory
        for file in os.listdir():
            if file.endswith(".sqlite"):
                os.remove(file)


if __name__ == "__main__":
    unittest.main()
