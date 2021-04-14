import os
import os.path as path
dir_path = path.dirname(path.realpath(__file__))
dst = path.expanduser('~/Desktop/Liveview.desktop')
print(dir_path)


icon = '{}/icon.png'.format(dir_path)
exc = '{}/run.sh'.format(dir_path)

data = """[Desktop Entry]
Version=1.0
Type=Application
Terminal=true
Icon={}
Name=Liveview
Exec={}
""".format(icon, exc)
open(dst, 'w').write(data)

os.system("chmod +x {}".format(dst))
