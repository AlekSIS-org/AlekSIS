# school-apps
## Apps
# In Betrieb
keine
# Im Testbetrieb
keine
# In der Entwicklung
- **Dashboard**: Verwaltet Aktivitäten und Benachrichtigungen (welche auch per E-Mail versendet werden, dient also auch zum E-Mail-Versand) 
- **AUB**: Antrag auf Unterrichtsbefreiung
# Ideen (bestätigt)
- Stunden-, Vertretungsplan
- REBUS
# Ideen (unbestätigt)
- Elternsprechtag
- Bundesjungendspiele
## Installation
### Grundsystem
```
apt install python3 python3-pip python3-mysqldb git mysql-server
pip3 install django
```

### MySQL-Datenbank
1. Datenbank `schoolapps` (`utf8_general_ci`) anlegen
2. Benutzer `www-data` anlegen
3. Benutzer `www-data` alle Rechte auf `schoolapps` geben
```
mysql -u root -p
CREATE DATABASE schoolapps;
```



