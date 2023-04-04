if __name__ == '__main__':
    import os
    import glob
    os.chdir('./tasks/packs')
    packsDir = os.getcwd()
    packs = glob.glob("./*")
    for pack in packs:
        if('__pycache__' not in pack and os.path.isdir(pack)):
            os.chdir(pack)
            print(f"[package] found package '{pack.replace('./', '')}' -> installing requirements.txt")
            os.system('pip install --no-cache-dir -r requirements.txt')
            os.system('touch installed.lock')
            os.chdir(packsDir)