class Car:

    cc_engine = 2000  # class variable, common to all   

    def __init__(self, model, color, for_sale):
        self.car_name = model
        self.car_color = color
        self.car_is_for_sale = for_sale

    def Drive(self):
        print(f"You can drive the car : {self.car_name}")

    def Stop(self):
        print(f"Stop the car :{self.car_name} of color {self.car_color}")


class India(Car):
    pass

class USA(Car):
    pass
    