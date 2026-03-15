import zipfile, re

z = zipfile.ZipFile('CheckpointB.zip')
hashes = set(re.findall(r'\b[a-fA-F0-9]{40}\b', open('amcache_sha1_with_names.txt').read()))

for p in hashes:
    try:
        z.extractall(pwd=p.encode())
        print(f"Password: {p}")
        break
    except:
        pass