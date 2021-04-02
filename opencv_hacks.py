'''quickhack was in den server gehoeren muss
ist halt jetzt als quickhack da
'''
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
import temp
import os


def qpixmap_to_cvmat(img: QPixmap) -> np.array:
    try:
        path = temp.tempfile() + '.png'
        img.save(path)
        mat = cv2.imread(path, cv2.IMREAD_COLOR)
    finally:
        if os.path.exists(path):
            os.remove(path)
    return mat


def cvmat_to_qpixmap(mat: np.array) -> QPixmap:
    try:
        tmpfn = temp.tempfile() + '.png'
        cv2.imwrite(tmpfn, mat)
        img = QPixmap()
        img.load(tmpfn)
    finally:
        if os.path.exists(tmpfn):
            os.remove(tmpfn)
    return img


def qpixmap_to_border_512x512(img: QPixmap) -> QPixmap:
    mat = qpixmap_to_cvmat(img)
    if mat.shape[0] > mat.shape[1]:
        bs = int((mat.shape[0] - mat.shape[1]) / 2)
        mq = cv2.copyMakeBorder(mat, 0, 0, bs, bs, cv2.BORDER_REPLICATE)
    elif mat.shape[1] > mat.shape[0]:
        bs = int((mat.shape[1] - mat.shape[0]) / 2)
        mq = cv2.copyMakeBorder(mat, bs, bs, 0, 0, cv2.BORDER_REPLICATE)
    else:
        mq = mat
    dim = (512, 512)
    resized = cv2.resize(mq, dim, interpolation=cv2.INTER_AREA)
    return cvmat_to_qpixmap(resized)


def qpolygon_tocvcontour(poly):
    res = []
    for i in range(poly.count()):
        p = poly.at(i).toPoint()
        res.append([p.x(), p.y()])
    return np.array(res)


def build_oldstyle_png_with_alpha(img: QPixmap, poly) -> bytes:
    # draw contour
    b, g, r = cv2.split(qpixmap_to_cvmat(img))
    conts = qpolygon_tocvcontour(poly)
    a = np.zeros((512, 512, 1), np.uint8)
    cv2.fillPoly(a, [conts], 255)
    img = cv2.merge((b, g, r, a))
    _, data = cv2.imencode('.png', img)
    return data.tobytes()
