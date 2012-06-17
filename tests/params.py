#!/usr/bin/env python
# encoding: utf-8

from settings          import *
from yard.forms.params import *
from yard.exceptions   import InvalidParameterValue, ConversionError
from datetime          import datetime


def fail_validation(p, x):
    try:
        p._validate(x)
        return False
    except InvalidParameterValue:
        return True

def fail_conversion(p, x):
    try:
        p.convert(x)
        return False
    except ConversionError:
        return True


class TestIntegerParam(unittest.TestCase):
        
    def test_convert(self, param=IntegerParam):
        p = param()
        assert fail_conversion(p, RANDOM.string())
        number = RANDOM.number()
        assert number == p.convert(str(number))
    
    def test_default(self, param=IntegerParam):
        p = param()
        for i in range(-RANDOM.number(),RANDOM.number()):
            assert p._default(i) == i
        
        default = RANDOM.number()
        p = param(default=default)
        number = RANDOM.number()
        assert p._default(number) == number
        assert p._default(None) == default
        
        max_ = RANDOM.number()
        p = param(default=lambda x: min(x,max_))
        number = RANDOM.number(0,max_)
        assert p._default(number) == number
        assert p._default(RANDOM.number(max_,10)) == max_
        assert p._default(None) == None

    def test_validate(self, param=IntegerParam):
        p = param()
        for i in range(-RANDOM.number(),RANDOM.number()):
            assert p._validate(i) != None
            
        min_, max_ = -RANDOM.number(), RANDOM.number()
        p = param(min_value=min_, max_value=max_)
        assert fail_validation(p, min_-RANDOM.number())
        assert fail_validation(p, max_+RANDOM.number())
        
        max_ = RANDOM.number()
        p = param(max_value=max_)
        assert p._validate(-max_)
        assert fail_validation(p, max_+RANDOM.number())
        
        min_ = -RANDOM.number()
        p = param(min_value=min_)
        assert fail_validation(p, min_-RANDOM.number())
        assert p._validate(min_*-1)
    

class TestPositiveIntegerParam(TestIntegerParam):
    
    def test_conversion(self, param=PositiveIntegerParam):
        TestIntegerParam.test_convert(self, param)
        
    def test_default(self, param=PositiveIntegerParam):
        TestIntegerParam.test_default(self, param)
        
    def test_validate(self, param=PositiveIntegerParam):
        p = param()
        for i in range(0,RANDOM.number()):
            assert p._validate(i) != None
        assert fail_validation(p, -RANDOM.number())
        
        max_ = RANDOM.number()
        p = PositiveIntegerParam(max_value=max_)
        assert fail_validation(p, max_+RANDOM.number())


class TestFloatParam(TestIntegerParam):
    
    def test_convert(self, param=FloatParam):
        TestIntegerParam.test_convert(self, param)
        value = RANDOM.float()
        assert value == param().convert(str(value))
        
    def test_default(self):
        TestIntegerParam.test_default(self, FloatParam)

    def test_validate(self):
        TestIntegerParam.test_validate(self, FloatParam)
    

class TestPositiveFloatParam(TestPositiveIntegerParam):

    def test_convert(self, param=PositiveFloatParam):
        TestPositiveIntegerParam.test_convert(self, param)
        value = RANDOM.float()
        assert value == param().convert(str(value))

    def test_default(self):
        TestPositiveIntegerParam.test_default(self, PositiveFloatParam)

    def test_validate(self):
        TestPositiveIntegerParam.test_validate(self, PositiveFloatParam)


class TestCharParam(unittest.TestCase):

    def test_convert(self, param=CharParam):
        value = RANDOM.string()
        assert value == param().convert(value)
    
    def test_default(self, param=CharParam):
        default = RANDOM.string()
        p = param(default=default)
        assert p._default(None) == default
        string = RANDOM.string()
        assert p._default(string) == string
        
    def test_validate(self, param=CharParam):
        max_ = RANDOM.number()
        p = param(max_length=max_)
        assert fail_validation(p, RANDOM.string()*max_)
        assert p._validate(RANDOM.string(max_)) != None
        assert p._validate(RANDOM.string(max_))


class TestRegexParam(unittest.TestCase):
    
    def test_convert(self):
        value = RANDOM.string()
        assert value == RegexParam(r'.*').convert(value)
    
    def test_default(self):
        default = RANDOM.string()
        p = RegexParam(r'.*', default=default)
        assert p._default(None) == default
        string = RANDOM.string()
        assert p._default(string) == string
    
    def test_validate(self, param=CharParam):
        p = RegexParam(r'[0-9]*')
        assert fail_validation(p, RANDOM.string())
        assert p._validate(RANDOM.char_number())
        assert fail_validation(p, RANDOM.string())


class TestDateTimeParam(unittest.TestCase):

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
        assert p._default(None) == today
        string = RANDOM.string()
        assert p._default(string) == string


class TestDateParam(TestDateTimeParam):
    
    def test_convert(self):
        p = DateParam()
        assert p.convert('2012-1-01')
        assert fail_conversion(p, '2012-1-1 0:0:0')

    def test_default(self):
        TestDateTimeParam.test_default(self, DateParam)


class TestTimeParam(TestDateTimeParam):

    def test_convert(self):
        p = TimeParam()
        assert p.convert('1:1:1')
        assert p.convert('01:01')
        assert fail_conversion(p, '2012-1-1 0:0:0')
            
    def test_default(self):
        TestDateTimeParam.test_default(self, TimeParam)


class TestBooleanParam(unittest.TestCase):

    def test_convert(self):
        p = BooleanParam()
        for i in ['False', 'None', '0000']:
            assert not p.convert(i)
        assert p.convert(RANDOM.string())
        
    def test_default(self, param=BooleanParam):
        default = RANDOM.boolean()
        p = BooleanParam(default=default)
        assert p._default(None) == default, str(p._default(None))
        boolean = RANDOM.boolean()
        assert p._default(boolean) == boolean
        

class TestChoiceParam(unittest.TestCase):

    def test_validate(self):
        options = RANDOM.list_of_numbers()
        p = ChoiceParam(options)
        assert p._validate(RANDOM.choice(options))
        assert fail_validation(p, RANDOM.string())


class TestMultipleChoiceParam(unittest.TestCase):
    
    def test_convert(self):
        options = RANDOM.list_of_numbers()
        p = MultipleChoiceParam(options)
        assert p.convert('1,2') == [1,2]
        p = MultipleChoiceParam(options, sep='-')
        assert p.convert('1-2') == [1,2]
    
    def test_validate(self):
        options = RANDOM.list_of_numbers()
        p = MultipleChoiceParam(options)
        assert p._validate([RANDOM.choice(options),RANDOM.choice(options)])
        assert fail_validation(p, [RANDOM.string(), RANDOM.string()])


class TestPointParam(unittest.TestCase):

    def test_convert(self):
        p = PointParam()
        assert p.convert('1,1.1')
        assert fail_conversion(p, '1.1')


class TestIpAddressParam(unittest.TestCase):

    def test_validate(self):
        p = IpAddressParam()
        assert p.validate('1')
        assert p.validate('1.1.1.1')
        assert fail_validation(p, 'aa')
        assert fail_validation(p, '1.1.1.1.1.1.1.1.1.1')


class TestEmailParam(unittest.TestCase):

    def test_validate(self):
        p = EmailParam()
        assert p.validate('sth@wtv.com')
        assert p.validate('1.1@wtv.com')
        assert fail_validation(p, 'sthwtv')
        assert fail_validation(p, 'sth@wtv.1')
        assert fail_validation(p, 'sth@wtv.x')


class TestTimestampParam(unittest.TestCase):

    def test_convert(self):
        p = TimestampParam()
        assert p.convert('1')
        assert p.convert('11111')
        assert fail_conversion(p, 'a')
        assert fail_conversion(p, '11111111111111111')


if __name__ == '__main__':
    unittest.main()
