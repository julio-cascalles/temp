class Solution:
    def singleNumber(self, arr: list) -> int:
        arr.sort()
        last = None
        while arr:
            item = arr.pop()
            if item != last and (not arr or item != arr[-1]):
                return item
            last = item
        return None


if __name__ == "__main__":
    res = Solution().singleNumber([1,2,2,3,2,1,1])
    print(res)
