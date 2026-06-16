import base64

def main():
    input_string = input("Enter a string to encrypt: ")
    
    encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    with open("data.txt", "w") as file:
        file.write(encoded_string)

    print("da ma hoa va ghi vao tep data.txt")
if __name__ == "__main__":
    main()