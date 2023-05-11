import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
from lxml import etree

class XPathApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XPath App")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Input field for XPath expression
        self.xpath_input = QLineEdit(self)
        layout.addWidget(self.xpath_input)

        # Button to execute XPath query
        self.execute_button = QPushButton("Execute", self)
        self.execute_button.clicked.connect(self.execute_xpath)
        layout.addWidget(self.execute_button)

        # Output text box
        self.output_text = QTextEdit(self)
        layout.addWidget(self.output_text)

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
