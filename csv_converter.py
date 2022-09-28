import pandas as pd

file_name = "products.txt"

#turning replacement strings into bits
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
amp = "AMPHETAMINE ASPARTATE; AMPHETAMINE SULFATE; DEXTROAMPHETAMINE SACCHARATE; DEXTROAMPHETAMINE SULFATE".encode()
amp_edited = "AMPHETAMINE ASPARTATE/AMPHETAMINE SULFATE/DEXTROAMPHETAMINE SACCHARATE/DEXTROAMPHETAMINE SULFATE".encode()
dext = "DEXTROAMP SACCHARATE, AMP ASPARTATE, DEXTROAMP SULFATE AND AMP SULFATE".encode()
dext_edited = "DEXTROAMP SACCHARATE-AMP ASPARTATE-DEXTROAMP SULFATE AND AMP SULFATE".encode()
mg_semicolon = "MG;".encode()
cap_ex = "CAPSULE, EXTENDED RELEASE".encode()
cap_ex_edited = "CAPSULE: EXTENDED RELEASE".encode()
besy = "BESYLATE; BENAZEPRIL".encode()
besy_edited = "BESYLATE/BENAZEPRIL".encode()
ac = "ACETAMINOPHEN; BUTALBITAL; CAFFEINE".encode()
ac_edited = "ACETAMINOPHEN/BUTALBITAL/CAFFEINE".encode()
ac_caf = "ACETAMINOPHEN; BUTALBITAL; CAFFEINE;".encode()
ac_caf_edited = "ACETAMINOPHEN/BUTALBITAL/CAFFEINE/".encode()
asp = "ASPIRIN; BUTALBITAL; CAFFEINE; CODEINE PHOSPHATE".encode()
asp_edited = "ASPIRIN/BUTALBITAL/CAFFEINE/CODEINE PHOSPHATE".encode()
cream_vaginal = "CREAM;TOPICAL, VAGINAL".encode()
cream_vaginal_edited = "CREAM;TOPICAL:VAGINAL".encode()
percent = "%;".encode()
percent_edited = "%/".encode()

#opening txt file and replacing strings
with open(file_name, "rb") as file:
    data = file.read()
    data = data.replace(inh_semicolon, inh_slash)
    data = data.replace(inh_zero, inh_dash_zero)
    data = data.replace(discn, "".encode())
    data = data.replace(metered_inhalation, metered_space)
    data = data.replace(amp, amp_edited)
    data = data.replace(dext, dext_edited)
    data = data.replace(mg_semicolon, "MG/".encode())
    data = data.replace(cap_ex, cap_ex_edited)
    data = data.replace(besy, besy_edited)
    data = data.replace(ac, ac_edited)
    data = data.replace(percent, percent_edited)
    data = data.replace(ac_caf, ac_caf_edited)
    data = data.replace(asp, asp_edited)
    data = data.replace(cream_vaginal, cream_vaginal_edited)
    data = data.replace(double_tilde, none)
    data = data.replace(tilde, comma_space)
    data = data.replace(semicolon, comma_space)



#creating a new file for the edited version
edited_file = "products_edited.txt"

#writing to the edited file
with open(edited_file, "wb") as file:
    file.write(data)

#converting to csv
read_file = pd.read_csv(edited_file)
read_file.to_csv("products.csv", index=None)