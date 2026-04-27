
# Import itertools to make all possible character combinations
import itertools

# Define sets of characters for each category
capital_letters = ['A', 'B', 'C', 'D', 'E']
lowercase_letters = ['a', 'b', 'c', 'd', 'e']
digits = ['1', '2', '3', '4', '5']
specials = ['$', '&', '%']

# Combine all the characters into one list
all_chars = capital_letters + lowercase_letters + digits + specials

# Ask user to enter how long the password should be
length = int(input("Enter the password length (try 4, 5 or 6): "))

# Make all possible combinations for that length (streaming, not saving all in memory)
combinations = itertools.product(all_chars, repeat=length)

# Make an empty list to keep the good passwords
valid_passwords = []

# Check every possible password
for combo in combinations:
    password = ''.join(combo)  # Join characters into a string

    # It must start with a letter (A-Z or a-z)
    if not password[0].isalpha():
        continue  # skip this one if not starting with letter

    # Check if it has at least one capital letter
    if not any(c in password for c in capital_letters):
        continue

    # Check if it has at least one lowercase letter
    if not any(c in password for c in lowercase_letters):
        continue

    # Check if it has at least one digit
    if not any(c in password for c in digits):
        continue

    # Check if it has at least one special symbol
    if not any(c in password for c in specials):
        continue

    # No more than 2 capital letters allowed
    if sum(1 for c in password if c in capital_letters) > 2:
        continue

    # No more than 2 special symbols allowed
    if sum(1 for c in password if c in specials) > 2:
        continue

    # If all checks are OK, add this password to the list
    valid_passwords.append(password)

# Save the valid passwords in a file
with open("valid_passwords.txt", "w") as file:
    for i, password in enumerate(valid_passwords, 1):
        file.write(f"{i} {password}\n")

# Print how many good passwords we found
print(f"Total valid passwords: {len(valid_passwords)}")
print("All saved to valid_passwords.txt")
