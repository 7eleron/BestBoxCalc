def save_xml(namefiel, data):
    try:
        with open(f"{namefiel}.txt", "w") as file:
            file.write(data)
        print('Done')
    except Exception as e:
        return f'Error: {e}'
