def update_vector_clock(own_clock, incoming_clock, process_number):
    if len(own_clock) != len(incoming_clock):
        raise Exception('Vector clock lengths do not match!')
    
    # each process gets the bigger value of the two, and increment this process's value by 1
    result_clock = [max(own_clock[i], incoming_clock[i]) for i in range(len(own_clock))]
    result_clock[process_number] += 1
    return result_clock
    