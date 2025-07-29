import struct
import sys


stlfile = sys.argv[1]
ofile = sys.argv[2]
solid_name = "ModelX"


with open(ofile, 'w') as fo:
    with open(stlfile, 'rb') as f:
        r_header = f.read(80)
        r_facets = f.read(4)
        n_facets = int.from_bytes(r_facets, 'little', signed=False)
        fo.write("solid %s\n" % solid_name)
        for n_f in range(0, n_facets):
            print(n_f)
            norm_x = struct.unpack('f', f.read(4))[0]
            norm_y = struct.unpack('f', f.read(4))[0]
            norm_z = struct.unpack('f', f.read(4))[0]
            v1_x = struct.unpack('f', f.read(4))[0]
            v1_y = struct.unpack('f', f.read(4))[0]
            v1_z = struct.unpack('f', f.read(4))[0]
            v2_x = struct.unpack('f', f.read(4))[0]
            v2_y = struct.unpack('f', f.read(4))[0]
            v2_z = struct.unpack('f', f.read(4))[0]
            v3_x = struct.unpack('f', f.read(4))[0]
            v3_y = struct.unpack('f', f.read(4))[0]
            v3_z = struct.unpack('f', f.read(4))[0]
            abc_unused = f.read(2)

            #print("%f / %f / %f" % (norm_x, norm_y, norm_z))
            fo.write("  facet normal %f %f %f\n" % (norm_x, norm_y, norm_z))
            fo.write("    outer loop\n")
            fo.write("      vertex %f %f %f\n" % (v1_x, v1_y, v1_z))
            fo.write("      vertex %f %f %f\n" % (v2_x, v2_y, v2_z))
            fo.write("      vertex %f %f %f\n" % (v3_x, v3_y, v3_z))
            fo.write("    endloop\n")
            fo.write("  endfacet\n")

        fo.write("endsolid %s\n" % solid_name)
