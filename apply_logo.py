import sys
import os
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PySide6.QtGui import QImage
from PySide6.QtCore import Qt

def main():
    app = QApplication(sys.argv)
    
    # Prompt the user to select the logo they provided
    file_path, _ = QFileDialog.getOpenFileName(None, "Select the Logo Image for Nexus", "", "Images (*.png *.jpg *.jpeg)")
    
    if not file_path:
        print("No image selected. Exiting.")
        return

    # Load the image
    img = QImage(file_path)
    if img.isNull():
        QMessageBox.critical(None, "Error", "Failed to load the selected image.")
        return

    # 1. Save the main app icon
    app_icon_path = "nexus_icon.png"
    img.scaled(256, 256, Qt.IgnoreAspectRatio, Qt.SmoothTransformation).save(app_icon_path)
    print(f"Saved main app icon to {app_icon_path}")

    # 2. Save the extension icons
    sizes = [16, 32, 48, 128]
    ext_icons_dir = os.path.join("nexus-extension", "icons")
    os.makedirs(ext_icons_dir, exist_ok=True)

    for size in sizes:
        scaled_img = img.scaled(size, size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        icon_path = os.path.join(ext_icons_dir, f"icon{size}.png")
        scaled_img.save(icon_path)
        print(f"Saved extension icon to {icon_path}")

    # 3. Embed logo as base64 in HTML files
    import base64
    from PySide6.QtCore import QBuffer, QIODevice

    # Create a 20x20 base64 string
    img20 = img.scaled(20, 20, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    buffer = QBuffer()
    buffer.open(QIODevice.WriteOnly)
    img20.save(buffer, "PNG")
    base64_20px = buffer.data().toBase64().data().decode()

    html_img_tag = f'<img src="data:image/png;base64,{base64_20px}" style="width:100%;height:100%;border-radius:4px;object-fit:cover;display:block;">'

    ext_dir = "nexus-extension"
    html_files = ["popup.html", "workflow_picker.html"]
    for html_file in html_files:
        html_path = os.path.join(ext_dir, html_file)
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "<!-- LOGO_PLACEHOLDER -->" in content:
                content = content.replace("<!-- LOGO_PLACEHOLDER -->", html_img_tag)
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Embedded logo in {html_file}")

    QMessageBox.information(None, "Success", "Logo successfully applied to the app and extension!\nYou can now load the extension in Chrome.")

if __name__ == "__main__":
    main()
