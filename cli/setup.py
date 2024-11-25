import os
import subprocess
import sys


def check_and_install(package_name):
    """
    Memeriksa apakah package sudah terinstal. Jika belum, menginstalnya.
    """
    try:
        __import__(package_name)
        print(f"'{package_name}' sudah terinstal.")
    except ImportError:
        print(f"'{package_name}' belum terinstal. Menginstall...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"'{package_name}' berhasil diinstal.")
        except subprocess.CalledProcessError as e:
            print(f"Gagal menginstall '{package_name}': {e}")


def install_playwright_browsers():
    """
    Menginstal browser untuk Playwright jika belum diinstal.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install"])
        print("Browser Playwright berhasil diinstal.")
    except subprocess.CalledProcessError as e:
        print(f"Gagal menginstal browser Playwright: {e}")


if __name__ == "__main__":
    print("Mengecek dan menginstal package yang diperlukan...")

    # Daftar package yang diperlukan
    packages = ["playwright"]

    # Iterasi setiap package untuk diperiksa dan diinstal
    for package in packages:
        check_and_install(package)

    # Instal browser Playwright
    install_playwright_browsers()

    print("Semua package dan browser Playwright telah dicek.")
