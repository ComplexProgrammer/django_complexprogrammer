import os

# CloudLinux / cPanel thread limitini saqlash:
# Server 64 yadroli bo'lgani uchun OpenBLAS/NumPy sukut bo'yicha 64 ta thread ochishga urinadi.
# Bu esa hostingning NPROC (threads) limitiga urilib, "Resource temporarily unavailable" xatosini keltirib chiqaradi.
# Quyidagi o'zgaruvchilar uni faqat 1 ta thread ishlatishga majburlaydi.
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"

from django_complexprogrammer.wsgi import application