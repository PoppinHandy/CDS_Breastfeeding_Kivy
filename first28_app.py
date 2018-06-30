# -*- coding: utf-8 -*-
"""
Created on Sat May 19 10:18:38 2018

@author: Andy Pham

First 28 Decision Support Breastfeeding app
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.storage.jsonstore import JsonStore
from KivyCalendar import CalendarWidget
#from kivy.uix.checkbox import CheckBox
#from kivy.clock import Clock
from kivy.uix.label import Label
import re

Builder.load_file('first28_UI.kv')



# NEXT STEPS: CLEAR MENU SCREEN ONCE GOT BACK AND WORK ON ARI
class AlertButton(Button):
    def __init__(self, **kwargs):
        super(AlertButton, self).__init__(**kwargs)
    def on_press(self):
        if self.text == 'Dehydration':
            App.get_running_app().root.current = 'Dehydration_Questions'

        elif self.text == 'ARI':
            App.get_running_app().root.current = 'Ari_Questions'
        # parent.parent = BoxLayout, parent.parent.parent = GridLayout, 4 parents = Popup
        self.parent.parent.parent.parent.parent.dismiss()
    
# Button for after dehydration is solved
class SymptomsButton(Button):
    def __init__(self, **kwargs):
        super(SymptomsButton, self).__init__(**kwargs)
    def on_press(self):
        # Make sure to go back to main menu
        App.get_running_app().root.current = 'Menu'
        
        # Customize text based on button name
        if self.text == 'Submit Dehydration':
            acknowledgeButton = BoxLayout(orientation='vertical')
            symptomsText = "Your baby is showing " + str(self.parent.parent.dehydrationScore) + " out of 7 symptoms for dehydration."
            if self.parent.parent.dehydrationScore >= 4:
                symptomsText += "\nYou should consider consulting your doctor."
            else:
                symptomsText += "\nHere's how you can feed your baby better --> (Breastfeeding support)"
            acknowledgeButton.add_widget(LabelWrap(text=symptomsText))
            popupDehydrationSummary = Popup(title="Dehydration Summary", content=acknowledgeButton, auto_dismiss=False,size_hint=(.5,.5))
            acknowledgeButton.add_widget(Button(text='Acknowledge and exit', on_press=popupDehydrationSummary.dismiss, size_hint=(1, .5)))
            popupDehydrationSummary.open()
        elif self.text == 'Submit ARI':
            masterAriScore = App.get_running_app().root.screens[3].ariScore
            App.get_running_app().root.screens[3].clearScreen()
            acknowledgeButton = BoxLayout(orientation='vertical')
            symptomsText = "Your baby is showing " + str(masterAriScore) + " out of 6 symptoms for ARI."
            if self.parent.parent.ariScore >= 4:
                symptomsText += "\nYou should consider consulting your doctor."
            else:
                symptomsText += "\nHere's how you can feed your baby better --> (Breastfeeding support)"
            acknowledgeButton.add_widget(LabelWrap(text=symptomsText))
            popupARISummary = Popup(title="ARI Summary", content=acknowledgeButton, auto_dismiss=False,size_hint=(.5,.5))
            acknowledgeButton.add_widget(Button(text='Acknowledge and exit', on_press=popupARISummary.dismiss, size_hint=(1, .5)))
            popupARISummary.open()

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
        pat = re.compile('[^[\d+/\d+/\d+]') # Compile a regex to match non-dates
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
        store = JsonStore("D:/Git/Kivy_Apps/First28/records.json")
        # Storing record info
        feedingText = App.get_running_app().root.screens[0].ids.tabManager.ids.add_records_tab.ids.feed.text
        diapersText = App.get_running_app().root.screens[0].ids.tabManager.ids.add_records_tab.ids.diapers.text
        store.put('record1', feeding=feedingText, diaper=diapersText)
        feeding_int = int(feedingText)
        diapers_int = int(diapersText)
        if feeding_int >= 6:
            if diapers_int < 6:
                # do dehydration
                dismissButton = BoxLayout(orientation='vertical')
                dismissButton.add_widget(Label(text='Reason: Abnormal diaper amount'))
                popupDehydration = Popup(title="RISK ALERT!", content=dismissButton, auto_dismiss=False,size_hint=(.5,.5))
                bothLayout1 = BoxLayout(orientation='horizontal')
                bothLayout1.add_widget(AlertButton(text='Dehydration', size_hint=(1, .5)))
                dismissButton.add_widget(bothLayout1)
                popupDehydration.open()
            else:
                pass
                # ok@
        else:
            dismissButton2 = BoxLayout(orientation='vertical')
            dismissButton2.add_widget(Label(text='Reason: Abnormal diaper and feeding amount'))
            popupAll = Popup(title="RISK ALERT!", content=dismissButton2, auto_dismiss=False,size_hint=(.5,.5))
            bothLayout = BoxLayout(orientation='horizontal')
            bothLayout.add_widget(AlertButton(text='Dehydration', size_hint=(1, .5)))
            bothLayout.add_widget(AlertButton(text='ARI', size_hint=(1, .5)))
            dismissButton2.add_widget(bothLayout)
            popupAll.open()
            # Dehydration and ARI    
    
    
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
        store = JsonStore("D:/Git/Kivy_Apps/First28/profile.json")
        # Storing user information
        store.put('main_profile', name=self.bby_name, weight=self.bby_weight, height=self.bby_height)
        
        # Switching to new screen once the new user profile is implemented
        self.parent.current = 'Menu'
        
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

# UI Template for risk screens          
class RiskLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(RiskLayout, self).__init__(**kwargs)
            
class LabelWrap(Label):
    pass

class First28ScreenManager(ScreenManager):
    pass

class first_28_App(App):
    def build(self):
        store = JsonStore ('D:/Git/Kivy_Apps/First28/profile.json')
        sm = First28ScreenManager()
        if store.exists('main_profile'):
            sm.current = 'Menu'
        else:
            sm.current = 'NewProfile'            
        return sm

if __name__ == '__main__':
    first_28_App().run()
# =================================================NOTES==========================================================
# =============================================================================
#         sm.add_widget(MainMenu(name='Menu')) # [0]
#         sm.add_widget(NewProfile(name='NewProfile')) #[1]
#         sm.add_widget(DehydrationSet(name="Dehydration_Questions")) #[2]
#         sm.add_widget(AriSet(name="Ari_Questions")) #[3]
# =============================================================================