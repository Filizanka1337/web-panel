import threading
import os
from flask import Flask, render_template, Response, request, redirect, url_for
from colorama import Fore, Style

# Inicjalizacja colorama
Fore.RED + Style.RESET_ALL

# Wyświetlanie ASCII arta (logo) z pliku logo.txt w kolorze czerwonym
with open(os.path.join('data', 'logo.txt'), 'r') as logo_file:
    logo_text = logo_file.read()
    print(Fore.RED + logo_text + Style.RESET_ALL)

print(Fore.RED + "web panel by filizanka")

# Tworzymy aplikację Flask
app = Flask(__name__)

# Ustalamy ścieżkę do folderu z szablonami HTML (data)
templates_folder = os.path.join(os.path.dirname(__file__), 'data')

# Definiujemy funkcję, która uruchomi SSH
def zadanie_ssh():
    os.system("wssh")

# Odczytujemy zawartość pliku ncat.html
with open(os.path.join(templates_folder, 'ncat.html'), 'r') as ncat_file:
    ncat_content = ncat_file.read()

# Definiujemy funkcję, która uruchomi aplikację Flask na porcie 80
def zadanie_flask():
    @app.route('/')
    def index():
        # Pobieramy adres IP bieżącego połączenia
        ip_address = request.remote_addr
        # Przekazujemy adres IP do szablonu
        return render_template('index.html', ncat_content=ncat_content, ip_address=ip_address)

    @app.route('/ncat.html')
    def ncat():
        return render_template('ncat.html')

    @app.route('/stream_ncat')
    def stream_ncat():
        def generate():
            # Tutaj możesz przesyłać dane do przeglądarki w trybie strumieniowym
            yield "To jest treść strumienia\n"

        return Response(generate(), mimetype="text/plain")

    @app.route('/start_ncat', methods=['POST'])
    def start_ncat():
        # Uruchamiamy funkcję ncat0serwer0start(), która uruchomi ncat
        ncat0serwer0start()

        return redirect(url_for('ncat'))  # Przekierowanie na stronę ncat.html po zakończeniu

    @app.route('/start_ssh_server', methods=['POST'])
    def start_ssh_server():
        # Uruchamiamy funkcję start_sshd(), która włączy usługę SSH w PowerShell
        start_sshd()

        return redirect(url_for('index'))  # Przekierowanie na stronę główną po zakończeniu

    # Ustawiamy ścieżkę do folderu z szablonami HTML
    app.template_folder = templates_folder
    app.run(host='0.0.0.0', port=80)  # Zmieniamy port na 80

# Funkcja do uruchomienia serwera ncat z odpowiednimi argumentami
def ncat0serwer0start():
    os.system("ncat -l -p 82 -e cmd.exe")

# Funkcja do uruchomienia usługi SSH w PowerShell
def start_sshd():
    os.system('powershell.exe Start-Service sshd')

# Tworzymy dwa wątki, jeden dla każdej funkcji
watek_ssh = threading.Thread(target=zadanie_ssh)
watek_flask = threading.Thread(target=zadanie_flask)

# Uruchamiamy wątki
watek_ssh.start()
watek_flask.start()

# Oczekujemy na zakończenie wątków
watek_ssh.join()
watek_flask.join()

# Po zakończeniu wątków możemy kontynuować wykonywanie kodu głównego
print(Fore.RESET + "Wykonywanie kodu głównego...")
