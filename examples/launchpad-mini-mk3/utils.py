from random import choice


class Cube:
    CURSOR = "🯅🯆🯇🯈"

    def __init__(self, width, height):
        self._w = width
        self._h = height
        self._cursor = [width // 2, height // 2]

    def show(self, clear=True):
        content = self._generate_content()
        if clear:
            print(f"\033[{self._h + 3}A")
        s = "\n".join("".join(row) for row in content)
        print(s)

    def left(self):
        self._cursor[0] = max(1, self._cursor[0] - 1)
        self.show()

    def right(self):
        self._cursor[0] = min(self._w, self._cursor[0] + 1)
        self.show()

    def up(self):
        self._cursor[1] = max(1, self._cursor[1] - 1)
        self.show()

    def down(self):
        self._cursor[1] = min(self._h, self._cursor[1] + 1)
        self.show()

    def _generate_content(self):
        c = [["╔"] + ["═"] * self._w + ["╗"]]
        for row in range(self._h):
            c.append(["║"] + [" "] * self._w + ["║"])
        c.append(["╚"] + ["═"] * self._w + ["╝"])
        x, y = self._cursor
        c[y][x] = choice(self.CURSOR)
        return c
