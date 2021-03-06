from math import ceil, log2


class VEB:
    def high(self, x):
        return x >> (self.w // 2)

    def low(self, x):
        return x & (1 << (self.w // 2)) - 1

    def index(self, i, j):
        # return i*int(sqrt(self.u))+j
        return i << (self.w // 2) | j

    def __init__(self, u):
        self.w = ceil(log2(u))
        # self.u = 2 ** self.w
        self.min = self.max = None
        if self.w >= 1:
            self.cluster = [VEB(2 ** (self.w // 2)) for i in range(2 ** (self.w // 2))]
            self.summary = VEB(2 ** (self.w // 2))

    def member(self, x):
        if x == self.min or x == self.max:
            return True
        elif self.w == 1:
            return False
        else:
            c = self.high(x)
            i = self.low(x)
            return self.cluster[c].member(i)

    def insert(self, x):
        if self.min is None:
            self.min = x
            self.max = x
            return
        else:
            if x < self.min:
                x, self.min = self.min, x
            c = self.high(x)
            i = self.low(x)
            if self.w > 1:
                if self.cluster[c].min is None:
                    self.summary.insert(c)

                self.cluster[c].insert(i)
            if x > self.max:
                self.max = x

    def succesor(self, x):
        if self.w == 1:
            if x == 0 and self.max == 1:
                return 1
            else:
                return None
        elif self.min is not None and x < self.min:
            return self.min
        else:
            c = self.high(x)
            i = self.low(x)
            maxlow = self.cluster[c].max
            if maxlow is not None and i < maxlow:
                offset = self.cluster[c].succesor(i)
                return self.index(c, offset)
            else:
                succ_cluster = self.summary.succesor(self.high(x))
                if succ_cluster is None:
                    return None
                else:
                    offset = self.cluster[succ_cluster].min
                    return self.index(succ_cluster, offset)

    def predecessor(self, x):
        if self.w == 1:
            if x == 1 and self.min == 0:
                return 0
            else:
                return None
        elif self.max is not None and x > self.max:
            return self.max
        else:
            c = self.high(x)
            i = self.low(x)
            min_low = self.cluster[c].min
            if min_low is not None and i > min_low:
                offset = self.cluster[c].predecessor(i)
                return self.index(c, offset)
            else:
                prev_cluster = self.summary.predecessor(c)
                if prev_cluster is None:
                    if self.min is not None and x > self.min:
                        return self.min
                    else:
                        return None
                else:
                    offset = self.cluster[prev_cluster].max
                    return self.index(prev_cluster, offset)

    def delete(self, x):
        if x < self.min or x > self.max:
            return
        if self.min == self.max:
            self.min = self.max = None
        elif self.w == 1:
            if x == 0:
                self.min = 1
            else:
                self.min = 0
            self.max = self.min
        else:
            c = self.high(x)
            i = self.low(x)
            if x == self.min:
                first_cluster = self.summary.min
                x = self.index(first_cluster, self.cluster[first_cluster].min)
                self.min = x
            self.cluster[c].delete(i)
            if self.cluster[c].min is None:
                self.summary.delete(c)
                if x == self.max:
                    summary_max = self.summary.max
                    if summary_max is None:
                        self.max = self.min
                    else:
                        self.max = self.index(summary_max, self.cluster[summary_max].max)
            elif x == self.max:
                self.max = self.index(c, self.cluster[c].max)
