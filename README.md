# school-apps
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



