
# heatmap
# m is width, n is height
# m = 19
# n = 25
m = 8
n = 11


def caculate_Y():
    for index in range(n):
        j = index + 1
        ret = (2 * j - (n + 1)) / float(n)
        print "Y:"+str(ret)

def caculate_X():
    for index in range(m):
        i = index + 1
        ret = (2 * i - (m + 1)) / float(m)
        print "X:"+str(ret)


if __name__ == "__main__":
    caculate_X()
    caculate_Y()
