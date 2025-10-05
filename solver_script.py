
import os
from PIL import Image
from pyzbar.pyzbar import decode
import qrcode
import sys

QR_SIZE = 25 
SCALE = 20
BLACK_CHAR = '#'
WHITE_CHAR = ' '

def generate_ascii_qr(data, filename="qr.txt"):
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=1, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    
    with open(filename, 'w') as f:
        for row in qr.get_matrix():
            # **FIXED SYNTAX** (Note: '
#' is correctly closed)
            f.write("".join([BLACK_CHAR if cell else WHITE_CHAR for cell in row]) + '\n')

    
def render_qr(qr_data_lines, filename):
    size = len(qr_data_lines)
    img_size = size * SCALE
    img = Image.new('L', (img_size, img_size), 255)
    pixels = img.load()
    
    for r in range(size):
        for c in range(size):
            char = qr_data_lines[r][c]
            color = 0 if char in (BLACK_CHAR, '1') else 255
            
            for i in range(SCALE):
                for j in range(SCALE):
                    pixels[c * SCALE + j, r * SCALE + i] = color
    img.save(filename)
    return True
    
def scan_qr(filename):
    try:
        decoded_objects = decode(Image.open(filename))
        return 0 if decoded_objects else 1
    except Exception:
        return 1

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'generate':
        generate_ascii_qr('FLAG{COMPLEX_HISTORY_BUILT_AND_CORRECTED}')
        sys.exit(0)
    
    if not os.path.exists('qr.txt'):
        sys.exit(1)
    
    try:
        with open('qr.txt', 'r') as f: 
            qr_data_lines = [line.strip() for line in f if line.strip()]
    except Exception:
        sys.exit(1)
    
    if not render_qr(qr_data_lines, 'qr.png'):
        sys.exit(1)
        
    sys.exit(scan_qr('qr.png'))
    