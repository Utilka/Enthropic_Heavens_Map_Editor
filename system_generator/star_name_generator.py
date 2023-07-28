import random

nm1 = [
    "a", "e", "i", "o", "u", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ]
nm2 = [
    "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z", "br",
    "cr", "dr", "gr", "kr", "pr", "sr", "tr", "str",
    "vr", "zr", "bl", "cl", "fl", "gl", "kl", "pl", "sl", "vl", "zl", "ch", "sh", "ph", "th", ]
nm3 = [
    "a", "e", "i", "o", "u", "a", "e", "i", "o", "u", "a", "e", "i", "o", "u", "ae",
    "ai", "ao", "au", "aa", "ea", "ei", "eo", "eu", "ee", "ia", "io", "iu", "oa", "oi", "oo", "ua", "ue", ]
nm4 = [
    "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z", "br",
    "cr", "dr", "gr", "kr", "pr", "sr", "tr", "str",
    "vr", "zr", "bl", "cl", "fl", "hl", "gl", "kl", "ml", "nl", "pl", "sl", "tl", "vl", "zl", "ch", "sh", "ph", "th",
    "bd", "cd", "gd", "kd", "ld", "md", "nd", "pd", "rd", "sd", "zd", "bs", "cs", "ds", "gs", "ks", "ls", "ms", "ns",
    "ps", "rs", "ts", "ct", "gt", "lt", "nt", "st", "rt", "zt", "bb", "cc", "dd", "gg", "kk", "ll", "mm", "nn", "pp",
    "rr", "ss", "tt", "zz", ]
nm5 = [
    "", "", "", "", "", "", "", "", "", "", "", "", "", "b",
    "c", "d", "f", "g", "h", "k", "l", "m", "n", "p", "r", "s", "t", "x", "y", "b", "c", "d", "f", "g", "h", "k", "l",
    "m", "n", "p", "r", "s", "t", "x", "y", "cs",
    "ks", "ls", "ms", "ns", "ps", "rs", "ts", "ys", "ct", "ft", "kt", "lt", "nt", "ph", "sh", "th", ]

def star_name_gen():
    name = ""
    if random.choice([True, False]):
        rnd = random.randint(0, len(nm1) - 1)
        rnd2 = random.randint(0, len(nm2) - 1)
        rnd3 = random.randint(0, len(nm3) - 1)
        rnd6 = random.randint(0, len(nm5) - 1)
        name = nm1[rnd] + nm2[rnd2] + nm3[rnd3] + nm5[rnd6]
    else:
        rnd = random.randint(0, len(nm1) - 1)
        rnd2 = random.randint(0, len(nm2) - 1)
        rnd3 = random.randint(0, len(nm3) - 1)
        rnd4 = random.randint(0, len(nm4) - 1)
        rnd5 = random.randint(0, len(nm3) - 1)

        if rnd3 > 14:
            while rnd5 > 14:
                rnd5 = random.randint(0, len(nm3) - 1)

        rnd6 = random.randint(0, len(nm5) - 1)
        name = nm1[rnd] + nm2[rnd2] + nm3[rnd3] + nm4[rnd4] + nm3[rnd5] + nm5[rnd6]
    name = name.capitalize()
    return name


if __name__ == "__main__":
    print(6*len(nm2)*len(nm3)*len(nm4)*(len(nm5)-12))
    for i in range(10):
        print(star_name_gen())
