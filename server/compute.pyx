from math import exp

def compute(float complex_r, float complex_i, int iter):
    cdef float real = 0
    cdef float img = 0

    for i in range(1, iter+1):
        if (complex_r**2 + complex_i**2) > 4:
            break 
        else:
            real, img = iteration(real, img, complex_r, complex_i)

    return i 

def iteration(float prev_r, float prev_i, float complex_r, float complex_i):
    return ((prev_r**2 - prev_i**2) + complex_r, (2*prev_r*prev_i) + complex_i) # (real part, img part)