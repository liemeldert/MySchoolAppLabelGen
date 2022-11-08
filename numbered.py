from blabel import LabelWriter

def main():
    label_writer = LabelWriter("item_template.html",
                               default_stylesheets=("style.css",),
                               items_per_page=30)
    serials1 = ["C1MTW1REJ1WK", "C1MTW8M2J1WK", "C1MQ24VZG943", "C1MTW8PBJ1WK", "C1MTW8P4J1WK"]
    serials2 = ["C02RQFG7H3QD", "C1MWR9B5JQWK", "C1MTVGLEJ1WK", "C1MQ24VFG943", "C1MTW8PGJ1WK"]
    labels = []
    for index, each in enumerate(serials1):
        labels.append(
        {
            "name": "ESS-" + index,
            "serial": each,
            "grad_year": "CART-ESS-GR1",
        })
    for index, each in enumerate(serials2):
        labels.append(
        {
            "name": "ESS-" + index,
            "serial": each,
            "grad_year": "CART-ESS-GR2",
        })
    label_writer.write_labels(labels, target="numbered.pdf")


if __name__ == "__main__":
    main()
