import asyncio
import re
from blabel import LabelWriter

import requests
import json
import csv

msa_token = ""
msa_dir_id = ""
msa_base_url = "https://tenant.myschoolapp.com"
jamf_gen_groups = ["Class of 2023", "Class of 2024", "Class of 2025", "Class of 2026", "Class of 2027", "Class of 2028"]
file = "jamf.csv"

class MsaUser:
    def __init__(self, name: str) -> None:
        self.name: str | None = name
        self.state: str | None = None
        self.grad_year: int | None = None
        self.grade: int | None = None
        # a bit wacky
        self._make_request()

    def _make_request(self) -> None:

        cookies = {
           't': msa_token,
        }

        # most of this is probably unnecessary, but it's here for safety.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        params = {
            'directoryId': msa_dir_id,
            'searchVal': self.name,
            'facets': '',
            'searchAll': 'true',
        }

        response = requests.get(msa_base_url + '/api/directory/directoryfacetvaluesget',
                                params=params, cookies=cookies, headers=headers)
        if response.status_code == 404:
            return
        if response.status_code == 403:
            raise PermissionError
        jason = json.loads(response.text)
        if len(jason) > 3:
            raise IndexError

        try:
            self.state = jason[0]["FacetValue"]
            self.grad_year = jason[1]["FacetValue"]
            self.grade = jason[2]["FacetValue"]
        # Admittedly, this is a bit of a hack.
        except:
            print(self.name)
            print(jason)


def main():
    """
    Scrapes information from a jamf device spreadsheet.
    :return:
    """
    labels = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)
            serial = row[0]
            name = row[1]
            # doesn't work quite how i want so I have this redundant code.
            re.sub(r'[ \- ]([\s\S]*)$|(full_name)', '', name)
            if name == "full_name":
                continue

            print(serial, name)
            # if serial or name is None:
            #     print("fail sn/nm")
            #     continue
            if len(serial) != 12:
                print("fail sn len")
                continue
            if len(name) == 0:
                print("fail nm len")
                continue
            print("pass")

            if not any(elm in row[2] for elm in jamf_gen_groups):
                continue

            user = MsaUser(name)

            labels.append(
                {
                    "name": name,
                    "serial": serial,
                    "grade": user.grade,
                    "grad_year": user.grad_year,
                    "state": user.state
                }
            )

        label_writer = LabelWriter("item_template.html",
                                   default_stylesheets=("style.css",),
                                   items_per_page=30)
        label_writer.write_labels(labels, target="MSA_Device_labels.pdf")


def test_template():
    label_writer = LabelWriter("item_template.html",
                               default_stylesheets=("style.css",),
                               items_per_page=30)
    labels = [
        {
            "name": "John Doe",
            "serial": "F9FG48QXQ1GG",
            "grade": "10",
            "grad_year": "2024",
            "state": "VA"
        },
        {
            "name": "Dohn Joe",
            "serial": "91357846",
            "grade": "11",
            "grad_year": "1992",
            "state": "MD"
        },
        {
            "name": "GladOS",
            "serial": "R0B0T",
            "grade": "100",
            "grad_year": "-20",
            "state": "IDK"
        },
        {
            "name": "Ben Dover",
            "serial": "XAW12345678",
            "grade": "2",
            "state": "lost"
        }

    ]
    label_writer.write_labels(labels, target="MSA_Device_label_test.pdf")


if __name__ == "__main__":
    main()
