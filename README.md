![](https://katharineum-zu-luebeck.de/wp-content/uploads/2017/05/Logo_aktuell_2-2.png)
# SchoolApps
## Apps
siehe Wiki
## Installation
**Hinweis:** Es werden nur Linux-basierte Systeme unterstützt (in dieser Anleitung wird sich auf Debian-basierte Systeme wie Ubuntu oder Linux Mint bezogen). Außerdem werden Root-Rechte benötigt.

### Grundsystem
```
sudo apt install python3 python3-dev python3-pip git mariadb-server python3-venv libldap2-dev libsasl2-dev libmysqlclient-dev pandoc texlive texlive-fonts-extra texlive-lang-german texlive-latex-extra
```

### MySQL-Datenbank
1. Datenbank `schoolapps` (`utf8_general_ci`) anlegen
2. Benutzer `www-data` anlegen
3. Benutzer `www-data` alle Rechte auf `schoolapps` geben
4. Benutzer `untis-read` anlegen
5. Benutzer `untis-read` Leserechte auf UNTIS-DB geben

```
mysql -u root -p
CREATE DATABASE schoolapps;
CREATE DATABASE Untis;
CREATE USER 'www-data'@'localhost' IDENTIFIED BY 'grummelPASS1531';
GRANT ALL PRIVILEGES ON schoolapps.* TO 'www-data'@'localhost';
CREATE USER 'untis-read'@'localhost' IDENTIFIED BY 'grummelPASS1531';
GRANT SELECT ON Untis.* TO 'untis-read'@'localhost';
```

Hinweis: In Testumgebungen kann untis-read auch entfallen und 
stattdessen www-data auch für den Zugriff auf die Datenbank `Untis` verwendet werden:

```
GRANT SELECT ON Untis.* TO 'www-data'@'localhost';
```

### UNTIS-Beispieldaten importieren
Zum Testen kann die Datei `untiskath.sql` vom Forum in die Datenbank `Untis` importiert werden.


### SchoolApps clonen
```
git clone git@github.com:Katharineum/school-apps.git
```

### Django installieren
- Zum Installationsordner wechseln, dann:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

- `example_secure_settings.py` zu `secure_settings.py` kopieren und anpassen (hier müssen auch die passenden DB-Zugangsdaten eingetragen werden)


### Migrations durchführen/auflösen
Leider kommt es bei einer Erstinstallation von SchoolApps immer noch zu Problemen mit den Migrations. Sollte es Schwierigkeiten geben, @hansegucker kontaktieren.

Für die Migration folgende Befehle im aktivierten VirtualEnv ausführen:
```
python3 schoolapps/manage.py makemigrations
python3 schoolapps/manage.py migrate
```

### Testlauf
- Administratornutzer erstellen
```
python3 schoolapps/manage.py createsuperuser
```
- Django-Devserver starten
```
python3 schoolapps/manage.py runserver
```
- Einstellungen anpassen (http://127.0.0.1:8080/settings, siehe auch "Kanboard-Verbindung einrichten")

- SchoolApps benutzen 😃


### Kanboard-Verbindung einrichten
1. Zu den [Einstellungen](localhost:8000/settings) navigieren (/settings)
2. Den Kanboard-API-Key von [Kanboard](https://kanboard.katharineum.de/?controller=ConfigController&action) eintragen
3. Die Project-IDs von `REBUS` (#4) und `Feedback` (#18) eintragen
4. Die richtigen E-Mailadressen eintragen


## settings.py
Die settings können aus verschiedenen Quellen kommen.
1. Feste Settings (bspw. MEDIA_DIR) werden über `settings.py` festgelegt
2. Variable Settings (bspw. Datenbankzugangsdaten) benutzen in `settings.py` den `getenv`-Befehl mit Defaultwert
3. Diese variablen Settings lassen sich mit der Datei `secure_settings.py` überschreiben


Reihenfolge
1. `settings.py`
2. `settings.py` – `getenv`-Defaultwert
3. Umgebungsvariablen (`getenv`)
4. `secure_settings.py`

## LDAP (info.katharineum.de)

**WICHTIG:** LDAP funktioniert nur mit Nutzern, die folgende Gruppe haben: `info-admins`

#### Adresse lokal von info.katharineum.de
`localhost:389`

#### BIND-Nutzer
DN: `uid=readldap,ou=people,dc=skole,dc=skolelinux,dc=no`
PW: `grummelPASS1531`

#### Basis-DN
`dc=skole,dc=skolelinux,dc=no`

#### SSH-Tunnel herstellen
```sudo ssh -L 389:localhost:389 <user>@info.katharineum.de -N ```
	(`<user>` durch Nutzer mit Gruppe `info-admins` ersetzen)

#### Verbindung testen
1. Tunnel erstellen (siehe Befehl)
2. Apache Active Directory (AD) zum Testen öffnen (Download unter http://directory.apache.org/studio/)
3. Verbindung in AD mit oben genannten Daten herstellen
