import sort_main
from themes.colors import *
MIN_MERGE = 32

def calculate_min_run(n): 
    """Returns the minimum length of a 
    run from 23 - 64 so that 
    the len(array)/minrun is less than or 
    equal to a power of 2.  
    """
    r = 0
    while n >= MIN_MERGE: 
        r |= n & 1
        n >>= 1
    return n + r 

# TODO: Add Descending functionality 
# def counting_sort(draw_info,arr, low, high, ascending=True):
#     max_val = max(arr)
#     freq_arr = [0] * (max_val+1)
#     for num in arr:
#         freq_arr[num] += 1
#     for i in range(1, max_val + 1):
#         freq_arr[i] += freq_arr[i - 1]
#     output_array = [0] * len(arr)

#     for i in range(len(arr) - 1, -1, -1):
#         output_array[freq_arr[arr[i]] - 1] = arr[i]
#         freq_arr[arr[i]] -= 1
#     for i in range(len(arr)):
#         arr[i] = output_array[i]
#         sort_main.draw_list(draw_info, {i: 'green'}, clear_bg=True)
#         yield True
#     return output_array



# def bucket_sort(draw_info,lst,low,high, ascending=True):
#     arr = []
#     slot_num = 10
#     for i in range(slot_num):
#         arr.append([])
#     for j in lst:
#         index_b = int(slot_num * j)
#         arr[index_b].append(j)
#     for i in range(slot_num):
#         arr[i] = sorted(arr[i])
#     k = 0
#     for i in range(slot_num):
#         for j, item in enumerate(arr[i]):
#             lst[k] = item
#             k += 1
#             sort_main.draw_list(draw_info, {k: GREEN}, True)
#             yield True
            
def radix_count_sort(draw_info,arr,place,ascending=True):
    n = len(arr) 
    output_arr = [0] * (n) 
    count = [0] * (10) 
   
    for i in range(0, n): 
        index = (arr[i]/place) 
        count[int((index)%10)] += 1
   
    for i in range(1,10): 
        count[i] += count[i-1] 
   
    i = n-1
    while i>=0: 
        index = (arr[i]/place) 
        output_arr[ count[ int((index)%10) ] - 1] = arr[i] 
        count[int((index)%10)] -= 1
        i -= 1
   
    i = 0
    for i in range(0,len(arr)): 
        arr[i] = output_arr[i]
        sort_main.draw_list(draw_info, {i: 'green'}, clear_bg=True)
        yield True 
 
def radix_sort(draw_info,arr, low, high, ascending=True):
    max_ele = max(arr)
    place = 1
    while max_ele // place > 0:
        yield from radix_count_sort(draw_info,arr,place,ascending)
        place *= 10            
           
            
#* To Check
def bucket_sort(draw_info, lst, low, high, ascending=True):
    arr = []
    slot_num = 10
    for i in range(slot_num):
        arr.append([])
    for j in lst:
        index_b = int(slot_num * j)
        arr[index_b].append(j)
    for i in range(slot_num):
        arr[i] = sorted(arr[i], reverse=not ascending)
    k = 0
    for i in range(slot_num):
        for j, item in enumerate(arr[i]):
            lst[k] = item
            k += 1
            sort_main.draw_list(draw_info, {k: GREEN}, True)
            yield True
            
def counting_sort(draw_info, arr, low, high, ascending=True):
    max_val = max(arr)
    freq_arr = [0] * (max_val+1)
    for num in arr:
        freq_arr[num] += 1
    for i in range(1, max_val + 1):
        freq_arr[i] += freq_arr[i - 1]
    output_array = [0] * len(arr)

    if ascending:
        for i in range(len(arr) - 1, -1, -1):
            output_array[freq_arr[arr[i]] - 1] = arr[i]
            freq_arr[arr[i]] -= 1
    else:
        for i in range(len(arr)):
            output_array[i] = freq_arr[arr[i]]
            freq_arr[arr[i]] -= 1

    for i in range(len(arr)):
        arr[i] = output_array[i]
        sort_main.draw_list(draw_info, {i: 'green'}, clear_bg=True)
        yield True

    return output_array

# def radix_count_sort(draw_info, arr, place, ascending=True):
#     n = len(arr)
#     output_arr = [0] * n
#     count = [0] * 10

#     for i in range(n):
#         index = arr[i] / place
#         count[int(index % 10)] += 1

#     for i in range(1, 10):
#         count[i] += count[i - 1]

#     if ascending:
#         i = n - 1
#         while i >= 0:
#             index = arr[i] / place
#             output_arr[count[int(index % 10)] - 1] = arr[i]
#             count[int(index % 10)] -= 1
#             i -= 1
#     else:
#         i = 0
#         while i < n:
#             index = arr[i] / place
#             output_arr[n - count[int(index % 10)]] = arr[i]
#             count[int(index % 10)] -= 1
#             i += 1

#     for i in range(n):
#         arr[i] = output_arr[i]
#         sort_main.draw_list(draw_info, {i: 'green'}, clear_bg=True)
#         yield True

# def radix_sort(draw_info, arr, low, high, ascending=True):
#     max_ele = max(arr)
#     place = 1
#     while max_ele // place > 0:
#         yield from radix_count_sort(draw_info, arr, place, ascending)
#         place *= 10
        
#* Below works fine
def bubble_sort(draw_info,arr,low,high,ascending=True):
    for i in range(high):
        for j in range(high-i-1):
            if (arr[j]>arr[j+1] and ascending) or (arr[j]<arr[j+1] and not ascending):
                arr[j],arr[j+1] = arr[j+1],arr[j]
                sort_main.draw_list(draw_info,{j:GREEN,j+1:RED},clear_bg=True)
                yield True
    return arr
        
def selection_sort(draw_info, arr, low, high, ascending=True):
    for i in range(low, high):
        min_idx = i
        for j in range(i + 1, high):
            if (arr[j] < arr[min_idx] and ascending) or (arr[j] > arr[min_idx] and not ascending) :
                min_idx = j
                sort_main.draw_list(draw_info, {i: 'green', min_idx: 'red'}, clear_bg=True)
                yield True
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        sort_main.draw_list(draw_info, {i: 'green', min_idx: 'red'}, clear_bg=True)
        yield True
    return arr

def insertion_sort(draw_info,arr,low,high,ascending=True):
    for i in range(low, high):
        key = arr[i]
        j = i - 1
        if ascending:            
            while j >= low and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                sort_main.draw_list(draw_info, {j: 'green', j + 1: 'red'}, clear_bg=True)
                yield True
            arr[j + 1] = key
            sort_main.draw_list(draw_info, {j + 1: 'blue'}, clear_bg=True)
            yield True
        else:
            while j >= low and arr[j] < key:
                arr[j + 1] = arr[j]
                j -= 1
                sort_main.draw_list(draw_info, {j: 'green', j + 1: 'red'}, clear_bg=True)
                yield True
            arr[j + 1] = key
            sort_main.draw_list(draw_info, {j + 1: 'blue'}, clear_bg=True)
            yield True    
    return arr

def merge_sort(draw_info, lst,low,high, ascending=True):

	def merge(lst, l, m, r):
		n1 = m - l + 1
		n2 = r - m

		L = [0] * (n1)
		R = [0] * (n2)

		for i in range(0, n1):
			L[i] = lst[l + i]

		for j in range(0, n2):
			R[j] = lst[m + 1 + j]

		i = 0
		j = 0
		k = l

		while i < n1 and j < n2:
			if (L[i] <= R[j] and ascending) or (L[i] >= R[j] and not ascending):
				lst[k] = L[i]
				i += 1
			else:
				lst[k] = R[j]
				j += 1
			k += 1
			sort_main.draw_list(draw_info, {k: GREEN}, True)
			yield True

		while i < n1:
			lst[k] = L[i]
			i += 1
			k += 1
			sort_main.draw_list(draw_info, {k: GREEN}, True)
			yield True

		while j < n2:
			lst[k] = R[j]
			j += 1
			k += 1
			sort_main.draw_list(draw_info, {k: GREEN}, True)
			yield True
			return lst

	def merge_sort(lst, l, r, ascending=True):
		if l < r:
			m = (l + (r - 1)) // 2

			yield from merge_sort(lst, l, m, ascending)
			yield from merge_sort(lst, m + 1, r, ascending)
			yield from merge(lst, l, m, r)

	yield from merge_sort(lst, 0, len(lst) - 1, ascending)
	return lst

def quick_sort(draw_info,lst,low,high, ascending=True):
	def partition(lst, low, high, ascending=True):
		i = (low - 1)
		pivot = lst[high]

		for j in range(low, high):
			if (lst[j] < pivot and ascending) or (lst[j] > pivot and not ascending):
				i = i + 1
				lst[i], lst[j] = lst[j], lst[i]
				sort_main.draw_list(draw_info, {i: GREEN, j: RED}, True)
				yield True

		lst[i + 1], lst[high] = lst[high], lst[i + 1]
		sort_main.draw_list(draw_info, {i + 1: GREEN, high: RED}, True)
		yield True
		return (i + 1)

	def quick_sort(lst, low, high, ascending=True):
		if low < high:
			pi = yield from partition(lst, low, high, ascending)
			yield from quick_sort(lst, low, pi - 1, ascending)
			yield from quick_sort(lst, pi + 1, high, ascending)

	yield from quick_sort(lst, 0, len(lst) - 1, ascending)
	return lst
             
def merge(draw_info,arr, l, m, r,ascending): 
    len1 = m - l + 1
    len2 = r - m
    
    left, right = [], [] 
    
    for i in range(0, len1): 
        left.append(arr[l + i])

    for i in range(0, len2):
        right.append(arr[m+i+1])
    
    
    i, j, k = 0, 0, l

    while i < len1 and j < len2: 
        if ascending:
            if left[i] <= right[j]: 
                arr[k] = left[i] 
                i += 1

            else: 
                arr[k] = right[j] 
                j += 1

        else:
            if left[i] >= right[j]: 
                arr[k] = left[i] 
                i += 1

            else: 
                arr[k] = right[j] 
                j += 1

        sort_main.draw_list(draw_info, {k: 'green'}, clear_bg=True)
        yield True
        k += 1
               
    while i < len1: 
        arr[k] = left[i] 
        k += 1
        i += 1
        sort_main.draw_list(draw_info, {}, clear_bg=True)
        yield True
        
    while j < len2: 
        arr[k] = right[j] 
        k += 1
        j += 1
        sort_main.draw_list(draw_info, {}, clear_bg=True)
        yield True
             
def tim_sort(draw_info,arr, low, high, ascending=True):
    min_run = calculate_min_run(high)
    for i in range(low, high, min_run):
        end = min((i + min_run - 1), high - 1)
        yield from insertion_sort(draw_info,arr, i, end+1,ascending)

    size = min_run

    while size < high:
        for left in range(low, high, 2 * size):
            mid = min((left + size - 1), (high - 1))
            right = min((left + 2 * size - 1), (high - 1))
            if mid < right:
                yield from merge(draw_info, arr, left, mid, right,ascending)
        size = 2 * size
