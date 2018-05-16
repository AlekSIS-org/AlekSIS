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
### Grundsystem
```
apt install python3 python3-dev python3-pip  git mariadb-server python3-venv
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
```

### Django
- Zum Installationsordner wechseln
```
python3 -m venv env
source env/bin/activate
pip install mysqlclient
pip install django
```
- `example_secure_settings.py` zu `secure_settings.py` kopieren und anpassen






