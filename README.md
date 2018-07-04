# school-apps
## Apps
### In Betrieb
keine
### Im Testbetrieb
keine
### In der Entwicklung
- **Dashboard**: Verwaltet Aktivitäten und Benachrichtigungen (welche auch per E-Mail versendet werden, dient also auch zum E-Mail-Versand) 
- **AUB**: Antrag auf Unterrichtsbefreiung
- **Timetable**: Anzeige des Stundenplans, Vertretungsplan fehlt noch
### Ideen (bestätigt)
- Vertretungsplan
- REBUS
### Ideen (unbestätigt)
- Elternsprechtag
- Bundesjungendspiele
- Chat
## Installation
**Hinweis:** Es wird aktuell nur ein aktuelles Debian, Ubuntu, Linux Mint, etc. unterstützt.
### Grundsystem
```
apt install python3 python3-dev python3-pip git mariadb-server python3-venv libldap2-dev libsasl2-dev
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
```

### Django
- Zum Installationsordner wechseln
```
python3 -m venv env 
source env/bin/activate
pip install mysqlclient
pip install django
pip install django-auth-ldap
```
- `example_secure_settings.py` zu `secure_settings.py` kopieren und anpassen
### LDAP (info.katharineum.de)
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






