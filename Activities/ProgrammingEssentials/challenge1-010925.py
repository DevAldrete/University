l1 = ("L", "M", "M", "J", "V")
l2 = ("S", "D")
l3 = (
    l1[: l1.index("M") + 1]
    + tuple(l1[l1.index("M") + 1].replace("M", "X"))
    + l1[l1.index("M") + 2 :]
    + l2
)
print(l3)
