from random import random,seed,randint

def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    iter_no = 0
    while low <= high:
 
        mid = (high + low) // 2
        iter_no += 1
        # якщо x більше за значення посередині списку, ігноруємо ліву половину
        if arr[mid] < x:
            low = mid + 1
        
        # якщо x менше за значення посередині списку, ігноруємо праву половину
        elif arr[mid] > x:
            high = mid - 1
        # інакше x присутній на позиції і повертаємо його
        else:
            return iter_no, arr[mid]
    if low <= len(arr)-1:    
        return iter_no, arr[low]
    else:
        return iter_no, arr[high]
    

arr = []

for i in range(0, 12):
    arr.append(random() * 10)

arr = sorted(arr)
print("-"*40)
print("")
print("Generated sorted array:")
print (arr)
print("")
x = random() * 10
print("Generated search number: ", x)
result = binary_search(arr, x)
print(f"Result: {result[1]}; Number of iterations to find number: {result[0]}")
print("")
print("-"*40)

