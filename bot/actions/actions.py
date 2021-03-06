#Standard Packages
import json
import os
from typing import Any, Text, Dict, List

#Rasa Packages
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import Restarted

class ActionMapText(Action):

    def name(self) -> Text:
        return 'action_map_text'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        switch_ = tracker.get_slot('switch_')
        if switch_ is None or switch_ == 'on':
            dispatcher.utter_message(text='Opening up the map for you')
        else:
            dispatcher.utter_message(text='Closing the map for you')
        return [Restarted()]

class ActionNavigationText(Action):

    def name(self) -> Text:
        return 'action_navigation_text'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        switch_ = tracker.get_slot('switch_')
        if switch_ is None or switch_ == 'on':
            dispatcher.utter_message(text='Opening up the navigation menu for you')
        else:
            dispatcher.utter_message(text='Closing the navigation menu for you')
        return [Restarted()]

class ActionTerrainText(Action):

    def name(self) -> Text:
        return 'action_terrain_text'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        switch_ = tracker.get_slot('switch_')
        if switch_ is None or switch_ == 'on':
            dispatcher.utter_message(text='Displaying terrain markers')
        else:
            dispatcher.utter_message(text='Hiding terrain markers')
        return [Restarted()]

class ActionInitiateSample(Action):

    def name(self) -> Text:
        return 'action_initiate_sample'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #create samples folder if it does not exist
        if not os.path.exists('samples'):
            os.mkdir('samples')

        count = len(os.listdir('samples'))
        os.mkdir(f'samples/sample_{count + 1}')
        dispatcher.utter_message(custom={'sample': f'sample_{count + 1}'})
        return []

class ValidateFormSampleTagging(FormValidationAction):

    def name(self) -> Text:
        return 'validate_form_sample_tagging'

    def validate_lighting_conditions(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> Dict[Text, Any]:

        intent = tracker.latest_message['intent'].get('name')

        if intent is not None and intent == 'exit':
            return {'requested_slot': None}
        return {'lighting_conditions': slot_value}

    def validate_outcrop_appearance(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> Dict[Text, Any]:

        intent = tracker.latest_message['intent'].get('name')

        if intent is not None and intent == 'exit':
            return {'requested_slot': None}
        return {'outcrop_appearance': slot_value}

    def validate_mechanism_used(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> Dict[Text, Any]:

        intent = tracker.latest_message['intent'].get('name')

        if intent is not None and intent == 'exit':
            return {'requested_slot': None}
        return {'mechanism_used': slot_value}

    def validate_size_and_shape(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> Dict[Text, Any]:

        intent = tracker.latest_message['intent'].get('name')

        if intent is not None and intent == 'exit':
            return {'requested_slot': None}
        return {'size_and_shape': slot_value}

    def validate_sample_appearance(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> Dict[Text, Any]:

        intent = tracker.latest_message['intent'].get('name')

        if intent is not None and intent == 'exit':
            return {'requested_slot': None}
        return {'sample_appearance': slot_value}

    def validate_geo_interpretation(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> Dict[Text, Any]:

        intent = tracker.latest_message['intent'].get('name')

        if intent is not None and intent == 'exit':
            return {'requested_slot': None}
        return {'geo_interpretation': slot_value}

class ActionSampleTagging(Action):

    def name(self) -> Text:
        return 'action_sample_tagging'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        count = len(os.listdir('samples'))

        #Using this condition to check if sample tagging form was filled or not
        if tracker.get_slot('geo_interpretation') is not None:
            sample_details = {
                'sample_details': {
                    'Lighting Conditions': tracker.get_slot('lighting_conditions'),
                    'Outcrop Appearance': tracker.get_slot('outcrop_appearance'),
                    'Mechanism Used': tracker.get_slot('mechanism_used'),
                    'Size and Shape': tracker.get_slot('size_and_shape'),
                    'Sample Appearance': tracker.get_slot('sample_appearance'),
                    'Geological Interpretation': tracker.get_slot('geo_interpretation')
                }
            }

            json.dump(sample_details['sample_details'], open(f'samples/sample_{count}/sample_details.json', 'w'))
            sample_details['file_name'] = f'sample_{count}/sample_details.json'
            dispatcher.utter_message(custom=sample_details)
            dispatcher.utter_message(response='utter_sample_tagged')

        else:
            dispatcher.utter_message(response='utter_exit')

        dispatcher.utter_message(custom={'sample': False, 'id': count})
        return [Restarted()]

class ActionShowPanel(Action):

    def name(self) -> Text:
        return 'action_show_panel'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        panel = tracker.get_slot('panel')
        switch_ = tracker.get_slot('switch_')
        if switch_ is None:
            switch_ = 'on'
        elif switch_ not in ['on', 'off']:
            panel = switch_
            switch_ = 'on'

        dispatcher.utter_message(custom={'toggle': True, 'feature': panel, 'switch_': switch_})

        return [Restarted()]