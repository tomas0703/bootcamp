from typing import List

import re

from langchain_google_vertexai import VertexAI
import os
from typing import List
from prompt_poet import Prompt
import numpy as np
from typing import List
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
import numpy as np
import os
from typing import List
import matplotlib.pyplot as plt
from langchain_openai import OpenAI
import json
from langchain.output_parsers import OutputFixingParser
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.exceptions import OutputParserException


class Person(BaseModel):
    first_name: str
    age: int
    gender: str
    race: str
    ethnicity: str
    counts: int = Field(default = 1)

class Persons(BaseModel):
    persons: List[Person]



def datagather(
        model,
        profesion,
        place, 
        size):

    parser = PydanticOutputParser(pydantic_object=Person)

    prompt = PromptTemplate.from_template(
        template="""Create details for characters in the book. The character is a {role} in the {place} Create name, age, gender, race and ethnicity. Create at least {batch_size} examples to choose from.
Response as multiple lines, each formatted as JSON with fields: first_name, age, gender, race, ethnicity
        """
    )

    formatted_prompt = prompt.partial(schema = Person.schema())

    chain = formatted_prompt | model #| parser

    persons = []
    
    while len(persons) < size:
        added = 0
        response = chain.invoke({'role': profesion, 'place': place, 'batch_size': 10})
        for line in response.split('\n'):
            try:
                person = parser.invoke(line)
            except OutputParserException:
                pass
            else:
                if person not in persons:
                    added += 1
                    persons.append(person)
                else:
                    idx = persons.index(person)
                    persons[idx].counts += 1
        print(f'Added {added} persons in this round')

    return persons
  

def jsontodata(Data,Words, d):
    # b is the amount of diffrent output classes expressed in a list 
    # for example Words = [race , gender, age , ethnicity] ould be a d of [0,1,2,3]
    for sublst in Words:
        lst = {}
        for item in sublst:
            total = Data.count(item)
            lst.update({item : total})             
        return print(Data), lst 


def num_sim(n1, n2):
  """ calculates a similarity score between 2 numbers """
  return 1 - abs(n1 - n2) / (n1 + n2)

def createList(r1, r2):

 # Testing if range r1 and r2
 # are equal
 if (r1 == r2):
  return r1

 else:

  # Create empty list
  res = []

  # loop to append successors to
  # list until r2 is reached.
  while(r1 < r2+1 ):
   
   res.append(r1)
   r1 += 1
  return res

def datatograth(D):
    plt.bar(range(len(D)), list(D.values()), align='center')
    plt.xticks(range(len(D)), list(D.keys()))
    return plt.show()
def adddatatoreposotory(D):
    with open('/home/ubuntu/full.py', 'w') as fout:
        json.dump(D , fout)


if __name__ == '__main__':
    h = [1,2,3,4]
    MODEL = 'gemini-1.5-flash-001'
    model_kwargs = {
    "max_new_tokens": 8000, 
    "temperature": 2, 
    }
    model = VertexAI(model=MODEL, kwargs= model_kwargs)
   
    ethnicitys =  ["Abruzzi", "Acadian/Cajun", "Aden", "Afghan/Afghanistani", "African", "African American", "African Islands", "Afrikaner", "Afro", "Afro-American", "Agikuyu/Kikuyu", "Akan", "Alabama", "Aland Islander", "Alaska", "Alaska Athabascan", "Alaska Native", "Albanian", "Aleut", "Algerian", "Alhucemas", "Alsatian", "Amalfi", "Amara/Amhara", "Amazigh/Imazighen/Berber", "Amerasian", "American Indian", "American Indian and Alaska Native", "American Indian-English-French", "American Indian-English-German", "American Indian-English-Irish", "American Indian-German-Irish", "American Samoan", "American/United States", "Amerindian/Indigena/Indio", "Andalusian", "Andaman Islander", "Andhra Pradesh", "Andorran", "Anglo", "Angolan", "Anguilla Islander", "Antiguan/Barbudan", "Apache", "Appalachian", "Apulian", "Arab/Arabic", "Arapaho", "Arawak", "Argentinean/Argentine", "Arizona", "Arkansas", "Armenian", "Aruba Islander", "Aryan", "Asian", "Assamese", "Assiniboine Sioux", "Assyrian/Chaldean/Syriac", "Asturian", "Australian", "Australian Aborigine", "Austrian", "Azerbaijani", "Azeri", "Azorean", "Baggara", "Bahamian", "Bahraini", "Bajan/Barbadian", "Balearic Islander", "Baluchi", "Bamar/Burman", "Bangladeshi", "Bantu", "Barbadian", "Bashkir", "Basilicata", "Basque", "Bavarian", "Bedouin", "Belarusian/Belorussian", "Belgian", "Belizean", "Belorussian", "Bengali", "Benin", "Berber", "Berliner", "Bermudan", "Bessarabian", "Bhutanese", "Bioko", "Black", "Black Thai", "Black or African American", "Blackfeet", "Blackfeet Tribe of the Blackfeet Indian Reservation of Montana", "Bohemian", "Bolivian", "Borneo", "Bosniak", "Bosnian/Herzegovinian", "Botswana", "Brazilian", "Breton", "British", "British Isles", "British Virgin Islander", "British West Indian/Indies", "Briton/British", "Bucovina", "Bulgarian", "Burman", "Burmese", "Burundian", "Cabo Verdean", "Cajun", "Calabrian", "California", "Californio", "Cambodian", "Cameroonian/Cameroon", "Campbell Islander", "Canadian", "Canadian American Indian", "Canadian and French American Indian", "Canal Zone", "Canary Islander", "Cantonese", "Cape Verdean", "Caribbean", "Caroline Islander", "Carpathian", "Carpatho Rusyn", "Castillian", "Catalonian", "Cayenne", "Cayman Islander", "Celtic", "Central African", "Central African Republic", "Central American", "Central American Indian", "Central European", "Chadian", "Chamolinian", "Chamorro Islander", "Channel Islander", "Cherokee", "Chevash", "Cheyenne", "Chicano/Chicana", "Chickasaw", "Chilean", "Chinese", "Chippewa", "Chippewa-Cree Indians of the Rocky Boy's Reservation", "Choctaw", "Christmas Islander", "Chumash", "Chuukese", "Colombian", "Colorado", "Colored", "Colville", "Comanche", "Comanche Nation", "Confederated Salish and Kootenai Tribes of the Flathead Nation", "Confederated Tribes and Bands of the Yakama Nation", "Confederated Tribes of the Colville Reservation", "Congo-Brazzaville", "Congolese/Congo", "Connecticut", "Cook Islander", "Cornish", "Corsican", "Corsico Islander", "Cossack", "Costa Rican", "Cree", "Creek", "Creole", "Cretan", "Crimean", "Criollo/Criolla", "Croatian/Croat", "Crow", "Crow Tribe of Montana", "Cuban", "Cuban American", "Cycladic Islander", "Cypriot", "Czech", "Czechoslovakian", "Danish/Dane", "Delaware", "Dinka", "District of Columbia", "Djibouti", "Dominica Islander", "Dominican", "Dutch", "Dutch West Indian", "Dutch West Indian/Indies", "Dutch-French-Irish", "Dutch-German-Irish", "Dutch-Irish-Scotch", "East African", "East German", "East Indian", "East Indies", "Eastern Archipelago", "Eastern Cherokee", "Eastern European", "Eastern Tribes", "Ecuadorian", "Egyptian", "Emilia Romagna", "English", "English-French-German", "English-French-Irish", "English-German-Irish", "English-German-Swedish", "English-Irish-Scotch", "English-Scotch-Welsh", "Equatorial Guinea", "Eritrean", "Eskimo", "Estonian", "Ethiopian", "Eurasian", "European", "Faeroe Islander", "Fijian", "Filipino/Philippine", "Finnish/Finn", "Finno Ugrian", "Fleming/Flemish", "Florida", "Formosan", "French", "French Basque", "French Canadian", "French Samoan", "French West Indies", "Frisian", "Friulian", "Fulani/Hausa", "Fur", "Gabonese", "Gagauz", "Galician", "Gallego", "Gambian", "Gazan", "Georgia", "Georgian/Georgia CIS", "German", "German Russian", "German-French-Irish", "German-Irish-Italian", "German-Irish-Scotch", "German-Irish-Swedish", "Germanic", "Ghanaian/Ghanian", "Gibraltan", "Goanese", "Gosei", "Greek", "Greek Cypriote", "Greenlander", "Grenadian", "Gruziia", "Guadeloupe Islander", "Guamanian", "Guatemalan", "Guinea Bissau", "Guinean", "Gujarati", "Guyanese", "Guyanese/British Guiana", "Guyanese/French Guiana", "Haitian", "Hall Islander", "Hamburger", "Hanoverian", "Hausa", "Hawaiian", "Hawaiian/Native Hawaiian", "Hessian", "Hispanic", "Hmong", "Honduran", "Hong Kong", "Hopi", "Hungarian", "Husel", "Ibo/Igbo", "Icelander", "Idaho", "Ifni", "Illinois", "India", "Indian", "Indiana", "Indochinese", "Indonesian", "Inuit", "Inupiat", "Inupiat Eskimo", "Iowa", "Iranian", "Iraqi", "Irish", "Irish Scotch", "Iroquois", "Israeli", "Issei", "Italian", "Ivoirian/Ivory Coast", "Jamaican", "Japanese", "Javanese/Java/Jawa", "Jebel Druse", "Jewish/Jew", "Jordanian", "Kalmyk", "Kansas", "Kapinagamarangan", "Karelian", "Karnatakan", "Kashmiri", "Kashubian", "Katu", "Kazakh/Qazaq", "Kazakhstani", "Kentucky", "Kenyan", "Keralan", "Keres", "Kermadec Islander", "Khmer", "Kinh/Viet", "Kiowa", "Kirghiz", "Kiribatese", "Kittitian/Nevisian", "Kitts/Nevis Islander", "Korean", "Kosraean", "Kurdish/Kurd", "Kuria Muria Islander", "Kuwaiti", "La Raza", "Ladin", "Lamotrekese", "Lao Loum/Lowland Lao", "Laotian/Lao", "Lapp", "Latakian", "Latin", "Latin American", "Latin American Indian", "Latino/Latina", "Latvian", "Lebanese", "Lemko", "Lesotho", "Liberian", "Libyan", "Liechtensteiner", "Ligurian", "Lithuanian", "Livonian", "Lombardian", "Lorrainian", "Louisiana", "Lubecker", "Luiseno", "Lumbee", "Lumbee Indian", "Luxemburger", "Ma", "Macao", "Macedonian", "Madagascan", "Madeiran", "Madhya Pradesh", "Madrasi", "Magyar", "Maharashtran", "Maine", "Malawian", "Malay", "Malaysian", "Maldivian", "Malian", "Maltese", "Manchurian", "Mandarin", "Manx", "Maori", "Marches", "Marshall Islander", "Marshallese", "Maryland", "Massachusetts", "Mauritanian", "Mauritius", "Melanesian", "Melanesian Islander", "Mende", "Menominee Indian", "Meo", "Mesknetian", "Mestizo", "Mexican", "Mexican American", "Mexican American Indian", "Mexican Indian", "Mexican State", "Mexicano/Mexicana", "Miami", "Michigan", "Micmac", "Micronesian", "Middle Eastern", "Midway Islander", "Minnesota", "Mississippi", "Missouri", "Mnong", "Mohawk", "Mokilese", "Moldovan/Moldavian", "Molise", "Monegasque", "Mongolian", "Montagnard", "Montana", "Montenegrin", "Montserrat Islander", "Moor", "Moravian", "Mordovian", "Moroccan", "Mortlockese", "Mozambican", "Mulatto", "Muscat", "Muscogee (Creek) Nation", "Muscovite", "Mysore", "Naga", "Namanouito", "Namibian", "Natalian", "Native American", "Native Hawaiian", "Nauruan", "Navajo", "Navajo Nation", "Neapolitan", "Nebraska", "Nepalese/Nepali", "Nevada", "New Caledonian Islander", "New Guinean", "New Hampshire", "New Jersey", "New Mexico", "New York", "New Zealander", "Newfoundland", "Ngatikese", "Nicaraguan", "Niger", "Nigerian", "Nisei", "Niuean", "Nonwhite", "Norfolk Islander", "North African", "North American", "North Borneo", "North Carolina", "North Caucasian", "North Caucasian Turkic", "North Dakota", "Northern European", "Northern Irelander", "Northern Marianas", "Norwegian", "Nova Scotian", "Nuer", "Nuevo Mexicano", "Nukuoroan", "Occitan", "Oceania", "Oglala Sioux", "Ohio", "Okinawan", "Oklahoma", "Oklahoma Choctaw", "Omani", "Oneida Nation of New York/Oneida", "Oneida Tribe of Indians of Wisconsin", "Oregon", "Orissa", "Oromo", "Osage", "Ossetian", "Ottawa", "Pacific Islander", "Paiute", "Pakistani", "Palauan", "Palestinian", "Panamanian", "Papuan", "Paraguayan", "Pashtun/Pathan", "Pennsylvania", "Pennsylvania German", "Persian", "Peruvian", "Phoenix Islander", "Piedmontese", "Pima", "Pingelapese", "Polish/Pole", "Polynesian", "Pomeranian", "Pomo", "Ponapean", "Pondicherry", "Portuguese", "Potawatomi", "Providencia", "Prussian", "Pueblo", "Puerto Rican", "Puget Sound Salish", "Puglia", "Pulawatese", "Punjabi", "Qatar", "Quechua", "Rajasthani", "Rhode Island", "Rio de Oro", "Rom", "Romani", "Romanian", "Romansch", "Romanscho", "Rome", "Rosebud Sioux", "Rumanian", "Russian", "Rusyn", "Ruthenian", "Rwandan", "Ryukyu Islander", "Sac and Fox", "Saint Lucian", "Saipanese", "Salvadoran", "Samoan", "San Andres", "San Carlos Apache", "San Marino", "Sansei", "Sardinian", "Saudi Arabian/Saudi", "Sault Ste. Marie Chippewa", "Saxon", "Scandinavian/Nordic", "Scotch-Irish", "Scottish", "Seminole", "Seneca", "Senegalese", "Serbian/Serb", "Shan", "Shawnee", "Shona", "Shoshone", "Sicilian", "Sierra Leonean", "Sikkim", "Silesian", "Singaporean", "Singhalese/Sinhalese", "Sioux", "Slavic/Slav", "Slavonian", "Slovak", "Slovenian/Sloven", "Solomon Islander", "Somalian/Somali", "Sorb/Wend", "South African", "South American", "South American Indian", "South Carolina", "South Dakota", "South Yemeni", "Southern European", "Southerner", "Soviet Central Asia", "Soviet Turkic", "Soviet/Soviet Union", "Spaniard", "Spanish", "Spanish American", "Spanish American Indian", "Spanish Basque", "Sri Lankan", "St. Christopher", "St. Croix Islander", "St. John Islander", "St. Lucia Islander", "St. Maarten Islander", "St. Thomas Islander", "St. Vincent Islander/Vincent-Grenadine Islander", "St. Vincent and Grenadine Islander", "Subsaharan African", "Sudanese", "Sudetenlander", "Suisse", "Sumatran", "Surinamese", "Surinamese/Dutch Guiana", "Swaziland", "Swedish/Swede", "Swiss", "Switzer", "Syrian", "Tadzhik", "Tagalog", "Tahitian", "Taiwanese", "Tamil", "Tanganyikan", "Tanzanian", "Tarawa Islander", "Tartar", "Tasmanian", "Tatar", "Tejano/Tejana", "Temne/Temme/Themne", "Tennessee", "Teton Sioux", "Texas", "Thai", "Three Affiliated Tribes of North Dakota", "Tibetan", "Ticino", "Tigrinya/Tigray/Tigraway", "Tinian Islander", "Tirolean", "Tiv", "Tlingit", "Tlingit-Haida", "Tobagonian", "Togolese/Togo", "Tohono O'Odham", "Tokelauan", "Tongan", "Transjordan", "Transylvanian", "Trentino", "Trieste", "Trinidadian/Tobagonian", "Trucial Oman", "Truk Islander", "Trust Territory of the Pacific Islands", "Tsimshian", "Tunisian", "Turcoman", "Turkestani", "Turkish Cypriote", "Turkish/Turk", "Turks and Caicos Islander", "Turtle Mountain", "Tuscan", "Tuvinian", "U.S. Virgin Islander", "Udmurt", "Ugandan", "Ukrainian", "Ulithian", "Umbrian", "Union of South Africa", "United Arab Emirates/Emirati", "United Houma Nation", "Upper Voltan", "Uruguayan", "Utah", "Ute", "Uttar Pradesh", "Uzbek/Uzbeg", "Uzbekistani", "Valencian", "Valle d'Aosta", "Vanuatuan", "Veddah", "Venetian", "Venezuelan", "Vermont", "Vietnamese", "Virginia", "Volga", "Volta", "Voytak", "Wake Islander", "Wallachian", "Walloon", "Washington", "Welsh", "West African", "West Bank", "West German", "West Indian", "West Virginia", "Western European", "Western Lao", "Westphalian", "White Mountain Apache", "White/Caucasian", "Windish", "Wisconsin", "Woleaian", "Wyoming", "Yakama", "Yakut", "Yap Islander", "Yaqui", "Yemeni", "Yonsei", "Yoruba", "Yugoslavian", "Yuman", "Yupik/Yup'ik Eskimo", "Zairian", "Zambian", "Zanzibar Islander", "Zimbabwean", "Zulu", "Zuni"]
    words = [['', 'Asian' ,'Black','Hispanic', 'White' ],ethnicitys,createList(1, 100),['female', 'male']]
    d = [0,1,2,3]
    print(jsontodata(datagather(model,"Nurse","Huge Hospital", 25),words, d))

        

