from models.filament import Filament


class Spool:
    def __init__(self, id=None, filament=Filament, original_filament_weight=None, original_spool_weight=None,
                 original_length=None, last_weight=None):
        self.id = id
        self.filament = filament
        self.original_filament_weight = original_filament_weight
        self.original_spool_weight = original_spool_weight
        self.original_length = original_length
        self.last_weight = last_weight if last_weight is not None else original_spool_weight

    def calculate_length_by_weight(self, weight):
        spool_weight = self.original_spool_weight - self.original_filament_weight

        rest_filament_weight = weight - spool_weight

        return self.original_length / self.original_filament_weight * rest_filament_weight

    def __str__(self):
        return (f"Spool(id={self.id}, filament_id={self.filament.id}, original_length='{self.original_length}', "
                f"original_filament_weight={self.original_filament_weight}, original_spool_weight={self.original_spool_weight}, last_weight={self.last_weight}, estimate={self.calculate_length_by_weight(self.last_weight)}m)")


def spool_from_db(row):
    return Spool(
        id=row[0],
        original_filament_weight=row[2],
        original_spool_weight=row[3],
        original_length=row[4],
        filament=Filament(
            id=row[5],
            manufacturer=row[6],
            filament_type=row[7],
            color_name=row[8],
            custom_name=row[9]
        ),
        last_weight=row[10]
    )