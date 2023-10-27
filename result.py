import PyPDF2
import statistics
import csv
from datetime import datetime, timedelta

try:
    pdf_file_path = input("Enter the PDF file path: ")

    if pdf_file_path:
        result = 0
        nordpool_values = []

        with open(pdf_file_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            first_page = pdf_reader.pages[0]
            second_page = pdf_reader.pages[1]
            text_first_page = first_page.extract_text()
            text_second_page = second_page.extract_text()

            charge_start = text_first_page.find("Apmaksai")
            charge_end = text_first_page.find("Elektroenerģijas patēriņš")
            consumption_start = text_first_page.find("Elektroenerģijas patēriņš")
            consumption_end = text_first_page.find("Veicot")

            text_first_page = text_first_page.replace(',', '.')
            text_second_page = text_second_page.replace(',', '.')

            total_charge = float(text_first_page[charge_start + 10:charge_end].strip())
            consumption_quantity = float(text_first_page[consumption_start + 31:consumption_end].strip().replace(' ', '').replace('kWh', ''))

            time_frame_start = text_second_page.find("Apjoms")
            time_frame = text_second_page[time_frame_start - 23:time_frame_start].strip()
            start_date_str, end_date_str = time_frame.split(" - ")
            date_format = "%d.%m.%Y"
            start_date = datetime.strptime(start_date_str, date_format)
            end_date = datetime.strptime(end_date_str, date_format) + timedelta(days=1)

            price_kwh_start = text_second_page.find('kWh')
            price_per_kwh = float(text_second_page[price_kwh_start + 3:price_kwh_start + 10].strip())

        with open("nordpool.csv", "r") as nordpool_csv:
            nordpool_reader = csv.reader(nordpool_csv)
            next(nordpool_reader)
            for row in nordpool_reader:
                start_time, end_time, value = row
                value_date = datetime.strptime(start_time, date_format)
                if start_date <= value_date <= end_date:
                    nordpool_values.append(float(value))

        nordpool_average = statistics.mean(nordpool_values)

        if consumption_quantity != 0:
            nordpool_total = consumption_quantity * round(nordpool_average, 3)
            current_total = consumption_quantity * price_per_kwh
            result = round(current_total - nordpool_total, 1)

        print(result)
    else:
        print("PDF file path not provided.")
except Exception as e:
    print(0)
