![](https://katharineum-zu-luebeck.de/wp-content/uploads/2017/05/Logo_aktuell_2-2.png)
# SchoolApps
## Apps
siehe Wiki
## Installation
**Hinweis:** Es wird aktuell nur ein aktuelles Debian, Ubuntu, Linux Mint, etc. unterstützt. Es werden Root-Rechte benötigt.

### Grundsystem
```
sudo apt install python3 python3-dev python3-pip git mariadb-server python3-venv libldap2-dev libsasl2-dev libmysqlclient-dev
```

### MySQL-Datenbank
1. Datenbank `schoolapps` (`utf8_general_ci`) anlegen
2. Benutzer `www-data` anlegen
3. Benutzer `www-data` alle Rechte auf `schoolapps` geben
4. Benutzer `untis-read` anlegen
5. Benutzer `untis-read` Leserechte auf UNTIS-DB geben
```
mysql -u root -p
CREATE USER 'www-data'@'localhost' IDENTIFIED BY 'grummelPASS1531';
GRANT ALL PRIVILEGES ON *.* TO 'www-data'@'localhost';
CREATE USER 'untis-read'@'localhost' IDENTIFIED BY 'grummelPASS1531';
GRANT ALL PRIVILEGES ON *.* TO 'untis-read'@'localhost';
CREATE DATABASE schoolapps;
CREATE DATABASE Untis;
```

### UNTIS-Beispieldaten laden
1. PhpMyAdmin öffnen und die Datei untiskath.sql vom Forum importieren.

### SchoolApps clonen
```
git clone git@github.com:Katharineum/school-apps.git
```

### Django
- Zum Installationsordner wechseln
```
python3 -m venv env
source env/bin/activate
pip install mysqlclient
pip install django
pip install django-auth-ldap
pip install django-dbsettings
pip install django_pdb
pip install django-material
pip install django-filter
```
- `example_secure_settings.py` zu `secure_settings.py` kopieren und anpassen

### Submodules updaten
```
git submodule init
git submodule update
```

### Migrations auflösen
Leider kommt es bei einer Erstinstallation von SchoolApps immer zu Problemen mit den Migrations. Sollte es Schwierigkeiten geben, @hansegucker kontaktieren.

Für die Migration folgende Befehle im aktivierten VirtualEnv ausführen:
```
python3 schoolapps/manage.py makemigrations
python3 schoolapps/manage.py migrate
```

### Testlauf

## LDAP (info.katharineum.de)

**WICHTIG: LDAP funktioniert nur bei Root-Zugriff auf dem Infoserver!**

#### Adresse vom Info aus:
localhost:389

#### BIND-Nutzer
DN: uid=readldap,ou=people,dc=skole,dc=skolelinux,dc=no
PW: grummelPASS1531

#### BASIS DN
dc=skole,dc=skolelinux,dc=no

#### SSH-Tunnel herstellen
```sudo ssh -L 389:localhost:389 <user>@info.katharineum.de -N ```
	(<user> durch Nutzer ersetzen)

#### Verbindung testen
1. Tunnel erstellen (siehe Befehl)
2. Apache Active Directory (AD) zum Testen öffnen (Download unter http://directory.apache.org/studio/)
3. Verbindung in AD mit oben genannten Daten herstellen


