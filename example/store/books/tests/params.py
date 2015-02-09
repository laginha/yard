#!/usr/bin/env python
# encoding: utf-8
from django.test import TestCase
from yard.forms.parameters import *
from yard.exceptions import InvalidParameterValue, ConversionError
from .randomizer import Randomizer
from datetime import datetime

RANDOM = Randomizer()


def fail_validation(p, x):
    try:
        p.do_validate(x)
        return False
    except InvalidParameterValue:
        return True

def fail_conversion(p, x):
    try:
        p.convert(x)
        return False
    except ConversionError:
        return True


class IntegerParamTestCase(TestCase):
        
    def test_convert(self, param=IntegerParam):
        p = param()
        assert fail_conversion(p, RANDOM.string())
        number = RANDOM.number()
        assert number == p.convert(str(number))
    
    def test_default(self, param=IntegerParam):
        p = param()
        for i in range(-RANDOM.number(),RANDOM.number()):
            assert p.get_default(i)[0] == i
        
        default = RANDOM.number()
        p = param(default=default)
        number = RANDOM.number()
        assert p.get_default(number)[0] == number
        assert p.get_default(None)[0] == default

    def test_validate(self, param=IntegerParam):
        p = param()
        for i in range(-RANDOM.number(),RANDOM.number()):
            assert p.do_validate(i) != None
            
        min_, max_ = -RANDOM.number(), RANDOM.number()
        p = param(min_value=min_, max_value=max_)
        assert fail_validation(p, min_-RANDOM.number())
        assert fail_validation(p, max_+RANDOM.number())
        
        max_ = RANDOM.number()
        p = param(max_value=max_)
        assert p.do_validate(-max_)
        assert fail_validation(p, max_+RANDOM.number())
        
        min_ = -RANDOM.number()
        p = param(min_value=min_)
        assert fail_validation(p, min_-RANDOM.number())
        assert p.do_validate(min_*-1)
    

class PositiveIntegerParamTestCase(IntegerParamTestCase):
    
    def test_conversion(self, param=PositiveIntegerParam):
        IntegerParamTestCase.test_convert(self, param)
        
    def test_default(self, param=PositiveIntegerParam):
        IntegerParamTestCase.test_default(self, param)
        
    def test_validate(self, param=PositiveIntegerParam):
        p = param()
        for i in range(0,RANDOM.number()):
            assert p.do_validate(i) != None
        assert fail_validation(p, -RANDOM.number())
        
        max_ = RANDOM.number()
        p = PositiveIntegerParam(max_value=max_)
        assert fail_validation(p, max_+RANDOM.number())


class FloatParamTestCase(IntegerParamTestCase):
    
    def test_convert(self, param=FloatParam):
        IntegerParamTestCase.test_convert(self, param)
        value = RANDOM.float()
        assert value == param().convert(str(value))
        
    def test_default(self):
        IntegerParamTestCase.test_default(self, FloatParam)

    def test_validate(self):
        IntegerParamTestCase.test_validate(self, FloatParam)
    

class TestPositiveFloatParam(PositiveIntegerParamTestCase):

    def test_convert(self, param=PositiveFloatParam):
        PositiveIntegerParamTestCase.test_convert(self, param)
        value = RANDOM.float()
        assert value == param().convert(str(value))

    def test_default(self):
        PositiveIntegerParamTestCase.test_default(self, PositiveFloatParam)

    def test_validate(self):
        PositiveIntegerParamTestCase.test_validate(self, PositiveFloatParam)


class CharParamTestCase(TestCase):

    def test_convert(self, param=CharParam):
        value = RANDOM.string()
        assert value == param().convert(value)
    
    def test_default(self, param=CharParam):
        default = RANDOM.string()
        p = param(default=default)
        assert p.get_default(None)[0] == default
        string = RANDOM.string()
        assert p.get_default(string)[0] == string
        
    def test_validate(self, param=CharParam):
        max_ = RANDOM.number()
        p = param(max_length=max_)
        assert fail_validation(p, RANDOM.string()*max_)
        assert p.do_validate(RANDOM.string(max_)) != None
        assert p.do_validate(RANDOM.string(max_))


class RegexParamTestCase(TestCase):
    
    def test_convert(self):
        value = RANDOM.string()
        assert value == RegexParam(r'.*').convert(value)
    
    def test_default(self):
        default = RANDOM.string()
        p = RegexParam(r'.*', default=default)
        assert p.get_default(None)[0] == default
        string = RANDOM.string()
        assert p.get_default(string)[0] == string
    
    def test_validate(self, param=CharParam):
        p = RegexParam(r'[0-9]*')
        assert fail_validation(p, RANDOM.string())
        assert p.do_validate(RANDOM.char_number())
        assert fail_validation(p, RANDOM.string())


class DateTimeParamTestCase(TestCase):

    def test_convert(self, param=DateTimeParam):
        p = param()
        for i in ['2012-1-1 0:0:0', '2012-01-01 00:00', '2012-1-01']:
            assert p.convert(i)
        p = param(formats='%H:%M:%S %d-%m-%Y')
        assert p.convert('0:0:0 1-1-2012')
        assert fail_conversion(p, RANDOM.string())
    
    def test_default(self, param=DateTimeParam):
        today = datetime.today()
        p = param(default=today)
        assert p.get_default(None)[0] == today
        string = RANDOM.string()
        assert p.get_default(string)[0] == string


class DateParamTestCase(DateTimeParamTestCase):
    
    def test_convert(self):
        p = DateParam()
        assert p.convert('2012-1-01')
        assert fail_conversion(p, '2012-1-1 0:0:0')

    def test_default(self):
        DateTimeParamTestCase.test_default(self, DateParam)


class TimeParamTestCase(DateTimeParamTestCase):

    def test_convert(self):
        p = TimeParam()
        assert p.convert('1:1:1')
        assert p.convert('01:01')
        assert fail_conversion(p, '2012-1-1 0:0:0')
            
    def test_default(self):
        DateTimeParamTestCase.test_default(self, TimeParam)


class BooleanParamTestCase(TestCase):

    def test_convert(self):
        p = BooleanParam()
        for i in ['False', 'None', '0000']:
            assert not p.convert(i)
        assert p.convert(RANDOM.string())
        
    def test_default(self, param=BooleanParam):
        default = RANDOM.boolean()
        p = BooleanParam(default=default)
        assert p.get_default(None)[0] == default, str(p.get_default(None))
        boolean = RANDOM.boolean()
        assert p.get_default(boolean)[0] == boolean
        

class ChoiceParamTestCase(TestCase):

    def test_validate(self):
        options = RANDOM.list_of_numbers()
        p = ChoiceParam(options)
        assert p.do_validate(RANDOM.choice(options))
        assert fail_validation(p, RANDOM.string())


class MultipleChoiceParamTestCase(TestCase):
    
    def test_convert(self):
        options = RANDOM.list_of_numbers()
        p = MultipleChoiceParam(options)
        assert p.convert('1,2') == [1,2]
        p = MultipleChoiceParam(options, sep='-')
        assert p.convert('1-2') == [1,2]
    
    def test_validate(self):
        options = RANDOM.list_of_numbers()
        p = MultipleChoiceParam(options)
        assert p.do_validate([RANDOM.choice(options),RANDOM.choice(options)])
        assert fail_validation(p, [RANDOM.string(), RANDOM.string()])


class PointParamTestCase(TestCase):

    def test_convert(self):
        p = PointParam()
        assert p.convert('1,1.1')
        assert fail_conversion(p, '1.1')
        assert fail_conversion(p, '190,190')


class IpAddressParamTestCase(TestCase):

    def test_validate(self):
        p = IpAddressParam()
        assert p.validate('1')
        assert p.validate('1.1.1.1')
        assert fail_validation(p, 'aa')
        assert fail_validation(p, '1.1.1.1.1.1.1.1.1.1')


class EmailParamTestCase(TestCase):

    def test_validate(self):
        p = EmailParam()
        assert p.validate('sth@wtv.com')
        assert p.validate('1.1@wtv.com')
        assert fail_validation(p, 'sthwtv')
        assert fail_validation(p, 'sth@wtv.1')
        assert fail_validation(p, 'sth@wtv.x')


class TimestampParamTestCase(TestCase):

    def test_convert(self):
        p = TimestampParam()
        assert p.convert('1')
        assert p.convert('11111')
        assert fail_conversion(p, 'a')
        assert fail_conversion(p, '11111111111111111')


class CommaSeparatedValueParamTestCase(TestCase):

    def test_convert(self):
        p = CommaSeparatedValueParam()
        assert p.convert('1')
        assert p.convert('1,a') == ['1','a']


class CommaSeparatedIntegerParamTestCase(TestCase):

    def test_convert(self):
        p = CommaSeparatedIntegerParam()
        assert p.convert('1') == [1]
        assert p.convert('1,1') == [1, 1]
        assert fail_conversion(p, '1,a')
