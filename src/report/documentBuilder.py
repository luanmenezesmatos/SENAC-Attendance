from fpdf import FPDF


class DocumentBuilder:
    def __init__(self):
        self.pdf = FPDF()

    def create_table(self, table_data, dataframe):
        self.pdf.add_page()

        # Cabeçalho da tabela
        self.pdf.set_font('Times', 'B', size=16)
        for row in table_data:
            for item in row:
                self.pdf.cell(40, 10, txt=item, ln=1, align="C")
            self.pdf.ln()

        # Corpo da tabela
        self.pdf.set_font('Times', size=16)
        for i in range(0, len(dataframe)):
            self.pdf.cell(40, 10, txt=dataframe[i], ln=1, align="C")

        self.save("report.pdf")

    def create_report(self, table_data):
        try:
            self.pdf.add_page()

            self.pdf.set_font('Times', size=10)

            self.create_table(table_data=table_data, title="Frequência", cell_width="even")
            self.pdf.ln()

            self.save("report.pdf")

            return True
        except Exception as e:
            print(f"Erro na função: {e}")
            return False

    def save(self, path):
        self.pdf.output(path, 'F')
