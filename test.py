arr=[2,3,5,4,7,8,2,2,8]
def remove_duplicates(arr):
    return list(set(arr))

print('remove duplicates',remove_duplicates(arr))