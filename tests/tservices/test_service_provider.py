import unittest

from services.service_provider import ServiceProvider


class TestServiceProvider(unittest.TestCase):

    def setUp(self):
        self.sp = ServiceProvider()

        self.sp.register(name="PI")(3.141592)

        @self.sp.register()
        def foo(*args):
            return sum(args)

        @self.sp.register(name="UpperCase")
        class UpperCaseRepresentation:
            def __init__(self, value):
                self.value = value

            def __str__(self):
                return self.value.upper()

    def test_inject_into_function(self):

        @self.sp.inject("UpperCase", "PI", sum_args="foo")
        def bar(a, b, c, UpperCase, PI, sum_args):
            return str(UpperCase("abc")), PI, sum_args(a, b, c, 4, 5)

        result_tuple = bar(1, 2, 3)
        self.assertEqual(result_tuple[0], "ABC")
        self.assertEqual(result_tuple[1], 3.141592)
        self.assertEqual(result_tuple[2], 15)

    def test_inject_into_class(self):
        class Foo:

            @self.sp.inject("foo")
            def my_method(self, a, b, foo, kwarg1=30, *, kwarg2=8):
                return foo(a, b, kwarg1, kwarg2)

        self.assertEqual(Foo().my_method(1, 2, kwarg1=50), 61)
        self.assertEqual(Foo().my_method(1, 2), 41)
