import npyscreen


class TestApp(npyscreen.NPSApp):
    def __init__(self, output):
        self.output = output

    def main(self):
        self.F = npyscreen.Form(name="TCPing", editable=True)

        self.obj = self.F.add(npyscreen.GridColTitles, name="Ping #2",
                              col_titles=["host:port",
                                          "state of last packet",
                                          "time of last packet",
                                          "min/avg/max"],
                              scroll_exit=True, values=[["", "", "", ""]])
        self.F.display()
        self.obj.values.append(self.output)
        while True:
            self.obj.values = []
            for e in self.output:
                self.obj.values.append(e.output)

            self.F.display()


def Screen(output):
    App = TestApp(output)
    App.run()
