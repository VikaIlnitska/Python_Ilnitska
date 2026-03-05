numbers = [2, 3, 7, 2, 1, 0, 5, 2, 3, 1, 8, 4, 8]
A = 10
max_length = 0

print("Вихідні дані:")

for i in range(len(numbers)):
    current_sum = 0
    current_sub = []  
    
    for j in range(i, len(numbers)):
        current_sum = current_sum + numbers[j]
        current_sub.append(numbers[j]) 

        if current_sum == A:
            print(*current_sub, sep=", ")

            if len(current_sub) > max_length:
                max_length = len(current_sub)
                
        if current_sum > A:
            break

print("Максимальна кількість елементів:", max_length)