import sys

infilename = ""
outfilename = ""
is_st = False

def main():
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-in":
            i += 1
            infilename = sys.argv[i]
        elif sys.argv[i] == "-out":
            i += 1
            outfilename = sys.argv[i]
        elif sys.argv[i] == "-st":
            is_st = True

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

    if is_st:
        export_st(f, o)
    else:
        export_cx16(f, o)
        
    o.close()
    f.close()

def export_cx16(fp, op):
    ba = bytearray()
    ba.append(0)
    ba.append(0)

    while True:
        color = fp.read(3)
        if not color:
            break

        #print(f"r: {format(color[0], '08b')}")
        #print(f"g: {format(color[1], '08b')}")
        #print(f"b: {format(color[2], '08b')}")

        b = (int(color[2]) & 0xF0) >> 4
        g = (int(color[1]) & 0xF0)

        gb = g | b
        #print(f"gb: {format(gb, '08b')}")

        r = (int(color[0]) & 0xF0) << 4
        #print(f"r: {format(r, '08b')}")
        rgb = r | gb
        ba.append(rgb)
        ba.append(r)

    by = bytes(ba)
    op.write(by)

def export_st(fp, op):
    ba = bytearray()
    ci = 0

    while True:
        color = fp.read(3)
        if not color:
            break

        print(f"r: {format(color[0], '02x')}")
        print(f"g: {format(color[1], '02x')}")
        print(f"b: {format(color[2], '02x')}")

        b = ((int(color[2]) & 0xF) >> 1) & 0x7
        g = (((int(color[1]) & 0xF) >> 1) & 0x7) << 4

        gb = g | b
        #print(f"gb: {format(gb, '04x')}")
        #print("GB =", hex(gb))

        r = ((int(color[0]) & 0xF) >> 1) & 0x7
        print(f"r: {format(r, '04x')}")
        print("XR =", hex(r))
        rgb = (r << 8) | gb

        print("Color #",ci,f"rgb: {format(rgb, '04x')}")
        ci += 1

        ba.append(r)
        ba.append(gb)
        
    by = bytes(ba)
    op.write(by)
    
if __name__ == "__main__":
    main()
