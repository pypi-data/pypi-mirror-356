import warnings
from dataclasses import dataclass
from unittest import TestCase

from dataclassabc import dataclassabc

from dataclass_exceptions.errors import *


class ExceptionsTestCase(TestCase):
    def test_can_throw(self):
        with self.subTest("Generic"):
            with self.assertRaises(GenericException) as cm:
                raise GenericException("generic message")
            self.assertEqual(cm.exception.message, "generic message")
        
        with self.subTest("InvalidArgumentTypeError"):
            with self.assertRaises(InvalidArgumentTypeError) as cm:
                raise InvalidArgumentTypeError("argument name", str, 101)
            
            self.assertEqual(cm.exception.name, "argument name")
            self.assertEqual(cm.exception.expected, str)
            self.assertEqual(cm.exception.actual, 101)
            self.assertEqual(cm.exception.message, "Invalid argument 'argument name' type: Expected str, got <class 'int'> instead.")
        
        with self.subTest("InvalidSignature"):
            with self.assertRaises(InvalidSignature) as cm:
                raise InvalidSignature("function_name")
            
            self.assertEqual(cm.exception.name, "function_name")
            self.assertEqual(cm.exception.message, "Invalid function_name signature.")
    
    def test_can_warning(self):
        @dataclassabc(frozen=True)
        class DerivedWarning(BaseExceptionABC, Warning):
            message: str
        
        with self.assertWarns(DerivedWarning) as cm:
            warnings.warn(DerivedWarning("warning message"))
        self.assertEqual(cm.warning.message, "warning message")
    
    def test_can_subclass(self):
        with self.subTest("Field form"):
            @dataclassabc(frozen=True)
            class DerivedExceptionWithField(BaseExceptionABC):
                message: str
            
            with self.assertRaises(DerivedExceptionWithField) as cm:
                raise DerivedExceptionWithField("custom message")
            self.assertEqual(cm.exception.message, "custom message")
        
        with self.subTest("Property form"):
            @dataclass(frozen=True)
            class DerivedExceptionWithProperty(BaseExceptionABC):
                @property
                def message(self) -> str:
                    return "custom message 101"
            
            with self.assertRaises(DerivedExceptionWithProperty) as cm:
                raise DerivedExceptionWithProperty
            self.assertEqual(cm.exception.message, "custom message 101")



if (__name__ == '__main__'):
    from unittest import main
    main()
