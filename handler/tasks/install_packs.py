if __name__ == '__main__':
    import os
    import glob
    os.chdir('./packs')
    packsDir = os.getcwd()
    packs = glob.glob("./*")
    print(packsDir)
    print([pack for pack in packs])
    for pack in packs:
        os.chdir(pack)
        print(f"[package] found package at {pack} -> installing requirements.txt")
        os.system('pip install -r requirements.txt')
        os.system('touch installed.lock')
        os.chdir(packsDir)