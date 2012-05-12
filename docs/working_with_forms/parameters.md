# Parameters

All available parameter types have three core arguments:

- **alias:** Parameter's name within server's logic. If not given the parameter's name is used instead.
- **required:** Defines whether parameter is required or not.
- **default:** Defines the default value if none given in http request.


### IntegerParam

    IntegerParam( default=2012, min_value=1970, max_value=2012 )

Extra arguments:

- **min_value:** Defines the minimum value allowed.
- **max_value:** Defines the maximum value allowed.


### PositiveIntegerParam

    PositiveIntegerParam( default=2012 )

Extra arguments:

- **min_value:** Defines the minimum value allowed. Defaults to 0.
- **max_value:** Defines the maximum value allowed.


### CharParam

    CharParam( max_length=32 )

Extra arguments:

- **max_length:** Defines the maximum length allowed.


### RegexParam

    RegexParam( regex=r'[0-9][a-zA-Z]' )

Extra arguments:

- **regex:** Regex pattern that each value for this parameter must oblige to. (REQUIRED)


### FloatParam

    FloatParam()

Extra arguments:

- **min_value:** Defines the minimum value allowed.
- **max_value:** Defines the maximum value allowed.


### PositiveFloatParam

    PositiveFloatParam()

Extra arguments:

- **min_value:** Defines the minimum value allowed. Defaults to 0.
- **max_value:** Defines the maximum value allowed.


### DateTimeParam

    DateTimeParam( validate=lambda x: x<datetime.today(), formats='%d-%m-%Y')

Extra arguments:

- **validate:** Single-argument callable function used for parameter value validation.
- **formats:**  String or a list of Datetime formats as specified in the python's standard library. Defaults to ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d'].


### DateParam

    DateParam( validate=lambda x: x<datetime.today().date(), formats='%d-%m-%Y')

Extra arguments:

- **validate:** Single-argument callable function used for parameter value validation.
- **formats:**  String or a list of Datetime formats as specified in the python's standard library. Defaults to ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d'].


### TimeParam

    TimeParam( validate=lambda x: x<time(16,0) )

Extra arguments:

- **validate:** Single-argument callable function used for parameter value validation.
- **formats:**  String or a list of Datetime formats as specified in the python's standard library. Defaults to ['%Y-%m-%d'].


### BooleanParam

    BooleanParam()

- **default:** Defaults to True.


### ChoiceParam

    ChoiceParam( choices=['drama', 'comedy', 'action'] )

Extra arguments:

- **choices:** Allowed options for this parameter. (REQUIRED)


### ChoiceParam

    MultipleChoiceParam( choices=['drama', 'comedy', 'action'] )

Extra arguments:

- **choices:** Allowed options for this parameter. (REQUIRED)
- **sep:** Word separator for the input string. Defaults to ",".


### PointParam

    PointParam( validate=lambda x: x.coords[1]>0  ) 

*Note: expected input like: 40.0,8.0 (longitude, latitude)*

Extra arguments:

- **validate:** Single-argument callable function used for parameter value validation.

