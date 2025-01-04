import csv
from pyad import aduser, adcontainer
from pyad.adobject import ADObject

OU_PATH = "OU=UsersByScript,DC=FUCK,DC=OFF" # Ich habe jetzt eine eigene OU erstellt, um sicher keine Konflikte zu kreiren.
DOMAIN_SUFFIX = "@FUCK.OFF"  # Haha, ich hab das Skript am Samstag noch gemacht, ich hatte keine Zeit noch einen neuen Domain Controller aufzubauen und habe deswegen den hier genommen, deswegen das wüste Domain Suffix.

def create_user(logonname, first_name, last_name, office_location):
    try:
        # Der UPN ist in unserem Fall immer der Logon name + der Domain Suffix
        user_upn = logonname + DOMAIN_SUFFIX
        
        container = adcontainer.ADContainer.from_dn(OU_PATH)
        
        # Hier erstellen wir unseren Benutzer
        user = aduser.ADUser.create(
            name=f"{first_name} {last_name}",
            container_object=container,
            password="Willk0mmen!",  # Ein Default-Passwort dass der Benutzer ohnehin beim ersten Login anpassen muss.
            upn=user_upn
        )
        user.update_attribute("givenName", first_name)
        user.update_attribute("sn", last_name)
        user.update_attribute("displayName", f"{first_name} {last_name}")
        user.update_attribute("physicalDeliveryOfficeName", office_location)
        user.enable()
        print(f"User {user_upn} created successfully.") # Durch diese Statusmeldungen wissen wir stets an was das Skript gerade ist.
    except Exception as e:
        print(f"Failed to create user {logonname}: {e}") # Hier würden wir ausfindig machen welcher User Probleme beim erstellen bereitet.

def main():
    csv_file = "users.csv"  # Pfad zum CSV-File
    try:
        with open(csv_file, mode="r") as file: # Hier importieren wir all die Parameter vom CSV.
            reader = csv.DictReader(file)
            for row in reader:
                logonname = row["logonname"]
                first_name = row["FirstName"]
                last_name = row["LastName"]
                office_location = row["OfficeLocation"]
                create_user(logonname, first_name, last_name, office_location) # Und hier callen wir die Funktion welche den Benutzer dann erstellt.
    except FileNotFoundError:
        print(f"File {csv_file} not found.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")

if __name__ == "__main__":
    main()
