import os
import cv2
import qrcode
import numpy as np
import sys

BLACK_CHAR = '#'
SCALE = 20

def generate_ascii_qr(data, filename="qr.txt"):
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=1, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    with open(filename, 'w') as f:
        for row in qr.get_matrix():
            f.write(''.join([BLACK_CHAR if cell else ' ' for cell in row]) + '\n')

def render_qr(qr_data_lines, filename):
    max_len = max(len(line) for line in qr_data_lines)
    size = len(qr_data_lines)
    img = np.ones((size*SCALE, max_len*SCALE), dtype=np.uint8) * 255
    for r in range(size):
        line = qr_data_lines[r].ljust(max_len)
        for c in range(max_len):
            if line[c] == BLACK_CHAR:
                img[r*SCALE:(r+1)*SCALE, c*SCALE:(c+1)*SCALE] = 0
    cv2.imwrite(filename, img)

def scan_qr(filename):
    detector = cv2.QRCodeDetector()
    img = cv2.imread(filename)
    if img is None:
        return 1
    data, bbox, _ = detector.detectAndDecode(img)
    if data:
        print("Reconstructed flag:", data)
        return 0
    return 1

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'generate':
        generate_ascii_qr('FLAG{COMPLEX_HISTORY_BUILT_AND_CORRECTED}')
        sys.exit(0)
    if not os.path.exists('qr.txt'):
        sys.exit(1)
    with open('qr.txt', 'r') as f:
        qr_data_lines = [line.rstrip() for line in f if line.strip()]
    render_qr(qr_data_lines, 'qr.png')
    sys.exit(scan_qr('qr.png'))
