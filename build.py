#!/usr/bin/env python3

import sass
import shutil, os
from diff_match_patch import diff_match_patch

BUILD_PATH = "./_build"
THEMESRC_PATH = f"{BUILD_PATH}/themesrc"
OUT_PATH = f"{BUILD_PATH}/theme"
OUT_GNOME_PATH = f"{OUT_PATH}/gnome-shell"
CSS_PATH = f"{OUT_GNOME_PATH}/gnome-shell.css"

def mk_patch(file: str):
    dmp = diff_match_patch()
    with open(f"./gnome-shell/data/theme/gnome-shell-sass/_{file}.scss", "r") as old:
        with open(f"./{file}.scss", "r") as new:
            old = old.read()
            new = new.read()
            patches = dmp.patch_make(old, new)
            diff = dmp.patch_toText(patches)
            with open("{file}.scss.patch", "w") as p:
                p.write(diff)
def mk_all_patches():
    mk_patch("colors")
    mk_patch("default-colors")

def clean():
    try:
        shutil.rmtree(f"{BUILD_PATH}")
    except:
        pass

def mk_theme_dir():
    print("Creating output build directory...")
    clean()
    src_path = "./gnome-shell/data/theme/"
    shutil.copytree(src_path, THEMESRC_PATH)
    os.mkdir(f"{OUT_PATH}")
    os.mkdir(f"{OUT_GNOME_PATH}")

def apply_patch(file: str):
    print(f"Patching {file}.scss...")
    dmp = diff_match_patch()
    colors_path = f"{THEMESRC_PATH}/gnome-shell-sass/_{file}.scss"
    colors_patch = f"./{file}.scss.patch"
    with open(colors_patch, "r") as p:
        p = p.read()
        patches = dmp.patch_fromText(p)
        with open(colors_path, "r") as cols:
            cols_t = cols.read()
            cols_t, _ = dmp.patch_apply(patches, cols_t)
        with open(colors_path, "w") as cols:
            cols.write(cols_t)

def edit_palette():
    print("Setting custom palette...")
    palette_path = f"{THEMESRC_PATH}/gnome-shell-sass/_palette.scss"
    palette_src = f"./palette.scss";
    shutil.copy(palette_src, palette_path)
    apply_patch("default-colors")
    apply_patch("colors")


def compile():
    css = sass.compile(filename=f"{THEMESRC_PATH}/gnome-shell-dark.scss")
    with open(CSS_PATH, "w") as output_css:
        output_css.write(css)

def build():
    print("Building CSS and finalizing theme build...")
    compile()
    shutil.copy("./index.theme", f"{OUT_PATH}/index.theme")


def main():
    mk_theme_dir()
    edit_palette()
    build()
    print("All done!")

if __name__ == "__main__":
    main()
