class Item(object):
    def __init__(self, value, not_none=False, validators=(), **kwargs):
        self.value = value
        self.validators = validators

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value

    def validate(self):
        for validator in self.validators:
            assert validator(self.value)
