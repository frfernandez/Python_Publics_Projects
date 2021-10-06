# Array of JSON Objects
products = [{"name": "HDD", "brand": "Samsung", "price": "$100"},
            {"name": "Monitor", "brand": "Dell", "price": "$120"},
            {"name": "Mouse", "brand": "Logitech", "price": "$10"}]

# Print the original data
print("The original JSON data:\n{0}".format(products))
# Sort the JSON data based on the value of the brand key
products.sort(key=lambda x: x["brand"])

# Print the sorted JSON data
print("The sorted JSON data based on the value of the brand:\n{0}".format(products))
