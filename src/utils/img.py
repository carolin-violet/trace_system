import qrcode


def make_qrcode(product_id, data):
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)

    qr.make(fit=True)
    img = qr.make_image()
    file_path = '../../static/qr_codes/' + str(product_id) + ".png"
    img.save(file_path)


if __name__ == '__main__':
    make_qrcode('123456', 'hello')