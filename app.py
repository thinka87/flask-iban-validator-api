from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def is_valid_iban(iban):
    # Remove spaces and convert to uppercase
    iban = iban.replace(' ', '').upper()

    # Define IBAN structure for each country (you can extend this list)
    iban_formats = {
    'AD': r'^AD\d{10}[A-Z0-9]{12}$',
    'AE': r'^AE\d{21}$',
    'AL': r'^AL\d{10}[A-Z0-9]{16}$',
    'AT': r'^AT\d{18}$',
    'AZ': r'^AZ\d{2}[A-Z]{4}[A-Z0-9]{20}$',
    'BA': r'^BA\d{18}$',
    'BE': r'^BE\d{14}$',
    'BG': r'^BG\d{2}[A-Z]{4}\d{6}[A-Z0-9]{8}$',
    'BH': r'^BH\d{2}[A-Z]{4}[A-Z0-9]{14}$',
    'BR': r'^BR\d{25}[A-Z0-9]$',
    'BY': r'^BY\d{2}[A-Z0-9]{4}\d{20}$',
    'CH': r'^CH\d{18}$',
    'CR': r'^CR\d{20}$',
    'CY': r'^CY\d{10}[A-Z0-9]{16}$',
    'CZ': r'^CZ\d{20}$',
    'DE': r'^DE\d{20}$',
    'DK': r'^DK\d{18}$',
    'DO': r'^DO\d{28}$',
    'EE': r'^EE\d{18}$',
    'ES': r'^ES\d{22}$',
    'FI': r'^FI\d{18}$',
    'FO': r'^FO\d{18}$',
    'FR': r'^FR\d{12}[A-Z0-9]{11}\d{2}$',
    'GB': r'^GB\d{2}[A-Z]{4}\d{14}$',
    'GE': r'^GE\d{2}[A-Z]{2}\d{16}$',
    'GI': r'^GI\d{2}[A-Z]{4}[A-Z0-9]{15}$',
    'GL': r'^GL\d{18}$',
    'GR': r'^GR\d{27}$',
    'GT': r'^GT\d{2}[A-Z0-9]{24}$',
    'HR': r'^HR\d{19}$',
    'HU': r'^HU\d{26}$',
    'IE': r'^IE\d{22}$',
    'IL': r'^IL\d{21}$',
    'IQ': r'^IQ\d{2}[A-Z]{4}\d{15}$',
    'IS': r'^IS\d{24}$',
    'IT': r'^IT\d{2}[A-Z]\d{10}[A-Z0-9]{12}$',
    'JO': r'^JO\d{2}[A-Z]{4}\d{20}$',
    'KW': r'^KW\d{2}[A-Z]{4}[A-Z0-9]{22}$',
    'KZ': r'^KZ\d{2}[A-Z0-9]{3}\d{13}$',
    'LB': r'^LB\d{6}[A-Z0-9]{20}$',
    'LC': r'^LC\d{2}[A-Z]{4}[A-Z0-9]{24}$',
    'LI': r'^LI\d{20}$',
    'LT': r'^LT\d{18}$',
    'LU': r'^LU\d{20}$',
    'LV': r'^LV\d{2}[A-Z]{4}[A-Z0-9]{13}$',
    'MC': r'^MC\d{12}[A-Z0-9]{11}\d{2}$',
    'MD': r'^MD\d{2}[A-Z0-9]{20}$',
    'ME': r'^ME\d{20}$',
    'MK': r'^MK\d{2}[A-Z0-9]{3}\d{10}[A-Z0-9]{2}$',
    'MR': r'^MR\d{25}$',
    'MT': r'^MT\d{2}[A-Z]{4}\d{5}[A-Z0-9]{18}$',
    'MU': r'^MU\d{2}[A-Z]{4}\d{19}[A-Z]{3}$',
    'NL': r'^NL\d{2}[A-Z]{4}\d{10}$',
    'NO': r'^NO\d{13}$',
    'PK': r'^PK\d{2}[A-Z0-9]{4}\d{16}$',
    'PL': r'^PL\d{26}$',
    'PS': r'^PS\d{2}[A-Z]{4}\d{21}$',
    'PT': r'^PT\d{23}$',
    'QA': r'^QA\d{2}[A-Z]{4}[A-Z0-9]{21}$',
    'RO': r'^RO\d{2}[A-Z]{4}[A-Z0-9]{16}$',
    'RS': r'^RS\d{20}$',
    'SA': r'^SA\d{4}[A-Z0-9]{18}$',
    'SE': r'^SE\d{22}$',
    'SI': r'^SI\d{17}$',
    'SK': r'^SK\d{20}$',
    'SM': r'^SM\d{2}[A-Z]\d{10}[A-Z0-9]{12}$',
    'SV': r'^SV\d{26}$',
    'TL': r'^TL\d{23}$',
    'TN': r'^TN\d{24}$',
    'TR': r'^TR\d{8}[A-Z0-9]{16}$',
    'UA': r'^UA\d{8}[A-Z0-9]{19}$',
    'VA': r'^VA\d{20}$',
    'VG': r'^VG\d{2}[A-Z0-9]{4}\d{16}$',
    'XK': r'^XK\d{18}$',
}


    # Check if the IBAN format is known
    country_code = iban[:2]
    if country_code not in iban_formats:
        return False

    # Check if IBAN matches the expected format
    if not re.match(iban_formats[country_code], iban):
        return False

    # Perform IBAN checksum validation
    iban_digits = iban[4:] + iban[:4]
    iban_digits = ''.join([str(ord(char) - ord('A') + 10) if char.isalpha() else char for char in iban_digits])
    iban_num = int(iban_digits)
    if iban_num % 97 != 1:
        return False

    return True

@app.route('/validate-iban', methods=['POST'])
def validate_iban():
    data = request.get_json()
    iban_number = data.get('iban')

    if not iban_number:
        return jsonify({'error': 'No IBAN provided'}), 400

    if is_valid_iban(iban_number):
        return jsonify({'message': 'Valid IBAN'}), 200
    else:
        return jsonify({'error': 'Invalid IBAN'}), 400

if __name__ == '__main__':
    app.run(debug=True)
