#from rich.pretty import pprint as PP
import PIL.ImageDraw
import turbocore
import trimesh
import numpy as np
import matplotlib.pyplot
from trimesh.path.entities import Line, Arc, Bezier
import matplotlib.image as mpimg
import qrcode
import math
import PIL
import PIL.Image
import PIL.ImageDraw


def main():
    turbocore.cli_this(__name__, 'cli_')


def imgfun():
    #import PIL
    #import PIL.Image
    #import PIL.ImageDraw
    width_px = 2100
    height_px = 2970
    _cm = float(2100.0/21.0)
    img = PIL.Image.new("RGB", (width_px, height_px), "white")
    draw = PIL.ImageDraw.Draw(img)
    draw.line([[10*_cm,10*_cm], [15*_cm,10*_cm]], fill="black", width=int(0.1*_cm))
    img.save("test.png", format="PNG")


def cli_xy(STLFILE, LAYOUT, Z, TITLE, SUBTITLE, RX, RY, BACKGROUND, PDF):
    filename = STLFILE
    mesh = trimesh.Trimesh()
    if STLFILE != "":
        mesh = trimesh.load(filename)


    angle_x = float(int(RX))*math.pi / 2  # 90 Grad in Radiant
    rotation_matrix_x = trimesh.transformations.rotation_matrix(
        angle=angle_x,
        direction=[1, 0, 0],  # Y-Achse
        point=[0, 0, 0]       # Rotationszentrum
    )

    angle_y = float(int(RY))*math.pi / 2  # 90 Grad in Radiant
    rotation_matrix_y = trimesh.transformations.rotation_matrix(
        angle=angle_y,
        direction=[0, 1, 0],  # Y-Achse
        point=[0, 0, 0]       # Rotationszentrum
    )

    if RX != "0":
        mesh.apply_transform(rotation_matrix_x)
    
    if RY != "0":
        mesh.apply_transform(rotation_matrix_y)

    width = 210
    height = 297
    width_inch = width / 25.4
    height_inch = height / 25.4

    fig, ax = matplotlib.pyplot.subplots(figsize=(width_inch, height_inch))
    ax = fig.add_axes([0, 0, 1, 1])

    min_xyz, max_xyz = mesh.bounds

    # center_slice = ((min_xyz + max_xyz) / 2)[:2]
    center_page = np.array([width/2, height/2])
    
    slices = []
    all_vertices_xy = []    
    
    #global_shift = center_page - center_slice

    for z in Z.split(","):
        plane_origin = [0,0,float(z)]
        plane_normal = [0,0,1]

        section = mesh.section(plane_origin=plane_origin,plane_normal=plane_normal)

        if section is not None:
            #slice_2d, to_3d = section.to_planar()

            path3d = section
            vertices_3d = path3d.vertices
            vertices_xy = vertices_3d[:, :2]

            slices.append((path3d, vertices_xy))
            all_vertices_xy.append(vertices_xy)

    all_vertices_xy = np.vstack(all_vertices_xy)
    min_xy_all = all_vertices_xy.min(axis=0)
    max_xy_all = all_vertices_xy.max(axis=0)
    center_all_slices = (min_xy_all + max_xy_all) / 2
            
    global_shift = np.zeros(2)
    if LAYOUT == "auto":
        global_shift = center_page - center_all_slices
    else:
        layout_cols_s = LAYOUT.split(",")
        l_mode = layout_cols_s[0]

        if l_mode == "o":
            # o,10,10 # origin x=10, y=10
            dx = float(layout_cols_s[1])
            dy = float(layout_cols_s[2])
            global_shift = np.array([dx, dy])

        if l_mode == "bb":
            # bb,20,30 # bounding box x=20, y=30
            dx = float(layout_cols_s[1])
            dy = float(layout_cols_s[2])
            global_shift = -min_xy_all + np.array([dx, dy])
            
    for path3d, vertices_xy in slices:
        path3d.apply_translation(np.append(global_shift, 0.0))
        discretized = path3d.discrete

        for segment in discretized:
            xs, ys = segment[:, 0], segment[:, 1]
            ax.plot(xs,ys,color="black", linewidth=0.9)
        
    major_ticks = np.arange(0, max(width, height), 10)
    minor_ticks = np.arange(0, max(width, height), 1)

    ax.set_xticks(major_ticks)
    ax.set_yticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(minor_ticks, minor=True)

    grid_alpha = 0
    alpha_x = 0;
    alpha_y = 0;

    if BACKGROUND == "mm":
        grid_alpha = 0.6
        alpha_x = 0.6;
        alpha_y = 0.6;

    ax.grid(which='minor', color='lightgrey', linewidth=0.3, alpha=grid_alpha)
    ax.grid(which='major', color='grey', linewidth=0.7, alpha=grid_alpha)

    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.invert_yaxis()  # damit oben = 0 ist, wie auf Papier üblich
    ax.set_aspect('equal')
    ax.tick_params(labelbottom=False, labelleft=False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    if TITLE != "":
        ax.text(15, 280-5, TITLE, fontweight="bold", fontfamily='monospace', fontsize=9, color="black",bbox=dict(facecolor="white", edgecolor="none", boxstyle="round,pad=0.3"))
    if SUBTITLE != "":
        ax.text(15, 285-5, SUBTITLE, fontfamily='monospace', fontsize=9, color="black",bbox=dict(facecolor="white", edgecolor="none", boxstyle="round,pad=0.3"))


    for x_ in range(1, 21):
        hori_down = 4
        ax.text(10*x_ + 0.8, 3+hori_down, "%d" % (x_*10), fontfamily='monospace', fontsize=5, color="black", alpha=alpha_x)
        if x_ > 0 and x_ < 20:
            ax.text(10*x_ + 0.8, 287-5+hori_down, "%d" % (x_*10), fontfamily='monospace', fontsize=5, color="black", alpha=alpha_x)
            ax.text(10*x_ + 0.8, 180+2+hori_down, "%d" % (x_*10), fontfamily='monospace', fontsize=5, color="black", alpha=alpha_x)
            ax.text(10*x_ + 0.8, 80+2+hori_down, "%d" % (x_*10), fontfamily='monospace', fontsize=5, color="black", alpha=alpha_x)

    for y_ in range(1, 30):
        ax.text(5+1, 10*y_ + 2, "%d" % (y_*10), fontfamily='monospace', fontsize=5, color="black", alpha=alpha_y, fontweight="bold")
        ax.text(210-4-5, 10*y_ + 2, "%d" % (y_*10), fontfamily='monospace', fontsize=5, color="black", alpha=alpha_y, fontweight="bold")

    #img = mpimg.imread("dein_bild.png")
    # Bild platzieren: extent = (x_min, x_max, y_min, y_max)
    #ax.imshow(img, extent=(x0, x1, y0, y1))

    # qr = qrcode.make("Test Daten")
    # qr_np = np.array(qr)
    # x0, x1 = 10, 50
    # y0, y1 = 250, 290  # Beachte deine invertierte Y-Achse!
    # ax.imshow(qr_np, extent=(x0, x1, y0, y1), cmap='gray', zorder=100)

    matplotlib.pyplot.savefig(PDF, format="pdf", pad_inches=0)
    matplotlib.pyplot.close()
    imgfun()