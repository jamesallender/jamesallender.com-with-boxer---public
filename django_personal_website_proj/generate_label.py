import os

import qrcode
import xlsxwriter
from django.http import HttpResponse
from wsgiref.util import FileWrapper


def make_label(file_path, box_qr_val, box_num, box_dest, content, box_id, box_warnings):

    print(f"where tf are we? {os.getcwd()}")

    print(f"file_path: {file_path}")
    print(f"box_qr_val: {box_qr_val}")
    print(f"box_num: {box_num}")
    print(f"box_dest: {box_dest}")
    print(f"content: {content}")
    print(f"box_id: {box_id}")
    print(f"box_warnings: {box_warnings}")

    temp_location = './temp'
    images_location = './images'

    # make list from contents. will be separated on commas
    content_list = []
    if content:
        content = content.replace(", ", ",")
        content_list = content.split(',')
        if len(content_list) > 14:
            print(f"Truncating content to 14 items from {content} to {', '.join(content_list)}")
            content_list = content_list[:14]

    print(f"content_list: {content_list}")

    # make list from box_warnings. will be separated on commas
    box_warnings_list = []
    if box_warnings:
        box_warnings = box_warnings.replace(", ", ",")
        box_warnings_list = box_warnings.split(',')
        if len(box_warnings_list) > 3:
            print(f"Truncating box_warnings to 3 items from {box_warnings} to {', '.join(box_warnings_list)}")
            content_list = content_list[:3]
    print(f"box_warnings_list: {box_warnings_list}")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=3,
        border=2,
    )

    qr.add_data(box_qr_val)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(f"{temp_location}/qr.png")

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()
    worksheet.set_landscape()
    worksheet.set_margins(left=0, right=0, top=0, bottom=0)

    # Create formats
    contents_cell_format = workbook.add_format()
    contents_cell_format.set_font_size(20)

    box_num_format = workbook.add_format()
    box_num_format.set_font_size(200)
    box_num_format.set_align('left')
    box_num_format.set_align('bottom')

    box_id_format = workbook.add_format()
    box_id_format.set_font_size(17)
    box_id_format.set_text_wrap()

    box_dest_format = workbook.add_format()
    box_dest_format.set_font_size(45)


    # Set Column Widths
    worksheet.set_column('A:A', 3.83)
    worksheet.set_column('B:B', 31.50)
    worksheet.set_column('C:C', 5.00)
    worksheet.set_column('D:D', 18.33)
    worksheet.set_column('E:E', 4.00)
    worksheet.set_column('F:F', 31.50)
    worksheet.set_column('G:G', 5.00)
    worksheet.set_column('H:H', 18.33)
    worksheet.set_column('I:I', 2.50)

    # Set Row Heights
    worksheet.set_row(0, 20)
    worksheet.set_row(1, 150, box_num_format)
    worksheet.set_row(2, 45, box_id_format)
    worksheet.set_row(3, 52, box_dest_format)
    worksheet.set_row(4, 25, contents_cell_format)
    worksheet.set_row(5, 25, contents_cell_format)
    worksheet.set_row(6, 25, contents_cell_format)
    worksheet.set_row(7, 25, contents_cell_format)
    worksheet.set_row(8, 25, contents_cell_format)
    worksheet.set_row(9, 25, contents_cell_format)
    worksheet.set_row(10, 25, contents_cell_format)
    worksheet.set_row(11, 25, contents_cell_format)
    worksheet.set_row(12, 25, contents_cell_format)
    worksheet.set_row(13, 25, contents_cell_format)
    worksheet.set_row(14, 25, contents_cell_format)
    worksheet.set_row(15, 25, contents_cell_format)
    worksheet.set_row(16, 25, contents_cell_format)
    worksheet.set_row(17, 25, contents_cell_format)
    worksheet.set_row(18, 25, contents_cell_format)

    # Fill box num lines
    worksheet.merge_range('A2:C3', box_num)
    worksheet.merge_range('E2:G3', box_num)

    # Fill Destination lines
    worksheet.merge_range('B4:D4', box_dest.title())
    worksheet.merge_range('F4:H4', box_dest.title())

    # Insert qr codes
    worksheet.insert_image('C2', f"{temp_location}/qr.png", {'x_scale': 1.15, 'y_scale': 1.30})
    worksheet.insert_image('G2', f"{temp_location}/qr.png", {'x_scale': 1.15, 'y_scale': 1.30})

    # Insert Warnings in first label
    warning_sym_start_row = 5
    for warning in box_warnings_list:
        warning_file = f"{images_location}/{warning}.png"
        if os.path.exists(warning_file):
            worksheet.insert_image(F"D{warning_sym_start_row}", warning_file, {'x_scale': 0.9, 'y_scale': 0.9})
            worksheet.insert_image(F"H{warning_sym_start_row}", warning_file, {'x_scale': 0.9, 'y_scale': 0.9})
            warning_sym_start_row += 4
        else:
            raise ValueError(f"Warning label file {warning_file} was missing from the system")

    # Fill in box id;s
    worksheet.write('D3', f"Box ID: {box_id}")
    worksheet.write('H3', f"Box ID: {box_id}")

    # Fill in contents
    content_line = 5
    for item in content_list:
        worksheet.write(f"B{content_line}", f"{item.title()}")
        worksheet.write(f"F{content_line}", f"{item.title()}")
        content_line += 1

    workbook.close()


def download_box_label(box_qr_val, box_num, box_dest, content, box_id, box_warnings):
    """
    e.g.: file_path = '/tmp/file.pdf'
    """
    file_name = f"box_{box_num}_label.xlsx"
    file_path = f"./temp/{file_name}"

    if os.path.exists(file_path):
        print(f"warning {file_path} exists, it will be overwritten")

    make_label(file_path, box_qr_val, box_num, box_dest, content, box_id, box_warnings)

    try:
        wrapper = FileWrapper(open(file_path, 'rb'))
        response = HttpResponse(wrapper,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
    except Exception as e:
        print(repr(e))
        return None
