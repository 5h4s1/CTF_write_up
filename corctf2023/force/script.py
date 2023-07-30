import random
import string

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def generate_unique_strings(count, length):
    unique_strings = set()
    while len(unique_strings) < count:
        unique_strings.add(generate_random_string(length))
    return list(unique_strings)

# if __name__ == "__main__":
#     num_strings = 100000
#     string_length = 10
    
#     random_strings = generate_unique_strings(num_strings, string_length)
#     with open("string.txt", "w") as f:
#         f.write('\n'.join(random_strings[:100000]))
    # print(random_strings[:10000])  # In ra 10 chuỗi đầu tiên chỉ để xem thử

strings = generate_unique_strings(100000, 10)
payloads = ""
for i in range(80000,90000):
    payloads = payloads + strings[i] + ":flag(pin:" + str(i) + ")" + "\n"
with open("paylods.txt", "w") as f:
    f.write(payloads)
print(payloads)