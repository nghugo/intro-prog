import json
import re
class DataValidator:

    @staticmethod
    def validate_country(country_name):
        #load data from country.json
        with open('countries.json', 'r') as file:
            countries = json.load(file)

        for country in countries:
            if country['name'] == country_name:
                return True

        return False


    @staticmethod
    def validate_name(name):
        pattern = r'^[A-Z][a-z]*(\s[A-Z][a-z]*)*$'
        result = bool(re.match(pattern, name)) and len(name)>1
        return result

    @staticmethod
    def validate_date(date):
        #todo: validate date
        pass
