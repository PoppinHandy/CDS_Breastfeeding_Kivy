# -*- coding: utf-8 -*-
"""
Created on Sat May 19 10:18:38 2018

@author: Andy Pham

First 28 Decision Support Breastfeeding app
"""
#import os
#os.environ['KIVY_IMAGE'] = 'pil,sdl2'
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, DictProperty
from kivy.storage.jsonstore import JsonStore
#from kivy.clock import Clock
from kivy.uix.label import Label
import re

Builder.load_file('first28_UI.kv')



# UI Template for risk screens          
class RiskLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(RiskLayout, self).__init__(**kwargs)
            
class LabelWrap(Label):
    pass

# Gateway button to access symptoms checklist
class AlertButton(Button):
    def __init__(self, **kwargs):
        super(AlertButton, self).__init__(**kwargs)
    def on_press(self):
        if self.text == 'Dehydration':
            App.get_running_app().root.current = 'Dehydration_Questions'

        elif self.text == 'ARI':
            App.get_running_app().root.current = 'Ari_Questions'
            
        # Have risk alert scereen remove buttons that have already been pressed
        App.get_running_app().root.screens[4].removeRisk(self)
    
# Button for after dehydration is solved
class SubmitSymptoms(Button):
    def __init__(self, **kwargs):
        super(SubmitSymptoms, self).__init__(**kwargs)
    def on_press(self):
        
        # Add to summary dictionary property to generate summary
        if self.text == 'Submit Dehydration':
            App.get_running_app().root.screens[5].risk_Score['Dehydration'] = App.get_running_app().root.screens[2].dehydrationScore
        elif self.text == 'Submit ARI':
            App.get_running_app().root.screens[5].risk_Score['ARI'] = App.get_running_app().root.screens[3].ariScore
       
        # If there are still risks, go back to risk alert screen
        riskLeft = App.get_running_app().root.screens[4].numberOfRisks
        if riskLeft > 0:
            App.get_running_app().root.current = 'Alert_Screen'
        else:
            App.get_running_app().root.screens[5].generateSummary()
            App.get_running_app().root.current = 'Summary_Screen'

# For saving and adding the profile to a json file
class AddProfile(Button):
    def __init__(self, **kwargs):
        super(AddProfile, self).__init__(**kwargs)
    def on_press(self):
        # Accessing new profile screen method to save profile info
        App.get_running_app().root.screens[1].saveProfileInfo()

# Button adds records for feeding and diapers to json files
class AddRecord(Button):
    def __init__(self, **kwargs):
        super(AddRecord, self).__init__(**kwargs)
    def on_press(self):
        # Call to MainMenu screen to save records in JSON
        feedingText = App.get_running_app().root.screens[0].ids.tabManager.ids.add_records_tab.ids.feed.text
        diapersText = App.get_running_app().root.screens[0].ids.tabManager.ids.add_records_tab.ids.diapers.text
        if feedingText == "" or diapersText == "":
            alertButton = BoxLayout(orientation='vertical')
            alertButton.add_widget(Label(text='Please enter a number for each entry.'))
            popupAlert = Popup(title="Entry Error", content=alertButton, auto_dismiss=False,size_hint=(.5,.5))
            alertButton.add_widget(Button(text='Got it!', on_press=popupAlert.dismiss, size_hint=(1, .5)))
            popupAlert.open()
        else:
            # Save record to json file
            App.get_running_app().root.screens[0].ids.tabManager.ids.add_records_tab.saveRecords()
            
            # Reset using root app path to all tab
            App.get_running_app().root.screens[0].ids.tabManager.ids.add_records_tab.ids.feed.text = ""
            App.get_running_app().root.screens[0].ids.tabManager.ids.add_records_tab.ids.diapers.text = ""
            App.get_running_app().root.screens[0].ids.tabManager.ids.add_records_tab.ids.date.text = ""
            

# Widget for reading in daily record text, filters out non-digit answers
class DigitRecord(TextInput):
    def __init__(self, **kwargs):
        super(DigitRecord, self).__init__(**kwargs)
        self.multiline=False
    def insert_text(self, substring, from_undo=False):
        pat = re.compile('[^\d+]') # Compiles a regex to match non-digits
        s = re.sub(pat, '', substring) # Replaces non-digits with no space
        
        # Return the filtered string
        return super(DigitRecord, self).insert_text(s, from_undo=from_undo)

class DateRecord(TextInput):
    def __init__(self, **kwargs):
        super(DateRecord, self).__init__(**kwargs)
        self.multiline=False
    def insert_text(self, substring, from_undo=False):
        # add a '/' for date format purposes once the required month or year is entered
        if len(self.text) == 1 or len(self.text) == 4:
            s = substring + '/'
            return super(DateRecord, self).insert_text(s, from_undo=from_undo)
        else:
            substring = substring[:10 - len(self.text)] # limit character entry to 10 characters for full date
            pat = re.compile('[^\d+]') # Compile a regex to match non-dates
            s = re.sub(pat, '', substring) # Replaces non-digits with no space
            # Return the filtered string
            return super(DateRecord, self).insert_text(s, from_undo=from_undo)
    
# Holds all tabs for the main menu    
class AllTabs(TabbedPanel):
    feeding_info = StringProperty('')
    diapers_info = StringProperty('')
    ari_Score = NumericProperty(0)
    dehydration_Score = NumericProperty(0)
    def __init__(self, **kwargs):
        super(AllTabs, self).__init__(**kwargs)
        


class AddRecordsTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(AddRecordsTab, self).__init__(**kwargs)   
        # Saves records and then calls the appropriate popup
    def saveRecords(self):
        # For testing
        #store = JsonStore("D:/Git/Kivy_Apps/First28/records.json") 
        store = JsonStore("records.json")
        # Storing record info
        feedingText = App.get_running_app().root.screens[0].ids.tabManager.ids.add_records_tab.ids.feed.text
        diapersText = App.get_running_app().root.screens[0].ids.tabManager.ids.add_records_tab.ids.diapers.text
        dateText = App.get_running_app().root.screens[0].ids.tabManager.ids.add_records_tab.ids.date.text
        store.put(dateText, feeding=feedingText, diaper=diapersText)
        feeding_int = int(feedingText)
        diapers_int = int(diapersText)
        
        # if diapers is abnormal, raise both ari and dehydration
        if diapers_int <= 6:
            App.get_running_app().root.screens[4].addRisk("ARI")
            App.get_running_app().root.screens[4].addRisk("Dehydration")
        # if diapers is normal and feediing is abnormal, raise dehydration
        elif feeding_int <= 6:
            App.get_running_app().root.screens[4].addRisk("Dehydration")
        else:
            pass # everything is a-ok
        App.get_running_app().root.current = "Alert_Screen"
                


# For all records and such
class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)

# For entering in data from a first time user
class NewProfile(Screen):
    bby_name = StringProperty('')
    bby_weight = StringProperty('')
    bby_height = StringProperty('')
    
    def saveProfileInfo(self):
        # For testing
        #store = JsonStore("D:/Git/Kivy_Apps/First28/profile.json")
        store = JsonStore("profile.json")
        # Storing user information
        store.put('main_profile', name=self.bby_name, weight=self.bby_weight, height=self.bby_height)
        
        # Switching to new screen once the new user profile is implemented
        self.parent.current = 'Menu'

# Screen for displaying potential risks based on data input
class AlertScreen(Screen):
    numberOfRisks = NumericProperty(0) # Determines whether or not to go back to alert screen
    def __init__(self, **kwargs):
        super(AlertScreen, self).__init__(**kwargs)
    # adds the relevant risks based on data input
    def addRisk(self, name):
        self.ids.button_space.add_widget(AlertButton(text=name))
        self.numberOfRisks += 1
    # removes risk if already answered questionnaire
    def removeRisk(self, btn_object):
        self.ids.button_space.remove_widget(btn_object)
        self.numberOfRisks -= 1
    
# Handles logic for dehydration question set and keeps track of score
class DehydrationSet(Screen):
    dehydrationScore = NumericProperty(0)
    def __init__(self, **kwargs):
        super(DehydrationSet, self).__init__(**kwargs)
    def increaseScore(self, value):
        if value:
            self.dehydrationScore += 1
        else:
            self.dehydrationScore -= 1
    def clearScreen(self):
        # Look for all the checkbox IDs, which are labeled in a specific format, and set them to False
        for k in self.ids:
            if 'dehydrationS' in k:
                if self.ids[k].active:
                    self.ids[k].active = False

# Handles logic for ARI question set and keeps track of score
class AriSet(Screen):
    ariScore = NumericProperty(0)
    def __init__(self, **kwargs):
        super(AriSet, self).__init__(**kwargs)
    def increaseScore(self, value):
        if value:
            self.ariScore += 1
        else:
            self.ariScore -= 1
    def clearScreen(self):
        # Look for all the checkbox IDs, which are labeled in a specific format, and set them to False
        for k in self.ids:
            if 'ariS' in k:
                if self.ids[k].active:
                    self.ids[k].active = False

# Screen to show after completing symptoms checklist
class SummaryScreen(Screen):
    risk_Score = DictProperty()
    def __init__(self, **kwargs):
        super(SummaryScreen, self).__init__(**kwargs)
    def generateSummary(self):
        # Anything > 4 is severe, anything less is moderate
        for k in self.risk_Score:
            severityText = k + ": "
            resourcesText = k + ": "
            if self.risk_Score[k] >= 4:    
                severityText += "[color=ff3333][u]Severe[/u][/color]"
                resourcesText += "\nResources for severe " + k + " here"
            else:
                severityText += "[color=ffff00][u]Moderate[/u][/color]"
                resourcesText += "\nResources for moderate " + k + " here"
        
            self.ids.severity_score.add_widget(LabelWrap(text=severityText, markup=True))
            self.ids.resources_set.add_widget(LabelWrap(text=resourcesText, markup=True))
    

class First28ScreenManager(ScreenManager):
    pass

class first_28_App(App):
    def build(self):
        # For testing
        #store = JsonStore ('D:/Git/Kivy_Apps/First28/profile.json')
        store = JsonStore ('profile.json')
        sm = First28ScreenManager()
        if store.exists('main_profile'):
            sm.current = 'Menu'
        else:
            sm.current = 'NewProfile'            
        return sm

if __name__ == '__main__':
    first_28_App().run()
# =================================================NOTES==========================================================
