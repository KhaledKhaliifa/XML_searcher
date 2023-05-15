import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QTabWidget, QComboBox, QLabel,QDateEdit,  QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QDate
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
        tab3 = QWidget()
        tab4 = QWidget()
        tab5 = QWidget()

        # Create form Layout
        self.car_form_layout = None

        # Create the Layout for the Query Tab
        tab1_layout = QVBoxLayout()

        #Create the Layout for the Add Cars Tab
        self.tab2_layout = QVBoxLayout()

        #Create the Layout for the Add Cars Tab
        self.tab3_layout = QVBoxLayout()

        #Create the layout for the Add Salesperson Tab
        self.tab4_layout = QVBoxLayout()

        #Create the layout for the Add Technician Tab
        self.tab5_layout = QVBoxLayout()


        # Add Query Tab to tbe tab widget
        tab1.setLayout(tab1_layout)
        tab_widget.addTab(tab1, "Query")

        # Add the second tab to the tab widget
        tab2.setLayout(self.tab2_layout)
        tab_widget.addTab(tab2, "Add Cars")

        # Add the third tab to the tab widget
        tab3.setLayout(self.tab3_layout)
        tab_widget.addTab(tab3, "Add Contracts")

        # Add the fourth tab to the tab widget
        tab4.setLayout(self.tab4_layout)
        tab_widget.addTab(tab4, "Add Salesperson")

        # ADd the fifth tab to the tab widget
        tab5.setLayout(self.tab5_layout)
        tab_widget.addTab(tab5, "Add Technician")

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
        # Add a layout for the form elements
        self.car_form_layout =QVBoxLayout()
        spacer_item = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.tab2_layout.addLayout(self.car_form_layout)
        self.tab2_layout.addItem(spacer_item)
        self.create_car_form()

        #TAB 3 ITEMS
        # Add a layout for the form elements
        self.contract_form_layout =QVBoxLayout()
        self.tab3_layout.addLayout(self.contract_form_layout)
        # self.tab3_layout.addItem(spacer_item1)
        self.create_contract_form()
        self.tab3_layout.addStretch(1)

        #TAB 4 ITEMS
        # Add a layout for the form elements
        self.salesperson_form_layout =QVBoxLayout()
        self.tab4_layout.addLayout(self.salesperson_form_layout)
        # self.tab4_layout.addItem(spacer_item2)
        self.create_salesperson_form()
        self.tab4_layout.addStretch(1)


        #TAB 5 ITEMS
        # Add a layout for the form elements
        self.technician_form_layout =QVBoxLayout()
        self.tab5_layout.addLayout(self.technician_form_layout)
        # self.tab5_layout.addItem(spacer_item4)
        self.create_technician_form()
        self.tab5_layout.addStretch(1)
    

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

    def create_car_form(self):

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
        self.car_form_layout.addLayout(row1)
        self.car_form_layout.addLayout(row2)
        self.car_form_layout.addLayout(row3)
        self.car_form_layout.addLayout(row4)

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

            if(price.replace(" ","") == "" or numbers.replace(" ","") == "" or letters.replace(" ","") == "" or (odometer.replace(" ","") == "" and self.type.currentText()=="used") or year.replace(" ","") == ""):
                QMessageBox.warning(self, "Warning", "All fields are required!")
                return

            # Load the XML file
            xml_file = './XML/database.xml'
            tree = etree.parse(xml_file)
            # Find the <cars> element
            cars_element = tree.find('.//cars')

            # Create the new <car> element
            car_element = etree.Element('car')

            # Create child elements and set their values
            contract_no_element = etree.SubElement(car_element, 'vehicle_id')
            contract_no_element.text = str(vehicle_id)
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

    def create_contract_form(self):
        row1 = QHBoxLayout()
        contract_date_lbl = QLabel("Contract Date:")
        self.contract_date = QDateEdit(self)
        self.contract_date.setDate(QDate.currentDate())
        row1.addWidget(contract_date_lbl)
        row1.addWidget(self.contract_date)
        payment_info_lbl = QLabel("Payment Info:")
        self.payment_info = QComboBox(self)
        self.payment_info.addItems(["Cash", "Credit"])
        row1.addWidget(payment_info_lbl)
        row1.addWidget(self.payment_info)
        row2 = QHBoxLayout()
        service_lbl = QLabel("Service:")
        service_price_lbl = QLabel("Price:")
        self.service_price=QLineEdit(self)
        service_name_lbl = QLabel("Name:")
        self.service_name = QLineEdit(self)
        row2.addWidget(service_name_lbl)
        row2.addWidget(self.service_name)
        row2.addWidget(service_price_lbl)
        row2.addWidget(self.service_price)
        customer_lbl= QLabel("Customer:")
        row3 = QHBoxLayout()
        customer_fname_lbl = QLabel("First Name:")
        self.customer_fname = QLineEdit(self)
        customer_lname_lbl = QLabel("Last Name:")
        self.customer_lname = QLineEdit(self)
        phone_no_lbl = QLabel("Phone No:")
        self.phone_no = QLineEdit(self)
        row3.addWidget(customer_fname_lbl)
        row3.addWidget(self.customer_fname)
        row3.addWidget(customer_lname_lbl)
        row3.addWidget(self.customer_lname)
        row3.addWidget(phone_no_lbl)
        row3.addWidget(self.phone_no)
        insert_button = QPushButton("Insert", self)
        insert_button.clicked.connect(self.insert_contract)
        

        
        self.tab3_layout.addLayout(row1)
        self.tab3_layout.addWidget(service_lbl)
        self.tab3_layout.addLayout(row2)
        self.tab3_layout.addWidget(customer_lbl)
        self.tab3_layout.addLayout(row3)
        self.tab3_layout.addWidget(insert_button)

    def create_salesperson_form(self):
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        firstName_lbl = QLabel("First Name:")
        self.sales_firstName = QLineEdit(self)
        lastName_lbl = QLabel("Last Name:")
        self.sales_lastName = QLineEdit(self)

        address_lbl = QLabel("Address:")
        self.sales_address_widget = QLineEdit(self)

        phone_no_lbl = QLabel("Phone No:")
        self.sales_phone_no = QLineEdit(self)

        salary_lbl = QLabel("Salary:")
        self.sales_salary_widget = QLineEdit(self)

        sex_lbl = QLabel("Sex:")
        self.sales_sex_widget = QComboBox(self)
        self.sales_sex_widget.addItems(["M", "F"])

        sales_lbl = QLabel("Sales:")
        self.sales = QLineEdit(self)

        row1.addWidget(firstName_lbl)
        row1.addWidget(self.sales_firstName)
        row1.addWidget(lastName_lbl)
        row1.addWidget(self.sales_lastName)

        row2.addWidget(address_lbl)
        row2.addWidget(self.sales_address_widget)
        row2.addWidget(phone_no_lbl)
        row2.addWidget(self.sales_phone_no)

        row3.addWidget(salary_lbl)
        row3.addWidget(self.sales_salary_widget)
        row3.addWidget(sex_lbl)
        row3.addWidget(self.sales_sex_widget)
        row3.addWidget(sales_lbl)
        row3.addWidget(self.sales)

        sales_insert_button = QPushButton("Insert", self)
        sales_insert_button.clicked.connect(self.insert_salesperson)
        self.tab4_layout.addLayout(row1)
        self.tab4_layout.addLayout(row2)
        self.tab4_layout.addLayout(row3)
        self.tab4_layout.addWidget(sales_insert_button)

    def create_technician_form(self):
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        firstName_lbl = QLabel("First Name:")
        self.tech_firstName = QLineEdit(self)
        lastName_lbl = QLabel("Last Name:")
        self.tech_lastName = QLineEdit(self)

        address_lbl = QLabel("Address:")
        self.tech_address = QLineEdit(self)

        phone_no_lbl = QLabel("Phone No:")
        self.technician_phone = QLineEdit(self)

        salary_lbl = QLabel("Salary:")
        self.techs_salary = QLineEdit(self)

        sex_lbl = QLabel("Sex:")
        self.tech_sex = QComboBox(self)
        self.tech_sex.addItems(["M", "F"])

        specialization_lbl = QLabel("Specialization:")
        self.specialization = QComboBox(self)
        self.specialization.addItems(["electrician", "mechanic"])

        row1.addWidget(firstName_lbl)
        row1.addWidget(self.tech_firstName)
        row1.addWidget(lastName_lbl)
        row1.addWidget(self.tech_lastName)

        row2.addWidget(address_lbl)
        row2.addWidget(self.tech_address)
        row2.addWidget(phone_no_lbl)
        row2.addWidget(self.technician_phone)

        row3.addWidget(salary_lbl)
        row3.addWidget(self.techs_salary)
        row3.addWidget(sex_lbl)
        row3.addWidget(self.tech_sex)
        row3.addWidget(specialization_lbl)
        row3.addWidget(self.specialization)


        tech_insert_button = QPushButton("Insert", self)
        tech_insert_button.clicked.connect(self.insert_technician)
        self.tab5_layout.addLayout(row1)
        self.tab5_layout.addLayout(row2)
        self.tab5_layout.addLayout(row3)
        self.tab5_layout.addWidget(tech_insert_button)
    
    def return_max_contract_id(self):
            xml_file = "./XML/database.xml"
            tree = etree.parse(xml_file)
            xpath_query = '//contracts/contract/contract_no/text()'
            contract_nos = tree.xpath(xpath_query)
            max_contract_no = max(map(int, contract_nos))
            return max_contract_no
    
    def return_max_service_id(self):
            xml_file = "./XML/database.xml"
            tree = etree.parse(xml_file)
            xpath_query = '//contracts/contract/service/service_no/text()'
            service_nos = tree.xpath(xpath_query)
            max_service_no = max(map(int, service_nos))
            return max_service_no
    
    def return_max_customer_id(self):
            xml_file = "./XML/database.xml"
            tree = etree.parse(xml_file)
            xpath_query = '//contracts/contract/customer/customer_id/text()'
            customer_ids = tree.xpath(xpath_query)
            max_customer_id = max(map(int, customer_ids))
            return max_customer_id
    
    def return_max_employee_id(self):
            xml_file = "./XML/database.xml"
            tree = etree.parse(xml_file)
            xpath_query_salesperson = '//employees/salesperson/emp_id/text()'
            xpath_query_technician = '//employees/technician/emp_id/text()'
            
            salesperson_ids = tree.xpath(xpath_query_salesperson)
            technician_ids = tree.xpath(xpath_query_technician)
            max_salesperson_id = max(map(int, salesperson_ids))
            max_technician_id = max(map(int, technician_ids))

            if(max_salesperson_id > max_technician_id):
                return max_salesperson_id
            else:
                return max_technician_id
    def insert_technician(self):
        tech_emp_id = self.return_max_employee_id() + 1
        tech_fname = self.tech_firstName.text()
        tech_lname = self.tech_lastName.text()
        tech_phone_no = self.technician_phone.text()
        tech_salary = self.techs_salary.text()
        tech_address = self.tech_address.text()
        tech_spec = self.specialization.currentText()
        tech_sex = self.tech_sex.currentText()
        if(tech_fname.replace(" ", "") == "" or
           tech_lname.replace(" ", "") == "" or tech_phone_no.replace(" ", "") == "" or
           tech_salary.replace(" ", "") == "" or tech_address.replace(" ", "") == "" or
           tech_spec.replace(" ", "") == "" or tech_sex.replace(" ", "") == ""):
            QMessageBox.warning(self, "Warning", "All fields are required!")
            return
        
        xml_file = "./XML/database.xml"
        tree = etree.parse(xml_file)
        employee = tree.find(".//employees")
        technician = etree.Element("technician")      
        technician.set("emp_id", str(tech_emp_id))
        technician.set("fname", tech_fname)
        technician.set("lname", tech_lname)
        technician.set("phone_no", tech_phone_no)
        technician.set("salary", tech_salary)
        technician.set("address", tech_address)
        technician.set("specialization", tech_spec)
        technician.set("sex", tech_sex)

        employee.append(technician)
        tree.write(xml_file)

    def insert_salesperson(self):
        sales_emp_id = self.return_max_employee_id() + 1
        sales_fname = self.sales_firstName.text()
        sales_lname = self.sales_lastName.text()
        sales_phone = self.sales_phone_no.text()
        sales_salary = self.sales_salary_widget.text()
        sales_address = self.sales_address_widget.text()
        sales_sales = self.sales.text()
        sales_sex = self.sales_sex_widget.currentText()

        if(sales_fname.replace(" ", "") == "" or 
           sales_lname.replace(" ", "") == "" or sales_phone.replace(" ", "") == "" or 
           sales_salary.replace(" ", "") == "" or sales_address.replace(" ", "") == "" or 
           sales_sales.replace(" ", "") == ""):
            QMessageBox.warning(self, "Warning", "All fields are required!")
            return

        xml_file = "./XML/database.xml"
        tree = etree.parse(xml_file)
        employee = tree.find(".//employees")
        salesperson = etree.Element("salesperson")
        salesperson.set("emp_id", str(sales_emp_id))
        salesperson.set("fname", sales_fname)
        salesperson.set("lname", sales_lname)
        salesperson.set("phone_no", sales_phone)
        salesperson.set("salary", sales_salary)
        salesperson.set("address", sales_address)
        salesperson.set("sales", sales_sales)
        salesperson.set("sex", sales_sex)

        employee.append(salesperson)
        tree.write(xml_file)

    def insert_contract(self):
        contract_no = self.return_max_contract_id() + 1
        cdate = self.contract_date.text()
        payment = self.payment_info.currentText()
        service_no = self.return_max_service_id() + 1
        service_price = self.service_price.text()
        service_name = self.service_name.text()
        customer_id = self.return_max_customer_id() + 1
        customer_fname = self.customer_fname.text()
        customer_lname = self.customer_lname.text()
        customer_phone = self.phone_no.text()

        if(payment.replace(" ", "") == "" or service_price.replace(" ", "") == "" or service_name.replace(" ", "") == "" 
           or customer_fname.replace(" ", "") == "" or customer_lname.replace(" ", "") == "" or customer_phone.replace(" ", "") == ""):
            QMessageBox.warning(self, "Warning", "All fields are required!")
            return

        # Load the XML file
        xml_file = './XML/database.xml'
        tree = etree.parse(xml_file)
        # Find the <contracts> element
        contracts_element = tree.find('.//contracts')

        # Create the new <contract> element
        contract_element = etree.Element('contract')

        # Create child elements and set their values
        contract_no_element = etree.SubElement(contract_element, 'contract_no')
        contract_no_element.text = str(contract_no)
        cdate_element = etree.SubElement(contract_element, 'cdate')
        cdate_element.text = str(cdate)
        payment_info_element = etree.SubElement(contract_element, 'payment_info')
        payment_info_element.text = str(payment)
        service_element = etree.SubElement(contract_element, 'service')
        service_no_element = etree.SubElement(service_element, 'service_no')
        service_no_element.text = str(service_no)
        service_price_element = etree.SubElement(service_element, 'price')
        service_price_element.text = str(service_price)
        service_name_element = etree.SubElement(service_element, 'name')
        service_name_element.text = str(service_name)
        customer_element = etree.SubElement(contract_element, 'customer')
        customer_id_element = etree.SubElement(customer_element, 'customer_id')
        customer_id_element.text = str(customer_id)
        customer_fname_element = etree.SubElement(customer_element, 'firstname')
        customer_fname_element.text = str(customer_fname)
        customer_lname_element = etree.SubElement(customer_element, 'lastname')
        customer_lname_element.text = str(customer_lname)
        customer_phone_element = etree.SubElement(customer_element, 'phone_no')
        customer_phone_element.text = str(customer_phone)

                    
        # Append the new <contract> element to the <cars> element
        contracts_element.append(contract_element)

        # Save the modified XML file
        tree.write(xml_file, pretty_print=True)

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
