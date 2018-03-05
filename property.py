class Property:
    """Indicates an object of property"""
    def __init__(self, square_feet='', beds='',
                 baths='', **kwargs):
        """Initializes property object by area, number
        of bedrooms and baths and other keyword arguments."""
        super().__init__(**kwargs)
        self.square_feet = square_feet
        self.num_bedrooms = beds
        self.num_baths = baths

    def display(self):
        """Prints property details."""
        print()
        print("PROPERTY DETAILS")
        print("================")
        print("square footage: {}".format(self.square_feet))
        print("bedrooms: {}".format(self.num_bedrooms))
        print("bathrooms: {}".format(self.num_baths))
        print()

    def prompt_init():
        """Returns dictionary with init params as keys and their values."""
        return dict(square_feet=input("Enter the square feet: "),
                    beds=input("Enter number of bedrooms: "),
                    baths=input("Enter number of baths: "))

    prompt_init = staticmethod(prompt_init)
    # making prompt_init static and available in all subclasses


def get_valid_input(input_string, valid_options):
    """
    Checks if input is valid, returns valid input.
    :param input_string: string to show when requesting input
    :param valid_options: list of valid input options
    """
    input_string += " ({}) ".format((", ".join(valid_options)))
    response = input(input_string)
    while response.lower() not in valid_options:
        response = input(input_string)
    return response


class Apartment(Property):
    """Indicates an apartment"""
    valid_laundries = ("coin", "ensuite", "none")
    valid_balconies = ("yes", "no", "solarium")

    def __init__(self, balcony='', laundry='', **kwargs):
        """Initializes apartment by balcony, laundry, area, number
        of bedrooms and baths."""
        super().__init__(**kwargs)
        self.balcony = balcony
        self.laundry = laundry

    def display(self):
        """Prints out the details about the apartment"""
        super().display()
        print()
        print("APARTMENT DETAILS")
        print("laundry: {}".format(self.laundry))
        print("has balcony: {}".format(self.balcony))
        print()

    def prompt_init():
        """Returns dictionary with init params as keys and their values."""
        parent_init = Property.prompt_init()
        laundry = get_valid_input(
                "What laundry facilities does "
                "the property have? ",
                Apartment.valid_laundries)
        balcony = get_valid_input(
                "Does the property have a balcony?",
                Apartment.valid_balconies)
        parent_init.update({
            "laundry": laundry,
            "balcony": balcony
        })
        return parent_init

    prompt_init = staticmethod(prompt_init)


class House(Property):
    """Indicates a house"""
    valid_garage = ("attached", "detached", "none")
    valid_fenced = ("yes", "no")

    def __init__(self, num_stories='',
                 garage='', fenced='', **kwargs):
        """Initializes a house from num of stories, garage, fenced boolean."""
        super().__init__(**kwargs)
        self.garage = garage
        self.fenced = fenced
        self.num_stories = num_stories

    def display(self):
        """Prints out the details about the house."""
        super().display()
        print()
        print("HOUSE DETAILS")
        print("# of stories: {}".format(self.num_stories))
        print("garage: {}".format(self.garage))
        print("fenced yard: {}".format(self.fenced))
        print()

    def prompt_init():
        """Returns dictionary with init params as keys and their values."""
        parent_init = Property.prompt_init()
        fenced = get_valid_input("Is the yard fenced? ",
                                 House.valid_fenced)
        garage = get_valid_input("Is there a garage? ",
                                 House.valid_garage)
        num_stories = input("How many stories? ")

        parent_init.update({
            "fenced": fenced,
            "garage": garage,
            "num_stories": num_stories
        })
        return parent_init

    prompt_init = staticmethod(prompt_init)


class Purchase:
    def __init__(self, property='', price='', taxes='', **kwargs):
        """
        Initializes a purchase.
        :param property: type of purchasing property - house or apartment
        :param price: price of the house
        :param taxes: taxes required
        """
        super().__init__(**kwargs)
        self.price = price
        self.taxes = taxes
        self.property = property

    def display(self):
        """Prints out the purchase details."""
        self.property.display()
        print()
        print("PURCHASE DETAILS")
        print("selling price: {}".format(self.price))
        print("estimated taxes: {}".format(self.taxes))
        print()

    def prompt_init(pr_type):
        """Returns dictionary with init params as keys and their values."""
        init = dict(
            price=input("What is the selling price (int) ?"),
            taxes=input("What are the estimated taxes (int) ? ")
        )
        if pr_type == 'house':
            args = House().prompt_init()  # adding House object to the purchase
            init.update(dict(property=House(**args)))
        elif pr_type == 'apartment':  # adding Apartment object to the purchase
            args = Apartment().prompt_init()
            init.update(dict(property=Apartment(**args)))
        return init
    prompt_init = staticmethod(prompt_init)


class Rental:
    def __init__(self, property='', furnished='', utilities='',
                 rent='', **kwargs):
        """Initializes a rental."""
        super().__init__(**kwargs)
        self.furnished = furnished
        self.rent = rent
        self.utilities = utilities
        self.property = property

    def display(self):
        """Prints out the details about the rental"""
        self.property.display()
        print("RENTAL DETAILS")
        print("rent: {}".format(self.rent))
        print("estimated utilities: {}".format(self.utilities))
        print("furnished: {}".format(self.furnished))

    def prompt_init(pr_type):
        """Returns dictionary with init params as keys and their values."""
        init = dict(
            rent=input("What is the monthly rent (int)? "),
            utilities=input("What are the estimated utilities? "),
            furnished=get_valid_input("Is the property furnished? ",
                                      ("yes", "no")))
        if pr_type == 'house':
            args = House().prompt_init() # adding Huose object to purchase
            init.update(dict(property=House(**args)))
        elif pr_type == 'apartment':
            args = Apartment().prompt_init() # adding Apartment object
            init.update(dict(property=Apartment(**args)))
        return init

    prompt_init = staticmethod(prompt_init)


class Agent:
    """Indicates a property agent."""
    type_map = {
        "rental": Rental,
        "purchase": Purchase,
        }

    def __init__(self):
        self.property_list = []

    def display_properties(self):
        """Prints details of all available properties."""
        for property in self.property_list:
            property.display()

    def add_property(self):
        """Adds one more property to the list."""
        property_type = get_valid_input(
                "What type of property? ",
                ("house", "apartment")).lower()
        payment_type = get_valid_input(
                "What payment type? ",
                ("purchase", "rental")).lower()
        PropertyClass = self.type_map[payment_type]
        init_args = PropertyClass.prompt_init(property_type)
        self.property_list.append(PropertyClass(**init_args))

    def houses_count(self):
        """Returns number of houses available"""
        c = 0
        for p in self.property_list:
            if isinstance(p.property, House):
                c += 1
        return c

    def apartments_count(self):
        """Returns number of apartments available"""
        c = 0
        for p in self.property_list:
            if isinstance(p.property, Apartment):
                c += 1
        return c

    def find_cheap_purchase(self, value=None, display=False):
        """Returns the cheapest purchase, or list of purchases cheaper
        than value if value is given. Displays info about these purchases"""
        l = [p for p in self.property_list if isinstance(p, Purchase)]
        a = [p for p in l if int(p.price) < value] if value else \
            [p for p in l if int(p.price) == min([int(p.price) for p in l])]
        if display:
            for el in a:
                el.display()
        return l
