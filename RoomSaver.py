import csv


class RoomSaver:
    def save_room(cells):
        with open('savefile.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['x', 'y', 'z', 'material_property_id'])
            for i in range(len(cells)):
                for j in range(len(cells[i])):
                    for k in range(len(cells[i][j])):
                        if cells[i][j][k] is not None:
                            writer.writerow([i, j, k, cells[i][j][k].toString()])

    def load_room(cells, cellGenerator):
        with open('savefile.csv', mode='r') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                # print(int(row["x"]),row["y"],row["z"],row["material_property_id"])
                position = [int(row["x"]), int(row["y"]), int(row["z"])]
                cells[position[0]][position[1]][position[2]] = \
                    cellGenerator.get_cell(position, int(row["material_property_id"]))
