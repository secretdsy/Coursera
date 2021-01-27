"""
This is a docstring for a merge function:
Return a new merged list.
"""
def merge(line):
    """
    This is a docstring for a merge function:
    Return a new merged list.
    """

    # empty list
    answer = []
    tmp_list = []
    
    # append not 0 in list 
    for dummy_i in range(len(line)):
        if line[dummy_i] != 0:
            tmp_list.append(line[dummy_i])
    
    # compare of the numbers
    if len(tmp_list) == 0:
        return line
    elif len(tmp_list) == 1:
        return tmp_list + [0 for dummy_i in range(len(line) - 1)]
    else:
        dummy_i = 0
        while(dummy_i < len(tmp_list) - 1):
            dummy_j = dummy_i + 1
            while(dummy_j < len(tmp_list)):
                if tmp_list[dummy_i] == tmp_list[dummy_j]:
                    answer.append(2 * tmp_list[dummy_i])
                    dummy_i += 2
                    break
                else:
                    answer.append(tmp_list[dummy_i])
                    dummy_i += 1
                    break
            if len(tmp_list) - dummy_i == 1:
                answer.append(tmp_list[-1])
    
    # add 0 elements to the list
    if len(answer) != len(line):
        answer += [0 for dummy_i in range(len(line) - len(answer))]
    
    return answer
