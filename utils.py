def print_table(data, headers):
    print("\n" + "-"*50)
    print(" | ".join(headers))
    print("-"*50)
    for row in data:
        print(" | ".join(str(x) for x in row))
    print("-"*50)
