#General Purpose Functions to be used in LSNYC Report Prep 
import datetime

#Remove extraneous summary rows
def RemoveNoCaseID(CaseID):
        if CaseID == '' or CaseID == 'nan' or CaseID.startswith("Unique") == True:
            return 'No Case ID'

        else:
            return str(CaseID)


#Turn a case ID# into a hyperlink
def Hyperlinker(CaseID):
        last7 = CaseID[-7:]
        hyperlinkedID = '=HYPERLINK("https://lsnyc.legalserver.org/matter/dynamic-profile/view/'+last7+'",'+ '"' + CaseID +'"' +')'
        return hyperlinkedID 
        

#Take a date formatted as MM/DD/YYYY and make it YYYYMMDD so it can be easily compared to other dates           
def DateMaker (Date):
            
            if isinstance(Date,datetime.datetime) == True:
                Date = Date.strftime("%m/%d/%Y")
            DateMonth = Date[:2]
            DateDay = Date[3:5]
            DateYear = Date[6:]
            
            
            if Date == "":
                return ""            
            else:
                return int(DateYear + DateMonth + DateDay)


#Turn the Queens micro-cities into just saying 'queens'       
QueensNeighborhoods = ["Arverne",
                        "Astoria",
                        "Bayside",
                        "Bellerose",
                        "Cambria Heights",
                        "College Point",
                        "Corona",
                        "East Elmhurst",
                        "Elmhurst",
                        "Far Rockaway",
                        "Flushing",
                        "Forest Hills",
                        "Fresh Meadows",
                        "Glendale",
                        "Hollis",
                        "Jackson Heights",
                        "Jackson Hts",
                        "Jamaica",
                        "Kew Gardens",
                        "Laurelton",
                        "Little Neck",
                        "Long Is City",
                        "Long Island City",
                        "Maspeth",
                        "Middle Village",
                        "Ozone Park",
                        "Queens",
                        "Queens Village",
                        "Queens Vlg",
                        "Rego Park",
                        "Richmond Hill",
                        "Ridgewood",
                        "Rockaway Beach",
                        "Rockaway Park",
                        "Rosedale",
                        "S Ozone Park",
                        "Saint Albans",
                        "South Ozone Park",
                        "South Richmond Hill",
                        "Springfield Gardens",
                        "Sprngfld Gdns",
                        "Sunnyside",
                        "Whitestone",
                        "Woodhaven",
                        "Woodside"]
       
def QueensConsolidater(City):
    if City in QueensNeighborhoods:
        return "Queens"
    else:
        return City

#Borough by Zip Code
BronxZips = [
            "10451",
            "10452",
            "10453",
            "10454",
            "10455",
            "10456",
            "10457",
            "10458",
            "10459",
            "10460",
            "10461",
            "10462",
            "10463",
            "10464",
            "10465",
            "10466",
            "10467",
            "10468",
            "10469",
            "10470",
            "10471",
            "10472",
            "10473",
            "10474",
            "10475",
            "10499",
            "10550",
            "10704",
            "10705",
            "10803"]

BrooklynZips = [
        "11201",
        "11202",
        "11203",
        "11204",
        "11205",
        "11206",
        "11207",
        "11208",
        "11209",
        "11210",
        "11211",
        "11212",
        "11213",
        "11214",
        "11215",
        "11216",
        "11217",
        "11218",
        "11219",
        "11220",
        "11221",
        "11222",
        "11223",
        "11224",
        "11225",
        "11226",
        "11228",
        "11229",
        "11230",
        "11231",
        "11232",
        "11233",
        "11234",
        "11235",
        "11236",
        "11237",
        "11238",
        "11239",
        "11241",
        "11242",
        "11243",
        "11245",
        "11247",
        "11249",
        "11251",
        "11252",
        "11256",
        "11693"]

ManhattanZips = ["10001",
            "10002",
            "10003",
            "10004",
            "10005",
            "10006",
            "10007",
            "10008",
            "10009",
            "10010",
            "10011",
            "10012",
            "10013",
            "10014",
            "10016",
            "10017",
            "10018",
            "10019",
            "10020",
            "10021",
            "10022",
            "10023",
            "10024",
            "10025",
            "10026",
            "10027",
            "10028",
            "10029",
            "10030",
            "10031",
            "10032",
            "10033",
            "10034",
            "10035",
            "10036",
            "10037",
            "10038",
            "10039",
            "10040",
            "10041",
            "10043",
            "10044",
            "10045",
            "10047",
            "10048",
            "10055",
            "10065",
            "10069",
            "10072",
            "10075",
            "10080",
            "10081",
            "10082",
            "10087",
            "10101",
            "10102",
            "10103",
            "10104",
            "10105",
            "10106",
            "10107",
            "10108",
            "10109",
            "10110",
            "10111",
            "10112",
            "10113",
            "10114",
            "10115",
            "10116",
            "10117",
            "10118",
            "10119",
            "10120",
            "10121",
            "10122",
            "10123",
            "10124",
            "10125",
            "10126",
            "10128",
            "10129",
            "10130",
            "10131",
            "10132",
            "10133",
            "10138",
            "10149",
            "10150",
            "10151",
            "10152",
            "10153",
            "10154",
            "10155",
            "10156",
            "10157",
            "10158",
            "10159",
            "10160",
            "10161",
            "10162",
            "10163",
            "10164",
            "10165",
            "10166",
            "10167",
            "10168",
            "10169",
            "10170",
            "10171",
            "10172",
            "10173",
            "10174",
            "10175",
            "10176",
            "10177",
            "10178",
            "10179",
            "10185",
            "10197",
            "10199",
            "10213",
            "10242",
            "10249",
            "10256",
            "10259",
            "10260",
            "10261",
            "10265",
            "10268",
            "10269",
            "10270",
            "10271",
            "10272",
            "10273",
            "10274",
            "10275",
            "10276",
            "10277",
            "10278",
            "10279",
            "10280",
            "10281",
            "10282",
            "10285",
            "10286",
            "10292",
            "10463",
            "11201"]

QueensZips = ["11001",
        "11004",
        "11005",
        "11040",
        "11096",
        "11101",
        "11102",
        "11103",
        "11104",
        "11105",
        "11106",
        "11109",
        "11239",
        "11351",
        "11352",
        "11354",
        "11355",
        "11356",
        "11357",
        "11358",
        "11359",
        "11360",
        "11361",
        "11362",
        "11363",
        "11364",
        "11365",
        "11366",
        "11367",
        "11368",
        "11369",
        "11370",
        "11371",
        "11372",
        "11373",
        "11374",
        "11375",
        "11377",
        "11378",
        "11379",
        "11380",
        "11381",
        "11385",
        "11386",
        "11405",
        "11411",
        "11412",
        "11413",
        "11414",
        "11415",
        "11416",
        "11417",
        "11418",
        "11419",
        "11420",
        "11421",
        "11422",
        "11423",
        "11424",
        "11425",
        "11426",
        "11427",
        "11428",
        "11429",
        "11430",
        "11431",
        "11432",
        "11433",
        "11434",
        "11435",
        "11436",
        "11439",
        "11451",
        "11499",
        "11559",
        "11580",
        "11690",
        "11691",
        "11692",
        "11693",
        "11694",
        "11695",
        "11697"]

StatenIslandZips = ["10301",
            "10302",
            "10303",
            "10304",
            "10305",
            "10306",
            "10307",
            "10308",
            "10309",
            "10310",
            "10311",
            "10312",
            "10313",
            "10314"]

def ZipToCity (ZipCode):
    ZipCode = str(ZipCode)
    if ZipCode in BronxZips:
        return "Bronx"
    elif ZipCode in BrooklynZips:
        return "Brooklyn"
    elif ZipCode in ManhattanZips:
        return "New York"
    elif ZipCode in QueensZips:
        return "Queens"
    elif ZipCode in StatenIslandZips:
        return "Staten Island"
    else:
        return "No NYC ZipCode"
    
        

        
#Borough office Abbreviators

def OfficeAbbreviator(AssignedBranch):
    if AssignedBranch == "Bronx Legal Services":
        return "BxLS"
    elif AssignedBranch == "Brooklyn Legal Services":
        return "BkLS"
    elif AssignedBranch == "Queens Legal Services":
        return "QLS"    
    elif AssignedBranch == "Manhattan Legal Services":
        return "MLS"    
    elif AssignedBranch == "Staten Island Legal Services":
        return "SILS"    
    elif AssignedBranch == "Legal Support Unit":
        return "LSU"    
    else:
        return AssignedBranch    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        