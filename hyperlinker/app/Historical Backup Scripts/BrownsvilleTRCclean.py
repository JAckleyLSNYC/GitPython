from flask import render_template, flash, redirect, url_for, request, Flask, jsonify, send_from_directory
from app import app, db
from app.models import User, Post
from app.forms import PostForm
from werkzeug.urls import url_parse
from datetime import datetime
import pandas as pd


@app.route("/BrownsvilleTRCclean", methods=['GET', 'POST'])
def upload_BrownsvilleTRCclean():
    if request.method == 'POST':
        print(request.files['file'])
        f = request.files['file']
        
        test = pd.read_excel(f)
        
        test.fillna('',inplace=True)
        
        #Cleaning
        if test.iloc[0][0] == '':
            data_xls = pd.read_excel(f,skiprows=2)
        else:
            data_xls = pd.read_excel(f)
        
        data_xls.fillna('',inplace=True)
        last7 = data_xls['Matter/Case ID#'].apply(lambda x: x[3:])
        CaseNum = data_xls['Matter/Case ID#']
        data_xls['Temp Hyperlinked Case #']='=HYPERLINK("https://lsnyc.legalserver.org/matter/dynamic-profile/view/'+last7+'",'+ '"' + CaseNum +'"' +')'
        del data_xls['Matter/Case ID#']
        move=data_xls['Temp Hyperlinked Case #']
        data_xls.insert(0,'Hyperlinked Case #', move)           
        del data_xls['Temp Hyperlinked Case #']
        
        data_xls['Assigned Branch/CC'] = data_xls['Assigned Branch/CC'].str.replace('Bronx Legal Services','BxLS')
        data_xls['Assigned Branch/CC'] = data_xls['Assigned Branch/CC'].str.replace('Brooklyn Legal Services','BkLS')
        data_xls['Assigned Branch/CC'] = data_xls['Assigned Branch/CC'].str.replace('Queens Legal Services','QLS')
        data_xls['Assigned Branch/CC'] = data_xls['Assigned Branch/CC'].str.replace('Manhattan Legal Services','MLS')
        data_xls['Assigned Branch/CC'] = data_xls['Assigned Branch/CC'].str.replace('Staten Island Legal Services','SILS')
        data_xls['Assigned Branch/CC'] = data_xls['Assigned Branch/CC'].str.replace('Legal Support Unit','LSU')


        #only brownsville advocates
        
        brownsville_advocates = [
                    "McCowen, Tamella",
                    "Farrell, Emily",
                    "Goncharov-Cruickshnk, Natalie",
                    "Henriquez, Luis",
                    "Katnani, Samar",
                    "Kelly, Dawn",
                    "Landry-Reyes, Jane",
                    "Bailey, Michael",
                    "Costa, Stephanie",
                    "Crisona, Kathryn",
                    "Hardy, Le`Shera",
                    "Hecht-Felella, Laura",
                    "Marchena, Ivan",
                    "McCormick, James",
                    "Patel, Mona",
                    "Roman, Melissa",
                    "Rubin, Jenn",
                    "St. Louis, Bianca",
                    "Wong, Humbert",
                    "Xie, Vivian",
                    "Chew, Thomas",
                    "Cisneros, Marisol",
                    "DeLong, Sarah",
                    "Reardon, Elizabeth",
                    "Ijaz, Kulsoom",
                    "Catuira, Rochelle",
                    "Haynes, Tralane",
                    "Hernandez, Elizabeth",
                    "Lee, Alicia",
                    "Pongnon, Miouly"
                    ]
        
        def BrownsvilleAdvocate (advocate, brownsvillelist ):
            if advocate in brownsvillelist:
                return "Brownsville"
            else:
                return "delete"

        data_xls['Brownsville?'] = data_xls.apply(lambda x: BrownsvilleAdvocate(x['Primary Advocate'], brownsville_advocates), axis = 1)
        
        data_xls = data_xls[data_xls['Brownsville?'] != 'delete']        

        #Has to have an HRA Release
        
        def HRARelease (HRARelease,EligibilityDate):
            if HRARelease == 'No' and EligibilityDate != '':
                return '**REMOVE ELIGIBILITY DATE**'
            elif HRARelease == '' and EligibilityDate != '':
                return '**REMOVE ELIGIBILITY DATE**'
            elif HRARelease == 'Yes':
                return ''
            else:
                return 'Needs HRA Release'
        data_xls['HRA Release Tester'] = data_xls.apply(lambda x: HRARelease(x['HRA Release?'],x['HAL Eligibility Date']), axis=1)
        
        #Has to have a Housing Type of Case
        
        def HousingType (HousingType):
            if HousingType == '':
                return 'Needs Housing Type of Case'
            else:
                return ''
        data_xls['Housing Type Tester'] = data_xls.apply(lambda x: HousingType(x['Housing Type Of Case']), axis=1)
        
        
        #Has to have a Housing Level of Service - and if DHCR case has to be admin proceeding or rep - admin agency 
        
        
        def HousingLevel (HousingLevel,HousingType):
            if HousingLevel == '':
                return 'Needs Level of Service'
            else:
                return ''
        data_xls['Housing Level Tester'] = data_xls.apply(lambda x: HousingLevel(x['Housing Level of Service'],x['Housing Type Of Case']), axis=1)
        
        #Has to say whether or not it's a building case 
        
        def BuildingCase (BuildingCase):
            if BuildingCase == '':
                return 'Needs Building Case Answer'
            if BuildingCase == 'Prefer Not To Answer':
                return 'Needs Building Case Answer'
            else:
                return ''
        data_xls['Building Case Tester'] = data_xls.apply(lambda x: BuildingCase(x['Housing Building Case?']), axis=1)
        
        #Referral Source Can't Be Blank
        
        def Referral (Referral,FundingSource):
            if Referral == '':
                return 'Needs Referral Source'
            elif FundingSource == '3011 TRC FJC Initiative' and Referral != 'FJC Housing Intake':
                return 'Must be FJC'
            else:
                return ''
        data_xls['Referral Tester'] = data_xls.apply(lambda x: Referral(x['Referral Source'],x['Primary Funding Code']), axis=1)
        
        #monthly rent can't be 0
        
        def Rent (Rent):
            if Rent == 0:
                return 'Needs Rent Amount'
            else:
                return ''
        data_xls['Rent Tester'] = data_xls.apply(lambda x: Rent(x['Housing Total Monthly Rent']), axis=1)
        
        #number of units in building can't be 0
        
        def Units (Units):
            
            Units = str(Units)
            if Units == 0:
                return 'Needs Units'
            elif any(c.isalpha() for c in Units) == True:
                return 'Must be a number'
            else:
                return ''
        data_xls['Unit Tester'] = data_xls.apply(lambda x: Units(x['Housing Number Of Units In Building']), axis=1)
        
        #Housing form of regulation can't be blank
        
        def Regulation (Regulation):
            if Regulation == '':
                return 'Needs Form of Regulation'
            else:
                return ''
        data_xls['Regulation Tester'] = data_xls.apply(lambda x: Regulation(x['Housing Form Of Regulation']), axis=1)
        
        #Housing subsidy can't be blank (can be none)
        
        def Subsidy (Subsidy):
            if Subsidy == '':
                return 'Needs Type of Subsidy'
            else:
                return ''
        data_xls['Subsidy Tester'] = data_xls.apply(lambda x: Subsidy(x['Housing Subsidy Type']), axis=1)
        
        #Years in Apartment Can't be 0 (can be -1)
        
        def Years (Years):
            if Years == 0:
                return 'Needs Years In Apartment'
            elif Years < -1:
                return 'Invalid Number'
            else:
                return ''
        data_xls['Years in Apartment Tester'] = data_xls.apply(lambda x: Years(x['Housing Years Living In Apartment']), axis=1)
        
        #Language Can't be Blank
        
        def Language (Language):
            if Language == '':
                return 'Needs Language'
            else:
                return ''
        data_xls['Language Tester'] = data_xls.apply(lambda x: Language(x['Language']), axis=1)
        
        #haven't added below to tester tester
        
        #Housing Posture of Case can't be blank if there is an eligibility date
        
        def Posture (Posture,EligibilityDate):
            if EligibilityDate  == '' and Posture == '':
                return 'Needs Posture of Case'
            else:
                return ''
        data_xls['Posture Tester'] = data_xls.apply(lambda x: Posture(x['Housing Posture of Case on Eligibility Date'],x['HAL Eligibility Date']), axis=1)
        
        #Housing Income Verification can't be blank or none
        def IncomeVerification (IncomeVerification):
            if IncomeVerification == '':
                return 'Needs Income Verification'
            if IncomeVerification == 'None':
                return 'Needs Income Verification'
            else:
                return ''
        data_xls['Income Verification Tester'] = data_xls.apply(lambda x: IncomeVerification(x['Housing Income Verification']), axis=1)
       
        #PA Tester (need to be correct format as well)
        def PATester (IncomeVerification,PANumber):
                        
            PANumber = str(PANumber)
            LastCharacter = PANumber[-1:]
            PenultimateCharater = PANumber[-2:-1]
            SecondCharacter = PANumber [1:2]
            if PANumber == '':
                return ''
            elif PANumber == 'None':
                return ''
            elif SecondCharacter == 'o':
                return ''
            elif SecondCharacter == 'n':
                return ''
            elif len(PANumber) == 10 and str.isalpha(LastCharacter) == True and str.isalpha(PenultimateCharater) == False and PenultimateCharater != '-' and PenultimateCharater != ' ':
                return ''
            elif len(PANumber) == 12 and str.isalpha(LastCharacter) == True and str.isalpha(PenultimateCharater) == False and PenultimateCharater != '-' and PenultimateCharater != ' ':
                return ''
            elif len(PANumber) == 9 and str.isalpha(LastCharacter) == False and PenultimateCharater != '-' and PenultimateCharater != ' ':
                return ''
            elif SecondCharacter == 'o':
                return 'Needs PA Number'
            else:
                return 'PA Number Format Wrong'
                
        data_xls['PA Tester'] = data_xls.apply(lambda x: PATester(x['Housing Income Verification'],x['Gen Pub Assist Case Number']), axis=1)
        
        #Test if case number is correct format
        def CaseNum (CaseNum):
            CaseNum = str(CaseNum)
            First3 = CaseNum[0:3]
            ThirdFromEnd = CaseNum[-3:-2]
            SecondFromEnd = CaseNum[-2:-1]
            First6 = CaseNum[0:6]
            First2 = CaseNum[0:2]
            #City LT Case format LT-123456-19/XX
            if len(CaseNum) == 15 and First3 == 'LT-' and ThirdFromEnd == '/':
                return ''
            elif len(CaseNum) == 15 and First3 == 'CV-' and ThirdFromEnd == '/':
                return ''
            #DHCR format AA-123456-S (or 2 letters at end)
            elif str.isalpha(First2) == True and len(CaseNum) == 11 and SecondFromEnd == '-':
                return ''
            elif str.isalpha(First2) == True and len(CaseNum) == 12 and ThirdFromEnd == '-':
                return ''
            #Federal/Supreme format 123456/2019
            elif len(CaseNum) == 11 and str.isdigit(First6) == True:
                return ''
            else:
                return "Case Number Format Wrong"
                
        data_xls['Case Number Tester'] = data_xls.apply(lambda x: CaseNum(x['Gen Case Index Number']), axis=1)
        
        #Test Housing Activity Indicator - can't be blank for closed cases that are full rep state or full rep federal(housing level of service) and eviction cases(housing type of case: non-payment holdover illegal lockout nycha housing termination)
        
        evictiontypes = ['Holdover','Non-payment','Illegal Lockout','NYCHA Housing Termination']
        leveltypes = ['Representation - State Court','Representation - Federal Court']
        
        def ActivityTester(HousingActivity,Disposition,Level,Type,EvictionTypes,LevelTypes):
            if Disposition == 'Closed' and Level in LevelTypes and Type in EvictionTypes and HousingActivity == '':
                return 'Needs Activity Indicator'
            else:
                return ''
        
       
        data_xls['Housing Activity Tester'] = data_xls.apply(lambda x: ActivityTester(x['Housing Activity Indicators'],x['Case Disposition'],x['Housing Level of Service'],x['Housing Type Of Case'],evictiontypes,leveltypes), axis = 1)
        
        #Test Housing Services Rendered - can't be blank for closed cases that are full rep state or full rep federal(housing level of service)
        
        def ServicesTester(HousingServices,Disposition,Level,Type,EvictionTypes,LevelTypes):
            if Disposition == 'Closed' and Level in LevelTypes and HousingServices == '':
                return 'Needs Services Rendered'
            elif Level == 'Representation - Admin. Agency' and Disposition == 'Closed':
                return 'Needs Services Rendered'
            else:
                return ''
               
        data_xls['Housing Services Tester'] = data_xls.apply(lambda x: ServicesTester(x['Housing Services Rendered to Client'],x['Case Disposition'],x['Housing Level of Service'],x['Housing Type Of Case'],evictiontypes,leveltypes), axis = 1)
        
        #Outcome Tester - needs outcome and date for eviction cases that are full rep at state or federal level (not admin)
        
        def OutcomeTester (Disposition,Outcome,OutcomeDate,Level,Type,EvictionTypes,LevelTypes):
            if Disposition == 'Closed' and Level in LevelTypes and Type in EvictionTypes and Outcome == '' and OutcomeDate == '':
                return 'Needs Outcome & Date'
            elif Disposition == 'Closed' and Level in LevelTypes and Type in EvictionTypes and Outcome == '':
                return 'Needs Outcome'
            elif Disposition == 'Closed' and Level in LevelTypes and Type in EvictionTypes and OutcomeDate == '':
                return 'Needs Outcome Date'
            else:
                return ''
        data_xls['Outcome Tester'] = data_xls.apply(lambda x: OutcomeTester(x['Case Disposition'],x['Housing Outcome'],x['Housing Outcome Date'],x['Housing Level of Service'],x['Housing Type Of Case'],evictiontypes,leveltypes), axis = 1)
        
        #Is everything okay with a case? (delete if so?)

        def TesterTester (ReleaseTester,TypeTester,LevelTester,BuildingTester,ReferralTester,RentTester,UnitTester,RegulationTester,SubsidyTester,YearsTester,LanguageTester,PostureTester,IncomeVerification,PATester,CaseNumberTester,ActivityTester,ServicesTester,OutcomeTester):
            if ReleaseTester == '' and TypeTester == '' and LevelTester == '' and BuildingTester == '' and ReferralTester == '' and RentTester == '' and UnitTester == '' and RegulationTester == '' and SubsidyTester == '' and YearsTester == '' and LanguageTester == '' and PostureTester == '' and IncomeVerification == '' and PATester == '' and CaseNumberTester == '' and ActivityTester == '' and ServicesTester == '' and OutcomeTester == '':
                return 'All Good!'
            else:
                return 'Case Needs Attention'
            
        data_xls['Tester Tester'] = data_xls.apply(lambda x: TesterTester(x['HRA Release Tester'],x['Housing Type Tester'],x['Housing Level Tester'],x['Building Case Tester'],x['Referral Tester'],x['Rent Tester'],x['Unit Tester'],x[ 'Regulation Tester'],x['Subsidy Tester'],x['Years in Apartment Tester'],x['Language Tester'],x['Posture Tester'],x['Income Verification Tester'],x['PA Tester'],x['Case Number Tester'],x['Housing Activity Tester'],x['Housing Services Tester'],x['Outcome Tester']),axis=1)
        

        #(delete if so?)
        
        data_xls = data_xls[data_xls['Tester Tester'] != 'All Good!']

        #sort by case handler
        
        data_xls = data_xls.sort_values(by=['Primary Advocate'])

        
        #Put everything in the right order
        
        data_xls = data_xls[['Hyperlinked Case #','Primary Advocate','HRA Release Tester','Housing Type Tester','Housing Level Tester','Building Case Tester','Referral Tester','Rent Tester','Unit Tester', 'Regulation Tester','Subsidy Tester','Years in Apartment Tester','Language Tester','Posture Tester','Income Verification Tester','PA Tester','Case Number Tester','Housing Activity Tester','Housing Services Tester','Outcome Tester']]      
        
        #Preparing Excel Document
        
        output_filename = f.filename     
        writer = pd.ExcelWriter("app\\sheets\\"+output_filename, engine = 'xlsxwriter')
        data_xls.to_excel(writer, sheet_name='Sheet1',index=False)

        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        link_format = workbook.add_format({'font_color':'blue', 'bold':True, 'underline':True})
        regular_format = workbook.add_format({'font_color':'black'})
        problem_format = workbook.add_format({'bg_color':'yellow'})
        
        
        worksheet.set_column('A:A',20,link_format)
        worksheet.set_column('B:BL',25)
        
        worksheet.conditional_format('C2:T100000',{'type': 'cell',
                                                 'criteria': '!=',
                                                 'value': '""',
                                                 'format': problem_format})
        writer.save()
        
        return send_from_directory('sheets',output_filename, as_attachment = True, attachment_filename = "Cleaned " + f.filename)

    return '''
    <!doctype html>
    <title>BrownsvilleTRCTester</title>
    <h1>Prepare a Brownsville TRC Cleanup Report:</h1>
    <form action="" method=post enctype=multipart/form-data>
    <p><input type=file name=file><input type=submit value=Clean!>
    </form>
    <h3>Instructions:</h3>
    <ul type="disc">
    <li>This tool is meant to be used in conjunction with the LegalServer report called "TRC Raw Case Data Report".</li>
    <li>It will only return cases for Brownsville advocates.</li>
    <li>Browse your computer using the field above to find the LegalServer excel document that you want to process for TRC cleanup.</li> 
    <li>Once you have identified this file, click ‘Clean!’ and you should shortly be given a prompt to either open the file directly or save the file to your computer.</li> 
    <li>When you first open the file, all case numbers will display as ‘0’ until you click “Enable Editing” in excel, this will populate the fields.</li> </ul>
    </br>
    <a href="/">Home</a>
    '''
