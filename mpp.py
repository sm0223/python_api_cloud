from dataclasses import dataclass, field
from typing import Optional
from xsdata.formats.dataclass.parsers import XmlParser, JsonParser
from generated.mpp import (
    Mpp,
)
import json
data = """
{
    "Application": {
        "Applicant": [
            {
            "Name":"Shubham",
            "Salary" : 10000
            
            }
        ]
    }
} 
"""

xml_parser = XmlParser()
json_parser = JsonParser()


mpp = json_parser.from_string(data, Mpp)
mpp.reference = "success"

# if mpp.application.array_of_applicant[0].applicant.name.upper() == "SHUBHAM":
mpp.application.applicant[0].salary = 2 * mpp.application.applicant[0].salary;

mpp.application.application_number = 123
print(mpp)


