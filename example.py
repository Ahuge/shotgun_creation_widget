from Qt import QtWidgets
from shotgun_api3 import Shotgun

# from sg.cached import Shotgun as CachedShotgun

from shotgun_creation_widget import ShotgunEntityCreationWidget

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    shotgun_connection = Shotgun(
        raw_input("Shotgun Site: "),
        login=raw_input("Username: "),
        password=raw_input("Password: "),
    )
    # shotgun_connection = CachedShotgun.wrap_existing(shotgun_connection)
    project_entity = shotgun_connection.find_one(
        "Project",
        filters=[["id", "is", 155]],
        fields=["code", "name", "tank_name"]
    )
    entity_type = "Shot"
    w = ShotgunEntityCreationWidget(
        shotgun_connection=shotgun_connection,
        project_entity=project_entity,
        entity_type=entity_type,
        data={"head_in": 1001},
        additional_fields=[],
        parent=None
    )
    w.show()
    app.exec_()
