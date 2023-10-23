from fpdf import FPDF


class DocumentBuilder:
    def __init__(self):
        self.pdf = FPDF()

    def create_table(self, table_data, title='', data_size=10, title_size=12, align_data='L', align_header='L', cell_width='even', x_start='x_default', emphasize_data=[], emphasize_style=None, emphasize_color=(0, 0, 0)):
        default_style = self.pdf.font_style
        if emphasize_style is None:
            emphasize_style = default_style
        # default_font = self.pdf.font_family
        # default_size = self.pdf.font_size_pt
        # default_style = self.pdf.font_style

        def get_col_widths():
            col_width = cell_width
            if col_width == 'even':
                col_width = self.pdf.w / len(data[0]) - 1
            elif col_width == 'uneven':
                col_widths = []

                for col in range(len(table_data[0])):
                    longest = 0
                    for row in range(len(table_data)):
                        cell_value = str(table_data[row][col])
                        value_length = self.pdf.get_string_width(cell_value)
                        if value_length > longest:
                            longest = value_length
                    col_widths.append(longest + 4)
                col_width = col_widths

            elif isinstance(cell_width, list):
                col_width = cell_width
            else:
                            col_width = int(col_width)
                        return col_width

                    if isinstance(table_data, dict):
                        header = [key for key in table_data]
                        data = []
                        for key in table_data:
                            value = table_data[key]
                            data.append(value)

                        data = [list(a) for a in zip(*data)]

                    else:
                        header = table_data[0]
                        data = table_data[1:]

                    line_height = self.pdf.font_size * 2.5

                    col_width = get_col_widths()
                    # self.pdf.set_font(family="", size=title_size)
                    self.pdf.set_font(family="Times", size=title_size)

                    if x_start == 'C':
                        table_width = 0
                        if isinstance(col_width, list):
                            for width in col_width:
                                table_width += width
                        else:
                            table_width = col_width * len(table_data[0])

                        margin_width = self.pdf.w - table_width

                        center_table = margin_width / 2
                        x_start = center_table
                        self.pdf.set_x(x_start)

                        if isinstance(x_start, float):
                            # calculate x_start based on center_table and margin_width
                            margin_width = self.pdf.w - table_width
                            center_table = margin_width / 2
                            x_start = center_table + x_start * margin_width
                            self.pdf.set_x(x_start)
                        elif isinstance(x_start, int):
                            self.pdf.set_x(x_start)
                        elif x_start == 'x_default':
                            x_start = self.pdf.set_x(self.pdf.l_margin)

                        if title != '':
                            self.pdf.multi_cell(0, line_height, title, border=0, align='j')
                            self.pdf.ln(line_height)

                        self.pdf.set_font(family="Times", size=data_size)

                        y1 = self.pdf.get_y()
                        if x_start:
                            x_left = x_start
                        else:
                            x_left = self.pdf.get_x()
                        x_right = self.pdf.epw + x_left
                        if not isinstance(col_width, list):
                            if x_start:
                                self.pdf.set_x(x_start)
                            for datum in header:
                                self.pdf.multi_cell(col_width, line_height, datum, border=0, align=align_header)
                                x_right = self.pdf.get_x()
                            self.pdf.ln(line_height)
                            y2 = self.pdf.get_y()
                            self.pdf.line(x_left, y1, x_right, y1)
                            self.pdf.line(x_left, y2, x_right, y2)

                            for row in data:
                                if x_start:
                                    self.pdf.set_x(x_start)
                                for datum in row:
                                    if datum in emphasize_data:
                                        self.pdf.set_text_color(*emphasize_color)
                                        self.pdf.set_font(family="Times", style=emphasize_style)
                                        self.pdf.multi_cell(col_width, line_height, datum, border=0, align=align_data)
                                        self.pdf.set_text_color(0, 0, 0)
                                        self.pdf.set_font(family="Times", style=default_style)
                                    else:
                                        self.pdf.multi_cell(col_width, line_height, datum, border=0, align=align_data)
                                self.pdf.ln(line_height)

                        else:
                            if x_start:
                                self.pdf.set_x(x_start)
                            for i in range(len(header)):
                                datum = header[i]
                                self.pdf.multi_cell(col_width[i], line_height, datum, border=0, align=align_header)
                                x_right = self.pdf.get_x()
                            self.pdf.ln(line_height)
                            y2 = self.pdf.get_y()
                            self.pdf.line(x_left, y1, x_right, y1)
                            self.pdf.line(x_left, y2, x_right, y2)

                            for i in range(len(data)):
                                if x_start:
                                    self.pdf.set_x(x_start)
                                row = data[i]
                                for i in range(len(row)):
                                    datum = row[i]
                                    if not isinstance(datum, str):
                                        datum = str(datum)
                                    adjusted_col_width = col_width[i]
                                    if datum in emphasize_data:
                                        self.pdf.set_text_color(*emphasize_color)
                                        self.pdf.set_font(family="Times", style=emphasize_style)
                                        self.pdf.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data)
                                        self.pdf.set_text_color(0, 0, 0)
                                        self.pdf.set_font(family="Times", style=default_style)
                                    else:
                                        self.pdf.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data)
                                self.pdf.ln(line_height)
                        y3 = self.pdf.get_y()
                        self.pdf.line(x_left, y3, x_right, y3)

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
