user_input = input("Your Text: ")
input_no_space = user_input.replace("+", ";").replace("-", ";").replace(" ", "")
number_list = input_no_space.split(";")
size = len(number_list)
broken_text_list = []


for i in user_input:
    broken_text_list.append(i)

res = int(number_list[0])
k = 1
for i in broken_text_list:
    if i == "+":
        res += int(number_list[k])
        k += 1
    if i == '-':
        res -= int(number_list[k])
        k += 1

print(res)