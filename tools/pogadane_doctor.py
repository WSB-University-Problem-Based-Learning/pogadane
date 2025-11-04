import os
import sys
import subprocess
import urllib.request
import shutil
from pathlib import Path
import time
import importlib.util

# --- Konfiguracja ---
SCRIPT_VERSION = "0.1.0"
POGADANE_PROJECT_NAME = "pogadane"

# Konfiguracja dla pobierania plików projektu
GITHUB_USERNAME = "WSB-University-Problem-Based-Learning"
GITHUB_REPO = POGADANE_PROJECT_NAME
BRANCH = "main"
BASE_RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{GITHUB_REPO}/{BRANCH}/"

FILES_TO_DOWNLOAD_OR_UPDATE = [
    ("LICENSE", "LICENSE"),
    ("NOTICES.md", "NOTICES.md"),
    ("README.md", "README.md"),
    (".config/config.py", ".config/config.py"),
    ("src/pogadane/gui.py", "src/pogadane/gui.py"),
    ("src/pogadane/transcribe_summarize_working.py", "src/pogadane/transcribe_summarize_working.py"),
]

# Zależności pip dla projektu "pogadane"
REQUIRED_PIP_PACKAGES = [
    {"name": "ttkbootstrap", "import_name": "ttkbootstrap"},
    {"name": "google-generativeai", "import_name": "google.generativeai"}
    # Jeśli projekt "pogadane" zacząłby używać 'requests', dodaj go tutaj:
    # {"name": "requests", "import_name": "requests"},
]

# --- Funkcje Pomocnicze ---

def print_header(title):
    print("\n" + "=" * 60)
    print(f"🩺 {title}")
    print("=" * 60)

def print_status(message, success=True, indent=0):
    prefix = "✅ " if success else "❌ "
    print(" " * indent + prefix + message)

def check_python_version():
    print_header(f"Sprawdzanie wersji Pythona ({POGADANE_PROJECT_NAME} Doctor v{SCRIPT_VERSION})")
    min_major, min_minor = 3, 7
    major, minor = sys.version_info.major, sys.version_info.minor
    if major > min_major or (major == min_major and minor >= min_minor):
        print_status(f"Wersja Pythona: {major}.{minor}.{sys.version_info.micro} (OK, >= {min_major}.{min_minor})")
        return True
    else:
        print_status(f"Wersja Pythona: {major}.{minor}.{sys.version_info.micro} (Problem, wymagana >= {min_major}.{min_minor})", success=False)
        print("      Proszę zaktualizować Pythona.")
        return False

def check_pip_availability():
    print_header("Sprawdzanie dostępności pip")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
        print_status("pip jest dostępny.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_status("pip nie jest dostępny lub nie znaleziono Pythona. Jest to wymagane do instalacji pakietów.", success=False)
        print("      Upewnij się, że Python jest poprawnie zainstalowany i dodany do PATH.")
        return False

def check_and_install_package(pkg_info):
    """Sprawdza i instaluje pakiet pip, jeśli jest potrzebny."""
    package_name = pkg_info["name"]
    import_name = pkg_info.get("import_name", package_name)
    
    print(f"  🔎 Sprawdzanie pakietu: {package_name}")
    
    # Try to find the module spec, but catch ModuleNotFoundError
    try:
        spec = importlib.util.find_spec(import_name)
        if spec is not None:
            print_status(f"Pakiet '{package_name}' jest już zainstalowany.", indent=2)
            return True
    except (ModuleNotFoundError, ValueError, ImportError):
        # Module not found, need to install
        pass
    
    print(f"  ⚠️ Pakiet '{package_name}' nie znaleziony. Próba instalacji...")
    try:
        process = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name],
            check=True, capture_output=True, text=True, encoding='utf-8'
        )
        print_status(f"Pomyślnie zainstalowano '{package_name}'.", indent=2)
        if process.stdout: print(f"     Output instalacji:\n{process.stdout[:300]}...") # Pokaż początek outputu
        return True
    except subprocess.CalledProcessError as e:
        print_status(f"Nie udało się zainstalować '{package_name}'. Kod błędu: {e.returncode}", success=False, indent=2)
        print(f"      Stderr:\n{e.stderr}", indent=2)
        return False
    except FileNotFoundError: # Should be caught by check_pip_availability, but as a safeguard
        print_status(f"Polecenie 'pip' nie znalezione podczas próby instalacji '{package_name}'.", success=False, indent=2)
        return False

def download_file_with_urllib(file_name_in_repo, local_save_path_str):
    """Pobiera plik z GitHub używając urllib."""
    file_url = f"{BASE_RAW_URL}{file_name_in_repo}"
    local_save_path = Path(local_save_path_str)

    print(f"  🌍 Pobieranie {file_name_in_repo} z {file_url}...")
    try:
        local_save_path.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(file_url, timeout=20) as response, open(local_save_path, 'wb') as out_file:
            if response.status >= 400: # Check for HTTP errors
                 print_status(f"Błąd HTTP {response.status} podczas pobierania {file_name_in_repo}.", success=False, indent=2)
                 return False
            shutil.copyfileobj(response, out_file)
        print_status(f"Zapisano {file_name_in_repo} jako {local_save_path}", indent=2)
        return True
    except urllib.error.HTTPError as e:
        print_status(f"Błąd HTTP {e.code} - {e.reason} podczas pobierania {file_name_in_repo}.", success=False, indent=2)
    except urllib.error.URLError as e:
        print_status(f"Błąd URL (np. brak połączenia) dla {file_name_in_repo}: {e.reason}", success=False, indent=2)
    except TimeoutError: # Python 3.10+ for urlopen timeout
         print_status(f"Timeout podczas pobierania {file_name_in_repo}.", success=False, indent=2)
    except OSError as e: # More general OS errors (like file permission)
         print_status(f"Błąd systemowy (np. uprawnienia) przy zapisie {local_save_path}: {e}", success=False, indent=2)
    except Exception as e:
        print_status(f"Niespodziewany błąd podczas pobierania {file_name_in_repo}: {e}", success=False, indent=2)
    return False

# --- Główna Logika ---
def main():
    if not check_python_version():
        sys.exit(1)

    if not check_pip_availability():
        print("\nInstalacja zależności pip nie jest możliwa. Proszę rozwiązać problem z pip/Python.")
        # Można kontynuować pobieranie plików, ale zależności nie zostaną zainstalowane
        # user_choice = input("Czy mimo to kontynuować pobieranie plików projektu? (t/N): ").lower()
        # if user_choice != 't':
        #     sys.exit(1)
        pass # Na razie kontynuujemy do pobierania plików, użytkownik został poinformowany

    # Krok 1: Instalacja zależności pip dla projektu "pogadane"
    print_header("Instalowanie/Sprawdzanie zależności pip dla projektu 'pogadane'")
    all_pip_ok = True
    if REQUIRED_PIP_PACKAGES:
        for pkg_info in REQUIRED_PIP_PACKAGES:
            if not check_and_install_package(pkg_info):
                all_pip_ok = False
        if all_pip_ok:
            print_status("Wszystkie wymagane pakiety pip są zainstalowane.")
        else:
            print_status("Niektóre pakiety pip nie mogły zostać zainstalowane. Sprawdź logi powyżej.", success=False)
    else:
        print("  Brak zdefiniowanych zależności pip do sprawdzenia.")


    # Krok 2: Pobieranie/Aktualizacja plików projektu
    print_header(f"Pobieranie/Aktualizacja plików projektu '{POGADANE_PROJECT_NAME}'")
    
    downloaded_project_files_count = 0
    failed_project_files_downloads = []
    destination_folder = Path(".")  # Pobieranie do bieżącego katalogu

    for file_name_in_repo, local_rel_path in FILES_TO_DOWNLOAD_OR_UPDATE:
        local_file_path = destination_folder / local_rel_path
        
        # Obsługa backupu dla config.py
        if local_rel_path.endswith("config.py") and local_file_path.exists():
            print(f"  ℹ️ Plik konfiguracyjny '{local_file_path}' istnieje.")
            timestamp = int(time.time())
            backup_path = destination_folder / f"{local_file_path.stem}.backup_{timestamp}{local_file_path.suffix}"
            try:
                local_file_path.rename(backup_path)
                print_status(f"Utworzono backup '{local_file_path}' jako: {backup_path}", indent=4)
            except OSError as e:
                print_status(f"Nie udało się utworzyć backupu dla {local_file_path}: {e}", success=False, indent=4)
                user_choice = input(f"      Czy chcesz kontynuować i nadpisać '{local_file_path}' bez backupu? (t/N): ").strip().lower()
                if user_choice != 't':
                    print(f"      Pominięto pobieranie '{local_file_path}'.")
                    failed_project_files_downloads.append(local_rel_path)
                    continue
        
        if download_file_with_urllib(file_name_in_repo, str(local_file_path)):
            downloaded_project_files_count += 1
        else:
            failed_project_files_downloads.append(local_rel_path)

    print("\n--- Podsumowanie pobierania plików projektu ---")
    if downloaded_project_files_count > 0:
        print_status(f"Pomyślnie pobrano/zaktualizowano {downloaded_project_files_count} plików projektu do katalogu: {destination_folder.resolve()}")
    
    if failed_project_files_downloads:
        print_status(f"Nie udało się pobrać {len(failed_project_files_downloads)} plików projektu: {', '.join(failed_project_files_downloads)}", success=False)
    
    if downloaded_project_files_count == 0 and not failed_project_files_downloads:
        print("  🤔 Żadne pliki projektu nie zostały pobrane (mogły być pominięte lub lista jest pusta).")

    print("\n🏁 Działanie 'pogadane_doctor.py' zakończone.")
    print("💡 Jeśli wystąpiły problemy, przejrzyj komunikaty powyżej.")
    if not all_pip_ok:
        print("   🔴 Nie udało się zainstalować wszystkich zależności pip. Główny program 'pogadane' może nie działać poprawnie.")
    print("   Teraz możesz spróbować uruchomić 'python -m pogadane.gui' lub 'python -m pogadane.transcribe_summarize_working'.")

if __name__ == "__main__":
    main()