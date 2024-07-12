from PIL import Image


# Функция для вычисления CRC8 с настройками начального и конечного XOR значений
def crc8_adjusted(data, poly, init_crc, final_xor):
    crc = init_crc
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFF
    return crc ^ final_xor

# Функция для обработки изображения и извлечения данных с использованием CRC8
def process_image_to_extract_data(image, poly, init_crc, final_xor):
    pixels = list(image.getdata())
    output_bytes = []
    for pixel in pixels:
        # Преобразование кортежа пикселей в представление int32, RGB хранятся как (R, G, B)
        pixel_value = (pixel[0] << 16) | (pixel[1] << 8) | pixel[2]
        # Вычисление CRC8 для этого значения пикселя
        crc_value = crc8_adjusted(pixel_value.to_bytes(4, byteorder='little'), poly, init_crc, final_xor)
        output_bytes.append(crc_value)

    # Преобразование списка байтов в формат бинарного файла
    return bytes(output_bytes)

# Загрузка файла
image_path = 'I1.png'
decoded_image = Image.open(image_path)

# Использование найденных правильных настроек для CRC8
poly = 0x1D
init_crc = 0xFF
final_xor = 0xFF

# Обработка изображения для извлечения данных
extracted_data = process_image_to_extract_data(decoded_image, poly, init_crc, final_xor)
output_file_path_jpeg = 'Result.jpg'
with open(output_file_path_jpeg, 'wb') as file:
    file.write(extracted_data)

print("Изображение обработано и сохранено в формате JPG.")

# Тестирование расчета CRC8
test_string = 'password'.encode()
expected_crc = 0xCF
calculated_crc = crc8_adjusted(test_string, poly, init_crc, final_xor)

if calculated_crc == expected_crc:
    print("Расчет CRC8 верный.")
else:
    print("Расчет CRC8 неверный. Ожидалось:", expected_crc, ", получено:", calculated_crc)
