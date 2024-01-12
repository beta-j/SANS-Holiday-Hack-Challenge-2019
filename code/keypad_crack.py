##############################################################################
## SANS Holiday Hack Challenge 2019
##
## JAMES BALDACCHINO - 26-DEC-2019
##
## Frosty Keypad Challenge
## find 4 digit combinations that are prime using 1,3 and 7
## One of the digits is repeated once
##############################################################################

digits=set('137');  #these are the allowed digits based on the frost on the keypad
num=0;
x=0;

#Check if a given number is prime or not
def check_if_prime(candidate):
test=0
for x in range (2,candidate):
if (candidate % x)==0:
test= 1;
if test==1:
return 0;
if test==0:
return 1;


# Check whether a given number has repeated digits and how many times they are repeated
def repeated_digits(x):
count=0;
checkstring=str(x);
for el in digits:
count=checkstring.count(el);
if count>1:
return count;


for num in range(1137,7731):  #smallest possible number with available digits and constrains is 1137, largest is 7731
if check_if_prime(num)==1: #If the combination is prime..
if all((d in digits) for d in str(num)) and len(str(num))==4:   #and the combination is only composed of 1,3 and 7 and is 4 digits long...
if repeated_digits(num)<3:  #and has no digits repeated more than twice
x=x+1
print(x,".  ",num, "is a PRIME candidate");

num = num +1;
print("\n\nThere are ",x," possible valid combinations.");
