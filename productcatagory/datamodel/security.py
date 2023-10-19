from werkzeug.security import safe_str_cmp
from productcatagory.datamodel.catagoryConfig import CatagoryValidation

def authenticate(name):
    user = CatagoryValidation.find_by_catagory(name)
    if user and safe_str_cmp(name):
        return user
