def next_bigger(num: int) -> int:
    """
        23988764410  <----
         ^     ^
         |     |
         |     +----- (pos) closer digit of digits[i]
         |
         (i) digits[i] < digits[i+1]
    """
    digits = list(str(num))
    i = len(digits)-2
    while i >= 0:
        if digits[i] < digits[i+1]:
            closer = min(d for d in digits[i+1:] if d > digits[i])
            pos = digits[i:].index(closer) + i
            digits[i], digits[pos] = digits[pos], digits[i]
            return int(''.join(digits[:i+1] + sorted(digits[i+1:])))
        i -= 1
    return -1


if __name__ == "__main__":
    res = next_bigger(23988764410)
    print(res)
