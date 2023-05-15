import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QTabWidget, QComboBox, QLabel
from PyQt5.QtCore import Qt
from lxml import etree

class XPathApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XPath App")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create a tab widget
        tab_widget = QTabWidget(self)

        # Create tabs and add them to the tab widget
        tab1 = QWidget()
        tab2 = QWidget()

        # Create the Layout for the Query Tab
        tab1_layout = QVBoxLayout()

        #Create the Layout for the Add Tab
        self.tab2_layout = QVBoxLayout()

        # Add Query Tab to tbe tab widget
        tab1.setLayout(tab1_layout)
        tab_widget.addTab(tab1, "Query")

        # Add the second tab to the tab widget
        tab2.setLayout(self.tab2_layout)
        tab_widget.addTab(tab2, "Add")


        # TAB 1 ITEMS
        # Input field for XPath expression
        self.xpath_input = QLineEdit(self)
        tab1_layout.addWidget(self.xpath_input)

        # Create a horizontal layout for the query buttons
        query_layout = QHBoxLayout()
        execute_clear_layout = QHBoxLayout()
        
        # Button to execute XPath Query 1
        self.query1_button = QPushButton("Query 1", self)
        self.query1_button.clicked.connect(lambda: self.query_xpath('//cars/car[type/@name="used" and price>20000]/model')) # Choose a suitable XPath expression
        query_layout.addWidget(self.query1_button)

        # Button to execute XPath Query 2
        self.query2_button = QPushButton("Query 2", self)
        self.query2_button.clicked.connect(lambda: self.query_xpath('//contracts/contract[service/price > 100]/service/name')) # Choose a suitable XPath expression
        query_layout.addWidget(self.query2_button)

        # Button to execute XPath Query 3
        self.query3_button = QPushButton("Query 3", self)
        self.query3_button.clicked.connect(lambda: self.query_xpath('//cars/car[substring(type/year, 1, 4)="2019"]/vehicle_id')) # Choose a suitable XPath expression
        query_layout.addWidget(self.query3_button)

         # Add the query button layout to the main layout
        tab1_layout.addLayout(query_layout)

        # Button to execute XPath query
        self.execute_button = QPushButton("Execute", self)
        self.execute_button.clicked.connect(self.execute_xpath)
        execute_clear_layout.addWidget(self.execute_button)

        # Create a button that clears the output text box
        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear_output)
        execute_clear_layout.addWidget(self.clear_button)

        # Add the execute clear layout buttons layout to the main layout
        tab1_layout.addLayout(execute_clear_layout)

        # Output text box
        self.output_text = QTextEdit(self)
        tab1_layout.addWidget(self.output_text)

        # TAB 2 ITEMS
        # Add a Drop down menu with choices
        self.element = QComboBox(self)
        self.element.addItems(["Car", "Contract", "Service","Sales Person", "Technician"])
        self.element.activated[str].connect(self.create_from)

        #Add the menu to Tab 2
        self.tab2_layout.addWidget(self.element)

        # Add a layout for the form elements
        self.form_layout =QVBoxLayout()
        self.tab2_layout.addLayout(self.form_layout)

        # Generate the default Form
        self.create_from(self.element.currentText())

        # Add the tab widget to the main layout
        layout.addWidget(tab_widget)

        self.setLayout(layout)

    def execute_xpath(self):
        try:
            xpath_expression = self.xpath_input.text()

            # Load and parse the XML document
            xml_file = "./XML/database.xml"
            tree = etree.parse(xml_file)
            # Execute the XPath query
            results = tree.xpath(xpath_expression)
            output = f"Found a total of {len(results)} results!\n==================\n\n"
            if(type(results[0]) == etree._ElementUnicodeResult):
                # Format and display the results in the output text box
                for index,result in enumerate(results):
                    output+= f"(Result {index+1})\n"
                    output += "\n" + str(result) + "\n___________________________________\n"
            else:
                for index,result in enumerate(results):
                    output+= f"(Result {index+1})\n\n"
                    output = iterate_results(result,output, 0)
                    output += "___________________________________\n\n"

            self.output_text.setText(output)
        except:
            if(self.xpath_input.text() == ""):
                self.output_text.setText("Please enter an expression")
            else:
                self.output_text.setText("Invalid XPath expression")
    
    def query_xpath(self, xpath_expression):

            # Load and parse the XML document
            xml_file = "./XML/database.xml"
            tree = etree.parse(xml_file)
            # Execute the XPath query
            results = tree.xpath(xpath_expression)
            output = f"Found a total of {len(results)} results!\n==================\n\n"
            if(results):
                if(type(results[0]) == etree._ElementUnicodeResult):
                    # Format and display the results in the output text box
                    for index,result in enumerate(results):
                        output+= f"(Result {index+1})\n"
                        output += "\n" + str(result) + "\n___________________________________\n"
                else:
                    for index,result in enumerate(results):
                        output+= f"(Result {index+1})\n\n"
                        output = iterate_results(result,output, 0)
                        output += "___________________________________\n\n"

            self.output_text.setText(output)
    
    def clear_output(self):
        self.output_text.setText("")

    def type_selected(self, element):
        if(element == "used"):
            self.odometer.setEnabled(True)
        else:
            self.odometer.setEnabled(False)

    def create_from(self, element):
        if(self.form_layout != None):
            self.tab2_layout.removeItem(self.form_layout)
        
        if element == "Car":

            # Create the form layout
            row1 = QHBoxLayout()
            row2 = QHBoxLayout()
            row3 = QHBoxLayout()
            row4 = QHBoxLayout()
            row5 = QHBoxLayout()

            # Create the Label and input fields for row 1
            model_lbl = QLabel("Model:")
            self.model = QComboBox(self)
            self.model.addItems(["BMW", "Audi", "Mercedes, Benz"])

            # Add the widgets to row 1
            row1.addWidget(model_lbl)
            row1.addWidget(self.model)

            # Create the Label and input fields for row 2
            price_lbl = QLabel("Price:")
            self.price = QLineEdit(self)
            color_lbl = QLabel("Color:")
            self.color = QComboBox(self)
            self.color.addItems(["Red", "Blue", "Green", "Yellow"])
            
            # Add the widgets to row 1
            row1.addWidget(price_lbl)
            row1.addWidget(self.price)
            row1.addWidget(color_lbl)
            row1.addWidget(self.color)

            # Create the Label and input fields for row 2
            numbers_lbl = QLabel("Numbers:")
            self.numbers = QLineEdit(self)
            self.numbers.setMaxLength(4)
            letters_lbl = QLabel("Letters:")
            self.letters = QLineEdit(self)
            self.letters.setMaxLength(4)

            # Create the Label and input fields for row 2
            type_lbl = QLabel("Type:")
            self.type = QComboBox(self)
            self.type.addItems(["used", "new"])
            self.type.activated[str].connect(self.type_selected)

            # Add the widgets to row 2
            row2.addWidget(numbers_lbl)
            row2.addWidget(self.numbers)
            row2.addWidget(letters_lbl)
            row2.addWidget(self.letters)
            row2.addWidget(type_lbl)
            row2.addWidget(self.type)

            #Create a label and a widget for year and odometer and add to row3
            year_lbl = QLabel("Year:")
            self.year = QLineEdit(self)
            self.year.setMaxLength(4)
            odometer_lbl = QLabel("Odometer:")
            self.odometer = QLineEdit(self)
            self.odometer.setMaxLength(4)
            row3.addWidget(year_lbl)
            row3.addWidget(self.year)
            row3.addWidget(odometer_lbl)
            row3.addWidget(self.odometer)


            # Add the rows to the tab layout
            self.form_layout.addLayout(row1)
            self.form_layout.addLayout(row2)
            self.form_layout.addLayout(row3)
            self.form_layout.addLayout(row4)

            def return_max_id():
                xml_file = "./XML/database.xml"
                tree = etree.parse(xml_file)
                xpath_query = '//cars/car/vehicle_id/text()'
                vehicle_ids = tree.xpath(xpath_query)
                max_vehicle_id = max(map(int, vehicle_ids))
                return max_vehicle_id
            def insert_cars():
                vehicle_id = return_max_id() + 1
                model = self.model.currentText()
                price = self.price.text()
                color = self.color.currentText()
                numbers = self.numbers.text()
                letters = self.letters.text()
                odometer = self.odometer.text()
                year = self.year.text()

                # Load the XML file
                xml_file = './XML/database.xml'
                tree = etree.parse(xml_file)
                # Find the <cars> element
                cars_element = tree.find('.//cars')

                # Create the new <car> element
                car_element = etree.Element('car')

                # Create child elements and set their values
                vehicle_id_element = etree.SubElement(car_element, 'vehicle_id')
                vehicle_id_element.text = str(vehicle_id)
                type_element = etree.SubElement(car_element, 'type')


                if(self.type.currentText() == "used"):
                    type_element.attrib['name'] = "used"
                    odometer_element = etree.SubElement(type_element, 'odometer')
                    odometer_element.text = odometer

                else:
                    type_element.attrib['name'] = "new"

                year_id_element = etree.SubElement(type_element, 'year')
                year_id_element.text = year

                model_element = etree.SubElement(car_element, 'model')
                model_element.text = model

                price_element = etree.SubElement(car_element, 'price')
                price_element.text = str(price)


                color_element = etree.SubElement(car_element, 'color')
                color_element.text = color

                numbers_element = etree.SubElement(car_element, 'numbers')
                numbers_element.text = str(numbers)

                letters_element = etree.SubElement(car_element, 'letters')
                letters_element.text = str(letters)

                            
                # Append the new <car> element to the <cars> element
                cars_element.append(car_element)

                # Save the modified XML file
                tree.write(xml_file, pretty_print=True)

            self.insert_button = QPushButton("Insert", self)

            self.insert_button.clicked.connect(insert_cars) # Choose a suitable XPath expression
            row4.addWidget(self.insert_button)


        # elif element == "Contract":
            
        # elif element == "Service":
            
        # elif element == "Sales Person":
            
        # elif element == "Technician":
            

def iterate_results(result, output, counter):
    if len(result.getchildren()) == 0:
        if(counter > 1):
            output += "\t"
        output += str(result.tag) + " : \t" + str(result.text)
    else:
        if(counter >0):
            output+= "\n[" + str(result.tag) + "]\n"
        for child in result.getchildren():
            output = iterate_results(child, output, counter+1)
    
    output += '\n'
    return output


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = XPathApp()
    window.resize(550,800)
    window.show()
    sys.exit(app.exec_())
