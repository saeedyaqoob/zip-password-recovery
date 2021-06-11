# import statements
from zipfile import ZipFile
from tqdm import tqdm
from itertools import permutations
import os


# Function to create a permuted list/file of password based on the words frequently used by you
# word_set -> Frequently/known used words by you
# length -> Combination length e.g. 123abc -> length=2, 123abcXYZ -> length=3, etc.
def create_password_list(word_set, length):

    filename = 'password.txt'

    try:
        # Remove any existing password.txt file
        os.remove(filename)

    except:
        pass

    # Password_list creation
    for i in range(1, length+1):

        # Using Itertools to permute over a word set and a combination length
        permutation_list = permutations(word_set, i)

        temp_word = []

        for value in permutation_list:
            for item in value:
                temp_word.append(item)

            temp_word = ''.join(temp_word)

            # Write the password to the password.txt file
            with open(filename, 'a') as f:
                f.write(temp_word + '\n')

            temp_word = []

    return filename


# Frequently/known used words by you
word_list = ['123', '456', '789', 'abc', 'ABC', 'xyz', 'XYZ']

# Combination length e.g. 123abc -> length=2, 123abcXYZ -> length=3, etc.
combination_length = 6

# Create the password.txt file
password_list = create_password_list(word_list, combination_length)

# Import the password protected zip file as a python ZipFile
# Change the filename as per the name of your zip file
zip_file = ZipFile('filename.zip')

# No. of passwords in the password.txt file
no_of_passwords = len(list(open(password_list, 'rb')))
print('Total no. of passwords to test: ', no_of_passwords)

# Brute force the passwords from the password.txt read as binaryIO on the zip file
with open(password_list, "rb") as wordlist:

    # Use tqdm module to display a status bar for percentage of passwords tried on the protected zip file
    for word in tqdm(wordlist, total=no_of_passwords, unit='word'):

        try:
            # Use the selected password to try to extract all the files in the zip
            # zip_file.extractall(pwd=word.strip(), path='./extracted')

            # Use the selected password to try to extract the first file in the zip, then remove the file
            zip_file.extract(member=zip_file.namelist()[0], pwd=word.strip())
            os.remove(str(zip_file.namelist()[0]))

        except:
            continue

        else:
            print('Password found: ', word.decode().strip())
            # Exit the program once the password is found
            exit(0)

print('Password not found, try another wordlist. ')
