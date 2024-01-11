'''
Given an input n representing number of buckets, wish to map via a function, f
the FICO scores to the set of integers 1 through n,
Then map this set of integers, via a function p, to a probability of default, such that
the summation of square errors between p(f(s)) and the actual default value over all data points is minimised.

 Once a bucket has been established, ie. choices made for f, is the probability function is k/n
 - this is easy to show with calculus.
 '''

import math
import pandas as pd


def main(num_buckets):
    # Stuff to open and process the data
    df = pd.read_csv("Loan_Data.csv")
    print(df)
    df = df.sort_values(by=["fico_score"], ignore_index=True)
    print(df)

    # Compute k and n values for [300, s) for s up to 851
    k = 0
    n = 0
    i = 0
    max_i = df.shape[0] - 1
    print(max_i)
    vals_kn = {}
    print(df["fico_score"][0])
    for s in range(300, 852):
        if i > max_i:
            vals_kn.update({s: [k, n]})
            continue
        while df["fico_score"][i] == s:
            n += 1
            if df["default"][i] == 1:
                k += 1
            i += 1
            if i > max_i:
                break
        vals_kn.update({s: [k, n]})

    ''' 
    Set up memo for storing results of err_func(a, b, m) which will record the error contribution of m buckets
    over the range [a, b), and the location and ratio of the split that optimises it
    Note that optimsing err_func(300, 851, n) will give the solution
    '''
    results = {}

    # Function to compute the error contribution for a bucket consisting of fico scores between a (inc) and b (exc)
    def error_con(a, b):
        k = vals_kn[b][0] - vals_kn[a][0]
        n = vals_kn[b][1] - vals_kn[a][1]

        # if there is no variation there is no error
        if n == 0 or k == 0 or k == n:
            return 0

        return -k * math.log(k / n) - (n - k) * math.log(1 - k / n)

    # Compute error contribute for each single bucket [a, b) storing as err_func(a, b, 1)
    for b in range(300, 852):
        for a in range(300, b):
            error = error_con(a, b)
            results.update({(a, b, 1): [error, b]})

    # Recursion on m to find optimal buckets, storing in memo as required
    def dp(a, b, m):
        if (a, b, m) in results:
            return results[(a, b, m)][0]
        if a == b:
            results.update({(a, b, m): [0]})
            return 0
        split_record = [results[(a, b, 1)][0], a, 0]
        for c in range(a, b):
            for num_buckets_split in range(1, m):
                temp = dp(a, c, num_buckets_split) + dp(c, b, m - num_buckets_split)
                if temp < split_record[0]:
                    split_record = [temp, c, num_buckets_split]
        print(a, b, m, split_record)
        results.update({(a, b, m): split_record})
        return results[(a, b, m)][0]

    dp(300, 850, num_buckets)

    # Use stored results to work back and find boundaries, storing in the array
    def retrieve_boundaries(a, b, m, l):
        if m == 1:
            boundaries[l] = b
            return
        retrieve_boundaries(a, results[(a, b, m)][1], results[(a, b, m)][2], l)
        retrieve_boundaries(results[(a, b, m)][1], b, m - results[(a, b, m)][2], l + results[(a, b, m)][2])
        return

    for h in range(2, num_buckets + 1):
        # Set up list to store the boundaries
        boundaries = [0] * (h + 1)
        boundaries[h] = 851
        retrieve_boundaries(300, 850, h, 1)
        print(boundaries)

main(5)



