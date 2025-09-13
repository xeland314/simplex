#!/bin/bash
set -e

#Compile the whole project
#uv run pyinstaller app.py --name simplex_solver --windowed --add-data="gui/assets:gui/assets"
#cp dist/simplex_solver/_internal/gui /dist/simplex_solver/

APP_NAME="SimplexSolver"
DIST_DIR="dist/simplex_solver"
APPDIR="$APP_NAME.AppDir"

# 1️⃣ Limpiar AppDir antiguo
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"

# 2️⃣ Copiar todo el contenido del dist de PyInstaller
cp -r "$DIST_DIR/"* "$APPDIR/usr/bin/"

# 3️⃣ Copiar icono y renombrarlo para AppImage
cp "$DIST_DIR/gui/assets/pixel-cat.png" "$APPDIR/$APP_NAME.png"

# 4️⃣ Crear AppRun
cat > "$APPDIR/AppRun" <<EOF
#!/bin/bash
HERE="\$(dirname "\$(readlink -f "\${0}")")"
export LD_LIBRARY_PATH="\$HERE/usr/bin:\$LD_LIBRARY_PATH"
exec "\$HERE/usr/bin/simplex_solver" "\$@"
EOF
chmod +x "$APPDIR/AppRun"

# 5️⃣ Crear archivo desktop
cat > "$APPDIR/$APP_NAME.desktop" <<EOF
[Desktop Entry]
Name=$APP_NAME
Exec=simplex_solver
Icon=$APP_NAME
Type=Application
Categories=Utility;
EOF

# 6️⃣ Generar AppImage
appimagetool "$APPDIR"
