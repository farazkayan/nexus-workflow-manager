import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt

def main():
    # Use offscreen platform to avoid X11 requirements
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    app = QApplication(sys.argv)
    
    ext_icons_dir = os.path.join(os.path.dirname(__file__), "nexus-extension", "icons")
    sizes = [16, 32, 48, 128]
    
    for size in sizes:
        svg_path = os.path.join(ext_icons_dir, f"icon{size}.svg")
        png_path = os.path.join(ext_icons_dir, f"icon{size}.png")
        
        if os.path.exists(svg_path):
            img = QImage(size, size, QImage.Format_ARGB32)
            img.fill(Qt.transparent)
            
            painter = QPainter(img)
            renderer = QSvgRenderer(svg_path)
            renderer.render(painter)
            painter.end()
            
            img.save(png_path)
            print(f"Created {png_path} from SVG.")
        else:
            # Fallback if svg missing, just create a solid box with an 'N'
            img = QImage(size, size, QImage.Format_ARGB32)
            img.fill(Qt.blue)
            painter = QPainter(img)
            painter.setPen(Qt.white)
            painter.drawText(img.rect(), Qt.AlignCenter, "N")
            painter.end()
            img.save(png_path)
            print(f"Created plain fallback {png_path}.")

if __name__ == "__main__":
    main()
