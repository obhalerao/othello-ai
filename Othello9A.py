import sys

def flip(board, width):
    return "".join([board[i:(i+width)][::-1] for i in range(0, len(board), width)])

def rot(board, height, width):
    s1 = "".join([board[i::width][::-1] for i in range(0, width)])
    s2 = "".join([s1[i::height][::-1] for i in range(0, height)])
    s3 = "".join([s2[i::width][::-1] for i in range(0, width)])
    return [board, s1, s2, s3]


def main():
    s = ""
    width = 0
    if(len(sys.argv) > 2):
        s = sys.argv[1]
        width = int(sys.argv[2])
    else:
        s = sys.argv[1]
    if width == 0:
        for i in range(int(len(s) ** .5) if (len(s) ** .5).is_integer() else int(len(s) ** .5)+1, len(s)):
            if len(s) % i == 0:
                width = i
                break
    lss = rot(s, len(s)//width, width) + rot(flip(s, width), len(s)//width, width)
    for i in set(lss): print(i)


if __name__ == "__main__":
    main()