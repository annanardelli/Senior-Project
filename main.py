import pandas as pd

file_name = "products.txt"

tilde = "~".encode()
comma_space = ", ".encode()
semicolon = ";".encode()
double_tilde = "~~".encode()
none = ", None, ".encode()
metered_inhalation = "metered;inhalation".encode()
metered_space = "metered inhalation".encode()
inh_semicolon = "INH;EQ".encode()
inh_slash = "INH/EQ".encode()
inh_zero = "INH;0".encode()
inh_dash_zero = "INH-0".encode()
discn = "DISCN~".encode()

with open(file_name, "rb") as file:
    data = file.read()
    data = data.replace(inh_semicolon, inh_slash)
    data = data.replace(inh_zero, inh_dash_zero)
    data = data.replace(discn, "".encode())
    data = data.replace(metered_inhalation, metered_space)
    data = data.replace(double_tilde, none)
    data = data.replace(tilde, comma_space)
    data = data.replace(semicolon, comma_space)


edited_file = "products_edited.txt"
with open(edited_file, "wb") as file:
    file.write(data)

read_file = pd.read_csv(edited_file)
read_file.to_csv("products.csv", index=None)