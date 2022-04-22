import os
# from pprint import pprint

from waapi import WaapiClient, CannotConnectToWaapiException


def get_object_id(object_path):
    try:
        args = {
            "from": {"path": object_path}
        }
        opts = {
            "return": [id]
        }
        return client.call("ak.wwise.core.object.get", args, options=opts)['return'][0][id]
    except TypeError:
        print("'NoneType' object is not subscriptable")


def get_selected_id():
    selected_id = []
    for obj in client.call("ak.wwise.ui.getSelectedObjects")['objects']:
        selected_id.append(obj['id'])
    if len(selected_id) == 1:
        return selected_id[0]
    else:
        return selected_id


def get_object_info(object_id, keyword):
    try:
        args = {
            "from": {"id": [object_id]}
        }
        opts = {
            "return": [keyword]
        }
        return client.call("ak.wwise.core.object.get", args, options=opts)['return'][0][keyword]
    except TypeError:
        print("'NoneType' object is not subscriptable")


def set_object_property(object_path_id, object_property, value):
    try:
        args = {
            "object": object_path_id,
            "property": object_property,
            "value": value
        }
        return client.call("ak.wwise.core.object.setProperty", args)
    except TypeError:
        print("'NoneType' object is not subscriptable")


def set_object_reference(object_path_id, reference_type, reference_path_id):
    try:
        args = {
            "object": object_path_id,
            "reference": reference_type,
            "value": reference_path_id
        }
        return client.call("ak.wwise.core.object.setReference", args)
    except TypeError:
        print("'NoneType' object is not subscriptable")


def set_object_randomizer(object_path_id, object_property, randomizer_min, randomizer_max):
    try:
        args = {
            "object": object_path_id,
            "property": object_property,
            "enabled": True,
            "min": randomizer_min,
            "max": randomizer_max
        }
        return client.call("ak.wwise.core.object.setRandomizer", args)
    except TypeError:
        print("'NoneType' object is not subscriptable")


def set_switch_assignment(object_path_id, state_switch_path_id):
    try:
        args = {
            "child": object_path_id,
            "stateOrSwitch": state_switch_path_id
        }
        return client.call("ak.wwise.core.switchContainer.addAssignment", args)
    except TypeError:
        print("'NoneType' object is not subscriptable")


def set_attenuation_curve(attenuation_path_id, attenuation_curve_type, attenuation_curve_points):
    try:
        args = {
            "object": attenuation_path_id,
            "curveType": attenuation_curve_type,
            # VolumeDryUsage
            # VolumeWetGameUsage
            # VolumeWetUserUsage
            # LowPassFilterUsage
            # HighPassFilterUsage
            # SpreadUsage
            # FocusUsage
            "use": "Custom",
            "points": attenuation_curve_points
            # Constant
            # Linear
            # Log3
            # Log2
            # Log1
            # InvertedSCurve
            # SCurve
            # Exp1
            # Exp2
            # Exp3
        }
        return client.call("ak.wwise.core.object.setAttenuationCurve", args)
    except TypeError:
        print("'NoneType' object is not subscriptable")


def create_object(parent_path_id, object_type, object_name):
    try:
        args = {
            "parent": parent_path_id,
            "type": object_type,
            "name": object_name
        }
        return client.call("ak.wwise.core.object.create", args)
    except TypeError:
        print("'NoneType' object is not subscriptable")


# object_path: \\Actor-Mixer Hierarchy\\Default Work Unit\\<Random Container>MyContainer\\<Sound>MySound
def file_import(audio_file, object_path):
    args = {
        "default": {
            "importLanguage": "SFX"
        },
        "imports": [
            {
                "audioFile": audio_file,
                "objectPath": object_path
            }
        ]
    }
    opts = {
        "return": [
            "id", "name", "path"
        ]
    }
    return client.call("ak.wwise.core.audio.import", args, options=opts)


# Command Line Interface
def interface():
    print("WWAPI Demo: Wwise Audio Importer")
    print("This script import audio file to \\Actor-Mixer Hierarchy\\Default Work Unit\\")
    print("Container Type? \"0\" for Sequence Container and \"1\" for Random Container")
    container_type = input()
    print("Audio Folder Path?")
    path = input()

    return container_type, os.path.abspath(path)


# ----
# 测试
try:
    client = WaapiClient()
except CannotConnectToWaapiException:
    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")
else:
    # Input
    m_container_type, m_path = interface()

    # Ref Path
    actor_mixer_name = m_path.rsplit("\\", 1)[1]
    actor_mixer_path = "\\Actor-Mixer Hierarchy\\Default Work Unit\\" + actor_mixer_name
    bus_parent_path = "\\Master-Mixer Hierarchy\\Default Work Unit\\Master Audio Bus"
    bus_path = bus_parent_path + "\\" + actor_mixer_name

    # Create Bus
    create_object(bus_parent_path, "Bus", actor_mixer_name)
    print(actor_mixer_name + "<Bus>")

    # Create ActorMixer and Set Bus
    create_object("\\Actor-Mixer Hierarchy\\Default Work Unit\\", "ActorMixer", actor_mixer_name)
    set_object_reference(actor_mixer_path, "OutputBus", bus_path)
    set_object_property(actor_mixer_path, "3DSpatialization", 2)
    print("  " + actor_mixer_name + "<ActorMixer>")

    # Create Attenuation
    attenuation_path = "\\Attenuations\\Default Work Unit\\" + actor_mixer_name
    create_object("\\Attenuations\\Default Work Unit", "Attenuation", actor_mixer_name)
    m_points = [{'shape': 'Log3', 'x': 0.0, 'y': 0.0},
                {'shape': 'Linear', 'x': 50.0, 'y': -200.0},
                {'shape': 'Linear', 'x': 100.0, 'y': -200.0}]
    set_attenuation_curve(attenuation_path, "VolumeDryUsage", m_points)
    set_object_reference(actor_mixer_path, "Attenuation", attenuation_path)

    # Create Switch Container
    switch_container_path = actor_mixer_path + "\\" + actor_mixer_name
    create_object(actor_mixer_path, "SwitchContainer", actor_mixer_name)
    print("    " + actor_mixer_name + " <Switch Container>")

    # Create Switch Group
    switch_group_path = "\\Switches\\Default Work Unit\\" + actor_mixer_name
    create_object("\\Switches\\Default Work Unit", "SwitchGroup", actor_mixer_name)
    set_object_reference(switch_container_path, "SwitchGroupOrStateGroup", switch_group_path)

    default_switch = ""
    # Import Audio Files and Create Containers
    for container in os.listdir(m_path):
        # Create Containers
        container_path = switch_container_path + "\\" + container
        create_object(switch_container_path, "RandomSequenceContainer", container)
        set_object_property(container_path, "RandomOrSequence", m_container_type)

        # Set Random Property
        if m_container_type == "1":
            set_object_property(container_path, "NormalOrShuffle", 0)
            set_object_property(container_path, "RandomAvoidRepeatingCount", 2)
            print("      " + container + " <Random Container>")
        else:
            print("      " + container + " <Sequence Container>")

        # Set Random Pitch and Volume
        set_object_randomizer(container_path, "Pitch", -100, 100)
        set_object_randomizer(container_path, "Volume", -2, 2)

        # Create Switches
        create_object(switch_group_path, "Switch", container)
        switch_path = switch_group_path + "\\" + container
        set_switch_assignment(container_path, switch_path)
        default_switch = switch_path

        for audio in os.listdir(os.path.join(m_path, container)):
            # Import Audio
            m_object_name = os.path.splitext(audio)[0]
            m_audio_file = os.path.join(m_path, container, audio)
            m_object_path = container_path + "\\<Sound>" + m_object_name
            file_import(m_audio_file, m_object_path)
            print("        " + m_object_name)
    set_object_reference(switch_container_path, "DefaultSwitchOrState", default_switch)
    # SUCCESS
    print("Import Success")

    client.disconnect()
