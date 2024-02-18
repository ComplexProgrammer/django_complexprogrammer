import subprocess

# Kutubxonalar ro'yxatini olish
installed_packages = subprocess.check_output(['pip', 'list']).decode('utf-8').split('\n')[2:]
# Har bir kutubxonani hajmini aniqlash
package_sizes = {}
for package in installed_packages:
    if package.strip():
        parts = package.split()
        package_name = parts[0]
        package_size = parts[-1]
        package_sizes[package_name] = package_size
        print(package_name, package_size)

largest_package = max(package_sizes.items(), key=lambda x: int(x[1]))

print(f"Eng katta hajmli kutubxona: {largest_package[0]} - {largest_package[1]}")
