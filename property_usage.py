from property import Property, get_valid_input, Apartment, House,\
   Purchase, Rental, Agent


print("Creating Property example from '150', '2', '1'")
ppt = Property('150', '2', '1')
print("Displaying property:")
ppt.display()

print("Initializing an Agent")
a = Agent()
print("Please add 3 properties to the agents' list")
print("1")
a.add_property()
print("2")
a.add_property()
print("3")
a.add_property()

print("Displaying properties.")
a.display_properties()

print("Houses count {}".format(a.houses_count()))
print("Apartments count {}".format(a.apartments_count()))

print("Looking for cheap purchase..")
p = input("Enter maximum price: ")
a.find_cheap_purchase(int(p), display=True)

print("All right.")
