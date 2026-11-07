"""Disk kvotasi (Errno 122: Disk quota exceeded / Errno 28: No space left) tölganida ham
saytni 500 Internal Server Error bilan yiqitmaydigan xavfsiz fayl-keş bekendi.
"""

import errno
import glob
import logging
import os

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache.backends.filebased import FileBasedCache

logger = logging.getLogger(__name__)

_QUOTA_ERRNOS = {
    getattr(errno, "EDQUOT", 122),  # 122: Disk quota exceeded (cPanel / CloudLinux)
    getattr(errno, "ENOSPC", 28),   # 28: No space left on device
}


class SafeFileBasedCache(FileBasedCache):
    """Django FileBasedCache ustidan xavfsiz qobiq:
    - Disk yoki inode kvotasi tölganda (OSError 122 / 28) avtomatik ravişda eski keş fayllarini
      tozalaydi (_emergency_purge) va qayta yozib köradi.
    - Agar diskda baribir joy bölmasa, OSError'ni yutib, saytning keşsiz (in-memory/fallback)
      uzluksiz işlaşini ta'minlaydi (500 xatolik bermaydi).
    """

    def _createdir(self):
        try:
            super()._createdir()
        except OSError as exc:
            logger.warning("Keş papkasini yaratib bölmadi (%s): %s", self._dir, exc)

    def _emergency_purge(self):
        """Kvota tölganda keş papkasidagi mavjud fayllarni tozalaydi."""
        try:
            if not os.path.exists(self._dir):
                return
            filelist = glob.glob(os.path.join(self._dir, f"*{self.cache_suffix}"))
            # Şuningdek mkstemp yaratgan va qolib ketgan vaqtinçalik fayllarni ham tozalaymiz
            all_files = [
                os.path.join(self._dir, name)
                for name in os.listdir(self._dir)
            ]
            targets = all_files if len(all_files) > len(filelist) else filelist
            for fpath in targets:
                try:
                    os.remove(fpath)
                except OSError:
                    pass
        except OSError:
            pass

    def get(self, key, default=None, version=None):
        try:
            return super().get(key, default=default, version=version)
        except OSError:
            return default

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        try:
            super().set(key, value, timeout=timeout, version=version)
            return True
        except OSError as exc:
            if exc.errno in _QUOTA_ERRNOS:
                self._emergency_purge()
                try:
                    super().set(key, value, timeout=timeout, version=version)
                    return True
                except OSError:
                    pass
            logger.warning("Keşga yozib bölmadi (key=%s): %s", key, exc)
            return False

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        try:
            if self.has_key(key, version):
                return False
        except OSError:
            return False
        return bool(self.set(key, value, timeout=timeout, version=version))

    def delete(self, key, version=None):
        try:
            return super().delete(key, version=version)
        except OSError:
            return False

    def touch(self, key, timeout=DEFAULT_TIMEOUT, version=None):
        try:
            return super().touch(key, timeout=timeout, version=version)
        except OSError:
            return False

    def has_key(self, key, version=None):
        try:
            return super().has_key(key, version=version)
        except OSError:
            return False

    def clear(self):
        try:
            super().clear()
        except OSError:
            self._emergency_purge()
