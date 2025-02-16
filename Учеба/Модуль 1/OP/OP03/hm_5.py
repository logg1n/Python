user_inputs = []

for i in range(10):
    user_input = input(f"Введите символ или цифру ({i+1}/10): ")
    user_inputs.append(user_input)

print("Введенные символы или цифры:", user_inputs)
