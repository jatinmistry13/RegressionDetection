# Enter your code here. Read input from STDIN. Print output to STDOUT
import json
import math
import scipy.stats.stats as st

'''
def plotHisto(data):
    """plot the histogram data to visualize"""
    
    plt.hist(data)
    plt.title("Gaussian Histogram")
    plt.xlabel("year")
    plt.ylabel("Frequency")
    plt.show()
'''


def compute_rmse(arr):
    """computes rmse (root mean square error)"""

    # compute mean
    mean = sum(arr) / len(arr)
    sse = 0

    # loop through the list
    for i in arr:

        # compute sse as (val - mean)^2
        sse += (i - mean) ** 2

    # compute rmse and return
    rmse = math.sqrt(sse) / len(arr)
    return rmse


def compute_stddev(arr):
    """computes standard deviation"""

    # compute mean
    mean = sum(arr) / len(arr)
    sse = 0

    # loop through the list
    for i in arr:

        # compute sse as (val - mean)^2
        sse += (i - mean) ** 2

    # compute std deviation and return
    stddev = math.sqrt(sse / len(arr))
    return stddev


def compute_2stddev(arr):
    """compute two standard deviation"""

    # compute mean
    mean = sum(arr) / len(arr)
    sse = 0

    # loop through the list
    for i in arr:

        # compute sse as (val - mean)^2
        sse += (i - mean) ** 2

    # compute two std deviation and return
    stddev = math.sqrt(sse / len(arr))
    two_stddev = mean + -2 * stddev
    return two_stddev


def check_regression(rmse_lst, stddev, skewnessList, skewness_stddev, date_lst):
    """check for regression and if found return the date else return empty string"""

    # initialize max value as lists first value
    maxVal = rmse_lst[0]

    # initialize regression date as empty string.
    # If regression no regression return empty string else return regression
    # date
    reg_date = ""

    # loop through rmse list
    for i in range(0, len(rmse_lst) - 1):

        # calculate absolute difference
        val = abs(rmse_lst[i] - rmse_lst[i + 1])

        # calculate absolute skewness difference
        skewVal = abs(skewnessList[i] - skewnessList[i + 1])

        # conditions check for finding regression
        if (val > stddev) and (i > 1) and (skewVal > skewness_stddev):
            reg_date = date_lst[i + 1]
            return reg_date
    return reg_date


def main():
    """main function"""

    json_string = raw_input()
    #json_string = data1

    # load json data
    parsed_json = json.loads(json_string)

    # histogram record length
    rec_len = len(parsed_json[0]['histogram'])

    # variables declaration
    date_lst = []
    rmse_lst = []
    skewnessList = []

    # loop through the record
    for record in parsed_json:
        # extract date part
        date = record['date']

        # extract histogram data part
        histogram = record['histogram']

        # compute rmse (root mean squared error for the histogram)
        rmse = compute_rmse(histogram)

        # add the computed rmse to a list. This gives us a date-wise rmse
        # values for histogram
        rmse_lst.append(rmse)

        # add date to a date list
        date_lst.append(date)

        # compute skewness of the histogram.
        # Skewness is the measure of symmetry.
        # If there is a spurious rise in the skewness value that means there is a
        # clear deviation of the distributionon a certain day from how it
        # appeared in the previous one
        skewnessList.append(st.skew(histogram))

    # compute standard deviation for the rmse list
    stddev = compute_stddev(rmse_lst)

    # compute two standard deviation of skewness list
    skew_2stdDev = compute_2stddev(skewnessList)

    # check for regression
    regression_date = check_regression(
        rmse_lst, stddev, skewnessList, skew_2stdDev, date_lst)

    # print the regression date. If regression is found then print the date
    # else print an empty string
    print regression_date

if __name__ == "__main__":
    main()
