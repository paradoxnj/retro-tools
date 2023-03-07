import sys

MODE_1BPP = 1
MODE_2BPP = 2
MODE_4BPP = 4
MODE_8BPP = 8
MODE_STBP = 16

infilename = ""
outfilename = ""
mode = MODE_8BPP

def main():
    st = False

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-in":
            i += 1
            infilename = sys.argv[i]
        elif sys.argv[i] == "-out":
            i += 1
            outfilename = sys.argv[i]
        elif sys.argv[i] == "-mode":
            i += 1
            mode = sys.argv[i]
        elif sys.argv[i] == "-st":
            mode = MODE_STBP

    u = infilename.upper()
    infilename = u

    u = outfilename.upper()
    outfilename = u

    print("Input File Name: " + infilename)
    print("Output File Name: " + outfilename)

    print("Opening input file: " + infilename)
    try:
        f = open(infilename, "rb")
    except:
        print("ERROR:  Could not open input file " + infilename)
        return

    print("Opening output file: " + outfilename)
    try:
        o = open(outfilename, "wb")
    except:
        print("ERROR:  Could not open output file" + outfilename)
        close(f)
        return

    if int(mode) == MODE_4BPP:
        print("Writing in 4BPP mode")
        write_4bpp(f, o)
    elif int(mode) == MODE_8BPP:
        print("Writing in 8BPP mode")
        write_8bpp(f, o)
    elif int(mode) == MODE_1BPP:
        print("Writing in 1BPP mode")
        write_1bpp(f, o)
    elif int(mode) == MODE_2BPP:
        print("Writing in 2BPP mode")
        write_2bpp(f, o, st)
    elif int(mode) == MODE_STBP:
        print("Writing Atari ST Bitplane Format")
        write_st(f, o)

    
    o.close()
    f.close()

def write_1bpp(inf, outf):
    b = bytearray()
    b.append(0)
    b.append(0)

    while True:
        i = inf.read(8)
        if not i:
            break

        o = (int(i[0]) & 0x1)  << 7
        o |= (int(i[1]) & 0x1) << 6
        o |= (int(i[2]) & 0x1) << 5
        o |= (int(i[3]) & 0x1) << 4
        o |= (int(i[4]) & 0x1) << 3
        o |= (int(i[5]) & 0x1) << 2
        o |= (int(i[6]) & 0x1) << 1
        o |= (int(i[7]) & 0x1)
        b.append(o)

    ba = bytes(b)
    outf.write(ba)

def write_2bpp(inf, outf):
    b = bytearray()
    b.append(0)
    b.append(0)
    
    while True:
        i = inf.read(4)
        if not i:
            break

        o = int(i[0] & 0x1)  << 6
        o |= int(i[1] & 0x1) << 4
        o |= int(i[2] & 0x1) << 2
        o |= int(i[3] & 0x1)
        b.append(o)

    ba = bytes(b)
    outf.write(ba)

def write_4bpp(inf, outf):
    b = bytearray()
    b.append(0)
    b.append(0)
    
    while True:
        i = inf.read(2)
        if not i:
            break

        o = (int(i[0]) & 0xF) << 4
        o |= (int(i[1]) & 0xF)
        b.append(o)

    ba = bytes(b)
    outf.write(ba)

def write_8bpp(inf, outf):
    b = bytearray()
    b.append(0)
    b.append(0)
    
    while True:
        i = inf.read(2)
        if not i:
            break

        b.append(int(i[0]))
        b.append(int(i[1]))

    ba = bytes(b)
    outf.write(ba)

def write_st(inf, outf):
    b = bytearray()
    
    while True:
        i = inf.read(8)
        if not i:
            break

        n = 7
        bp1 = 0
        bp2 = 0
        bp3 = 0
        bp4 = 0

        for x in range(0, len(i)):
            ival = int(i[x])
            bp4 |= (ival & 0x1) << n
            bp3 |= ((ival & 0x2) >> 1) << n
            bp2 |= ((ival & 0x4) >> 2) << n
            bp1 |= ((ival & 0x8) >> 3) << n
            n -= 1
            print(f"bitplane 1: {format(bp1, '08b')}")
            print(f"bitplane 2: {format(bp2, '08b')}")
            print(f"bitplane 3: {format(bp3, '08b')}")
            print(f"bitplane 4: {format(bp4, '08b')}")
            print("")

        b.append(bp1)
        b.append(bp2)
        b.append(bp3)
        b.append(bp4)

    
    ba = bytes(b)
    outf.write(ba)

if __name__ == "__main__":
    main()
