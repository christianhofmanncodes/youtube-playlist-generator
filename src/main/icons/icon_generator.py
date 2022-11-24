"""module icon_generator"""

import os
import sys

from PIL import Image

BASE_ICON_SIZES = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64)]
LINUX_ICON_SIZES = [(128, 128), (256, 256), (512, 512), (1024, 1024)]
MAC_ICON_SIZES = [(128, 128), (256, 256), (512, 512), (1024, 1024)]


def create_base_icons(image) -> None:
    """
    The create_base_icons function creates base icon sizes in src/main/icons/base.

    :param image: Used to Get the image that is used to create the icons.
    :return: None.
    """
    for size in BASE_ICON_SIZES:
        file_name = os.path.join(
            os.path.abspath(os.path.dirname(sys.argv[0])), "base", f"{str(size[0])}.png"
        )

        new_image = image.resize(size)
        new_image.save(file_name)
        print(f"Icon created: {file_name}")


def create_linux_icons(image) -> None:
    """
    The create_linux_icons function creates a set of icons for Linux.
    The function takes an image as input and creates a set of icons
    in the src/main/icons/linux folder.

    :param image: Used to Get the image that is used to create the icons.
    :return: None.
    """
    for size in LINUX_ICON_SIZES:
        file_name = os.path.join(
            os.path.abspath(os.path.dirname(sys.argv[0])),
            "linux",
            f"{str(size[0])}.png",
        )

        new_image = image.resize(size)
        new_image.save(file_name)
        print(f"Icon created: {file_name}")


def create_mac_icons(image) -> None:
    """
    The create_mac_icons function creates the mac icons in src/main/icons/mac
    using the image provided as a parameter.

    :param image: Used to Get the image that is used to create the icons.
    :return: None.
    """
    for size in MAC_ICON_SIZES:
        file_name = os.path.join(
            os.path.abspath(os.path.dirname(sys.argv[0])), "mac", f"{str(size[0])}.png"
        )

        new_image = image.resize(size)
        new_image.save(file_name)
        print(f"Icon created: {file_name}")


def create_ico_icon(image) -> None:
    """
    The create_ico_icon function creates an Icon.ico file in the src/main/icons folder
    using the image provided as a parameter.

    :param image: Used to Pass the logo image to the function.
    :return: None.
    """
    new_logo_ico_filename = os.path.join(
        os.path.abspath(os.path.dirname(sys.argv[0])), "Icon.ico"
    )
    new_logo_ico = image.resize((128, 128))
    new_logo_ico.save(new_logo_ico_filename, format="ICO", quality=90)
    print(f"Icon created: {new_logo_ico_filename}")


def main() -> None:
    """
    The main function creates all of the icons for the program.
    It takes an image as a parameter and creates all of the necessary icons from it.
    :return: None.
    """
    image = Image.open("youtube_playlist_generator_icon.png")
    create_base_icons(image)
    create_linux_icons(image)
    create_mac_icons(image)
    create_ico_icon(image)


if __name__ == "__main__":
    main()
