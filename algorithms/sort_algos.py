


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n-i-1):
            if arr[j]>arr[j+1]:
                arr[i],arr[j+1] = arr[j+1],arr[i]
        
def selection_sort(arr):
    n = len(arr)
    max_element = arr[0]
    for i in range(n):
        max_element = max(arr[0:n-i-1])
        arr[i], arr[arr.index(max_element)] = arr[arr.index(max_element)], arr[i]
        
def insertion_sort(arr):
    n = len(arr)
    for i in range(1,n):
        key = arr[i]
        j = i-1
        while(arr[j]>key):
            arr[j+1] = arr[j]
            j-=1
        arr[j+1] = key            

def merge_sort(arr):
    pass

def quick_sort(arr):
    pass

def redix_sort(arr):
    pass

def bucket_sort(arr):
    pass

def heap_sort(arr):
    pass

def shell_sort(arr):
    pass

def tim_sort(arr):
    pass

def intro_sort(arr):
    pass

