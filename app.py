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

    def create_from(self, element):
        self.tab2_layout
        if element == "Car":

            # Create the form layout
            row1 = QHBoxLayout()
            row2 = QHBoxLayout()
            row3 = QHBoxLayout()

            # Create the Label and input fields for row 1
            vId_lbl = QLabel("Vehicle ID:")
            self.vehicle_id = QLineEdit(self)
            model_lbl = QLabel("Model:")
            self.model = QComboBox(self)
            self.model.addItems(["BMW", "Audi", "Mercedes, Benz"])

            # Add the widgets to row 1
            row1.addWidget(vId_lbl)
            row1.addWidget(self.vehicle_id)
            row1.addWidget(model_lbl)
            row1.addWidget(self.model)

            # Create the Label and input fields for row 2
            price_lbl = QLabel("Price:")
            self.price = QLineEdit(self)
            color_lbl = QLabel("Color:")
            self.color = QComboBox(self)
            self.color.addItems(["Red", "Blue", "Green, Yellow"])
            
            # Add the widgets to row 2
            row2.addWidget(price_lbl)
            row2.addWidget(self.price)
            row2.addWidget(color_lbl)
            row2.addWidget(self.color)

            # Create the Label and input fields for row 3
            numbers_lbl = QLabel("Numbers:")
            self.numbers = QLineEdit(self)
            self.numbers.setMaxLength(4)
            letters_lbl = QLabel("Letters:")
            self.letters = QLineEdit(self)
            self.letters.setMaxLength(4)

            # Add the widgets to row 3
            row3.addWidget(numbers_lbl)
            row3.addWidget(self.numbers)
            row3.addWidget(letters_lbl)
            row3.addWidget(self.letters)

            # Add the rows to the tab layout
            self.form_layout.addLayout(row1)
            self.form_layout.addLayout(row2)
            self.form_layout.addLayout(row3)
            


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
