def size(arr):
    count = 0
    for x in range(len(arr)):
        if type(arr[x]) != int and len(arr[x]) > 0:
            count += len(arr[x])
        else:
            count += 1
    return count


a = [1, '2', 3]
b = [[1, 2], [3, 4]]
c = [[1, 2], [3, 4], [5, [6, 7]]]
print(size(a))
print(size(b))
print(size(c))
