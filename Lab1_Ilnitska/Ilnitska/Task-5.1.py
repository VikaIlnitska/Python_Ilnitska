import math

a = int(input("Введіть перше число (a): "))
b = int(input("Введіть друге число (b): "))

start = min(a, b)
end = max(a, b)

print(f"\nПрості числа в діапазоні від {start} до {end}:")

for num in range(start, end + 1):
    if num > 1:
        is_prime = True
    
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False  
                break        

        if is_prime:
            print(num, end=" ")
            
print()