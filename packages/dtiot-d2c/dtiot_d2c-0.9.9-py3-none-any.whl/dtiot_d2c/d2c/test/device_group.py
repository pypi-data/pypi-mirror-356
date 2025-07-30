import json
import logging
import sys
import time
from typing import List

import dtiot_d2c.d2c.test.utils as tutils
import dtiot_d2c.dmo as dmo
from dtiot_d2c.d2c import utils as utils
from dtiot_d2c.d2c.application import Application
from dtiot_d2c.d2c.device import Device
from dtiot_d2c.d2c.device.consts import *
from dtiot_d2c.d2c.device_group import DeviceGroup
from dtiot_d2c.d2c.get_response import GetResponse
from dtiot_d2c.d2c.test.application import (TestCase_CreateApplication,
                                            delete_application)
from dtiot_d2c.d2c.test.device import TestCase_CreateDevice, delete_device
from dtiot_d2c.d2c.test.testcli_base import TestCase, TestCLI_Base, TestSet
from dtiot_d2c.d2c.utils import color as color
from dtiot_d2c.dmo import ApiClient

log = logging.getLogger(__name__)
log_level = log.getEffectiveLevel() 

def delete_device_group(api:ApiClient, name:str):
    def operation():      
        if (application := DeviceGroup.get(api, name=name)):
            DeviceGroup.delete(api, name=name)        
    tutils.exec_test(f"Deleting device group {name}", operation)
    
class TestCase_CreateDeviceGroup(TestCase):
    def get_name(self):
        return "Create DeviceGroup"
    
    def run(self):
        name = self.cfg.get("name")

        create_props = self.cfg.get("create_props", None)
        if not create_props:
            raise Exception(f"Cannot find element create_props in configuration.")             

        def operation():   
            response = DeviceGroup.create(self.api, name=name, **create_props)

            if not response:
                return f"Device group {name} hasn't been created"
            
            if log_level <= tutils.INFO:
                GetResponse(response=response).print()      

        tutils.exec_test(f"Creating device group {name}", operation)

    def verify(self):
        name = self.cfg.get("name")

        create_props = self.cfg.get("create_props", None)
        if not create_props:
            raise Exception(f"Cannot find element create_props in configuration.")             
        
        '''
        {
            "cnd": "com.telekom.iot.orchestrator.deviceGroup",
            "rn": "myDeviceGroupFlexContainer000112",
            "nds": [
                "67d940fd665ccfe8ac0b736f"
            ],
            "aes": [
                "6724c9daa3618fe8cb390e24"
            ],
            "ty": 28,
            "cr": "CDevice-Group",
            "tsn": "dtiot:devGr",
            "st": 0,
            "ri": "67f3e2c1b59b8e3d0d98f0de",
            "pi": "67d85887d7ca00dc06b063b6",
            "ct": "20250407T143545,701000",
            "lt": "20250407T143545,701000",
            "m2m:sub": [
                {
                    "rn": "groupflexcontainer-update-subscription",
                    "nct": 1,
                    "enc": {
                        "net": [
                            1,
                            2,
                            3,
                            4
                        ]
                    },
                    "nu": [
                        "http://d2c-device-provisioning.d2c.svc.cluster.local/provisioning/device-group"
                    ],
                    "su": "http://d2c-device-provisioning.d2c.svc.cluster.local:80/provisioning/device-group",
                    "ty": 23,
                    "ri": "67f3e2c1136d98dce0994717",
                    "pi": "67f3e2c1b59b8e3d0d98f0de",
                    "ct": "20250407T143545,831000",
                    "lt": "20250407T143545,831000"
                }
            ]
        }
        '''
        def operation():
            onem2m_dict = dmo.get_resources(api_client=self.api, resourceName=f"device-group/{name}")
            if not onem2m_dict:
                raise Exception(f"Device group resource {name} couldn't be get after creation.")
            else:
                return onem2m_dict

        onem2m_dict:dict = tutils.exec_test(f"Getting ae {name}", operation)

        elem_path = "rn"
        elem_value = name
        def operation():
            if not tutils.call_has_element_value(onem2m_dict, elem_path, elem_value):
                raise Exception(f"Value of element {elem_path} does not meet required value {elem_value}.")
        tutils.exec_test(f"Verifing {elem_path} for {elem_value}", operation)

        for (key, val) in create_props.get("labels", {}).items():
            elem_path = "lbl"
            elem_value = f"{key}:{val}"
            def operation():
                if not tutils.call_has_element_value(onem2m_dict, elem_path, elem_value):
                    raise Exception(f"Value of element {elem_path} does not meet required value {elem_value}.")
            tutils.exec_test(f"Verifing {elem_path} for {elem_value}", operation)
            
class TestCase_ModifyDeviceGroup(TestCase):
    def get_name(self):
        return "Modify DeviceGroup"
    
    def run(self):
        name = self.cfg.get("name")
        modify_props = self.cfg.get("modify_props", None)
        if not modify_props:
            raise Exception(f"Cannot find element modify_props in configuration.")   

        def operation():      
            response = DeviceGroup.update(self.api, name=name, **modify_props)
            
            if not response:
                raise Exception(f"Device group {name} hasn't been modified")
        
            if log_level <= tutils.INFO:
                GetResponse(response=response).print()      

        tutils.exec_test(f"Modifing device group {name}", operation)

    def verify(self):
        name = self.cfg.get("name")
        modify_props = self.cfg.get("modify_props", None)
        if not modify_props:
            raise Exception(f"Cannot find element modify_props in configuration.")   

        def operation():
            onem2m_dict = dmo.get_resources(api_client=self.api, resourceName=f"device-group/{name}")
            if not onem2m_dict:
                raise Exception(f"Device group resource {name} couldn't be get after creation.")
            else:
                return onem2m_dict
        onem2m_dict:dict = tutils.exec_test(f"Getting device group {name}", operation)

        for (key, val) in modify_props.get("labels", {}).items():
            elem_path = "lbl"
            elem_value = f"{key}:{val}"
            def operation():
                if not tutils.call_has_element_value(onem2m_dict, elem_path, elem_value):
                    raise Exception(f"Value of element {elem_path} does not meet required value {elem_value}.")
            tutils.exec_test(f"Verifing {elem_path} for {elem_value}", operation)

class TestCase_DeleteDeviceGroup(TestCase):
    def get_name(self):
        return "Delete DeviceGroup"
    
    def run(self):
        delete_device_group(self.api, self.cfg.get("name"))

    def verify(self):
        name = self.cfg.get("name")

        def operation():
            if dmo.get_resources(api_client=self.api, resourceName=f"device-group/{name}"):
                raise Exception(f"Delete request didn't delete device group {name}.")
        tutils.exec_test(f"Checking if device group {name} has been deleted", operation)
                
class TestCase_AddApplicationsToDeviceGroup(TestCase):
    def __init__(self, api: ApiClient, device_group_cfg:dict, application_cfgs:List[dict], 
                 verify_device_cfgs:List[dict]=None):
        super().__init__(api=api, cfg=device_group_cfg)
        self.application_cfgs = application_cfgs
        self.verify_device_cfgs = verify_device_cfgs

    def get_name(self):
        return "'Add Applications to DeviceGroup"
    
    def run(self):
        device_group_name = self.cfg.get("name")
        self.application_names = []
                
        for application_cfg in self.application_cfgs:
            self.application_names.append(application_cfg.get("name"))
 
        for application_name in self.application_names:
            def operation():
                response = DeviceGroup.update_applications(self.api, 
                                                           name=device_group_name,
                                                           add_names=[application_name]
                                                          )
                if log_level <= tutils.INFO:
                    GetResponse(response=response).print()                 
                    
            tutils.exec_test(f"Adding application name {application_name} to device group {device_group_name}", operation)                
        
        return None

    def verify(self):
        '''
        {
            "cnd": "com.telekom.iot.orchestrator.deviceGroup",
            "rn": "devicegroup02-919",
            "lbl": [
                "deviceType:SDI People Counter"
            ],
            "nds": [],
            "aes": [
                "6802bf3474f6cb71f6fe8f1f"
            ],
            "ty": 28,
            "cr": "Cd2ccli",
            "tsn": "dtiot:devGr",
            "st": 1,
            "ri": "6802bf3074f6cb71f6fe8f1d",
            "pi": "680128d474f6cb71f6fe8e86",
            "ct": "20250418T210800,306000",
            "lt": "20250418T210811,046000",
            "m2m:sub": [
                {
                    "rn": "groupflexcontainer-update-subscription",
                    "nct": 1,
                    "enc": {
                        "net": [
                            1,
                            2,
                            3,
                            4
                        ]
                    },
                    "nu": [
                        "http://d2c-device-provisioning.d2c.svc.cluster.local/provisioning/device-group"
                    ],
                    "su": "http://d2c-device-provisioning.d2c.svc.cluster.local:80/provisioning/device-group",
                    "ty": 23,
                    "ri": "6802bf300aa198ff890ab5d4",
                    "pi": "6802bf3074f6cb71f6fe8f1d",
                    "ct": "20250418T210800,402000",
                    "lt": "20250418T210800,402000"
                }
            ]
        }
        '''
        device_group_name = self.cfg.get("name")
        
        ###
        # Verify if the application names have been added to the device group
        for application_name in self.application_names:
            def operation():
                onem2m_dict = dmo.get_resources(api_client=self.api, resourceName=f"device-group/{device_group_name}")
                if not onem2m_dict:
                    raise Exception(f"Could not load device group resource {device_group_name}.")
                else:
                    return onem2m_dict
            onem2m_dict:dict = tutils.exec_test(f"Getting device group {device_group_name}", operation)
                    
            def operation():
                if application_name not in onem2m_dict["aes"]:
                    raise Exception(f"Could not find application id {application_name} in device group.")
            tutils.exec_test(f"Verifying application id {application_name}", operation)

        ###
        # Verify if the application subscriptions have been added to the device communication
        # message received container
        if not self.verify_device_cfgs:
            return
        
        for device_cfg in self.verify_device_cfgs:
            device_name = device_cfg.get("name")

            # Name of subscription: <device-group-name>-<application-name>-<device-name>,
            for application_cfg in self.application_cfgs:
                application_name = application_cfg.get("name")
                
                n = f"device-communication/{device_name}/received-msg/{device_group_name}-{application_name}-{device_name}"
                def operation():
                    onem2m_dict = dmo.get_resources(api_client=self.api, resourceType="subscription", resourceName=n)
                    if not onem2m_dict:
                        raise Exception(f"Couldn't get subscription {n}.")
                    else:
                        return onem2m_dict
                onem2m_dict:dict = tutils.exec_test(f"Getting application subscription {n}", operation)           
        
class TestCase_RemoveApplicationsFromDeviceGroup(TestCase):
    def __init__(self, api: ApiClient, device_group_cfg:dict, 
                 application_cfgs:List[dict], verify_device_cfgs:List[dict]=None):
        super().__init__(api=api, cfg=device_group_cfg)
        self.application_cfgs = application_cfgs
        self.verify_device_cfgs = verify_device_cfgs
        self.application_names:List[str] = []
        
    def get_name(self):
        return "Remove Applications from DeviceGroup"
    
    def run(self):
        device_group_name = self.cfg.get("name")

        for application_cfg in self.application_cfgs:
            self.application_names.append(application_cfg.get("name"))
 
        def operation():
            response = DeviceGroup.update_applications(self.api, 
                                                       name=device_group_name,
                                                       remove_names=self.application_names
                                                      )
            if log_level <= tutils.INFO:
                GetResponse(response=response).print()                 
                
        tutils.exec_test(f"Removing application names {self.application_names} from device group {device_group_name}", operation)                
        
        return None

    def verify(self):
        '''
        {
            "cnd": "com.telekom.iot.orchestrator.deviceGroup",
            "rn": "devicegroup02-919",
            "lbl": [
                "deviceType:SDI People Counter"
            ],
            "nds": [],
            "aes": [
                "6802bf3474f6cb71f6fe8f1f"
            ],
            "ty": 28,
            "cr": "Cd2ccli",
            "tsn": "dtiot:devGr",
            "st": 1,
            "ri": "6802bf3074f6cb71f6fe8f1d",
            "pi": "680128d474f6cb71f6fe8e86",
            "ct": "20250418T210800,306000",
            "lt": "20250418T210811,046000",
            "m2m:sub": [
                {
                    "rn": "groupflexcontainer-update-subscription",
                    "nct": 1,
                    "enc": {
                        "net": [
                            1,
                            2,
                            3,
                            4
                        ]
                    },
                    "nu": [
                        "http://d2c-device-provisioning.d2c.svc.cluster.local/provisioning/device-group"
                    ],
                    "su": "http://d2c-device-provisioning.d2c.svc.cluster.local:80/provisioning/device-group",
                    "ty": 23,
                    "ri": "6802bf300aa198ff890ab5d4",
                    "pi": "6802bf3074f6cb71f6fe8f1d",
                    "ct": "20250418T210800,402000",
                    "lt": "20250418T210800,402000"
                }
            ]
        }
        '''
        name = self.cfg.get("name")
        
        def operation():
            onem2m_dict = dmo.get_resources(api_client=self.api, resourceName=f"device-group/{name}")
            if not onem2m_dict:
                raise Exception(f"Could not load device group resource {name}.")
            else:
                return onem2m_dict
        onem2m_dict:dict = tutils.exec_test(f"Getting device group {name}", operation)
                
        for application_name in self.application_names:
            def operation():
                if application_name in onem2m_dict["aes"]:
                    raise Exception(f"Application name {application_name} has NOT been removed from device group.")
            tutils.exec_test(f"Verifying application name {application_name}", operation)

        ###
        # Verify if the application subscriptions have been removed from the device communication
        # message received container
        if not self.verify_device_cfgs:
            return
        
        for device_cfg in self.verify_device_cfgs:
            device_name = device_cfg.get("name")

            # Name of subscription: <device-group-name>-<application-name>-<device-name>,
            for application_cfg in self.application_cfgs:
                application_name = application_cfg.get("name")
                
                n = f"device-communication/{device_name}/received-msg/{name}-{application_name}-{device_name}"
                def operation():
                    onem2m_dict = dmo.get_resources(api_client=self.api, resourceType="subscription", resourceName=n)
                    if onem2m_dict:
                        raise Exception(f"Application subscription {n} has not been removed.")
                tutils.exec_test(f"Verifying if application subscription {n} has been removed", operation)           

class TestCase_AddDevicesToDeviceGroup(TestCase):
    def __init__(self, api: ApiClient, device_group_cfg:dict, 
                 device_cfgs:List[dict], verify_application_cfgs:List[dict]=None):
        super().__init__(api=api, cfg=device_group_cfg)
        self.device_cfgs = device_cfgs
        self.verify_application_cfgs = verify_application_cfgs
        self.device_names = []
        
    def get_name(self):
        return "'Add Device to DeviceGroup"
    
    def run(self):
        device_group_name = self.cfg.get("name")

        for device_cfg in self.device_cfgs:
            self.device_names.append(device_cfg.get("name"))
 
        for device_name in self.device_names:
            def operation():
                response = DeviceGroup.update_devices(self.api, 
                                                       name=device_group_name,
                                                       add_names=[device_name]
                                                      )
                if log_level <= tutils.INFO:
                    GetResponse(response=response).print()                 
                    
            tutils.exec_test(f"Adding device name {device_name} to device group {device_group_name}", operation)                
        
        return None


    def verify(self):
        '''
        device-communication/<device-name>/
        {
            "rn": "device01-916",
            ....
            "m2m:cnt": [
                ...
                {
                    "mbs": 1000000,
                    "mni": 100,
                    "rn": "received-msg",
                    "ty": 3,
                    "st": 0,
                    "cbs": 0,
                    "cni": 0,
                    "cr": "CDevice-Provisioning",
                    "ri": "680b565083dba99abdafb5d3",
                    "pi": "680b565083dba99abdafb5cd",
                    "ct": "20250425T093056,295000",
                    "lt": "20250425T093056,295000",
                    "m2m:sub": [
                        {
                            "rn": "devicegroup02-916-devicegroup02-app1-916-device01-916",
                            "nct": 1,
                            "enc": {
                                "net": [
                                    1,
                                    2,
                                    3,
                                    4
                                ]
                            },
                            "nu": [
                                "d2c-dev-1/devicegroup02-app1-916"
                            ],
                            "su": "d2c-dev-1/devicegroup02-app1-916",
                            "ty": 23,
                            "ri": "680b566083dba99abdafb5df",
                            "pi": "680b565083dba99abdafb5d3",
                            "ct": "20250425T093112,448000",
                            "lt": "20250425T093112,448000"
                        }
                    ]
                },
                ...
            ]
        }        
        '''
        device_group_name = self.cfg.get("name")

        # Load device group
        def operation():
            onem2m_dict = dmo.get_resources(api_client=self.api, resourceName=f"device-group/{device_group_name}")
            if not onem2m_dict:
                raise Exception(f"Could not load device group resource {device_group_name}.")
            else:
                return onem2m_dict
        onem2m_dict:dict = tutils.exec_test(f"Getting device group {device_group_name}", operation)
          
        # Check if the device ids can be found in the device group   
        for device_name in self.device_names:
            def operation():
                if device_name not in onem2m_dict["nds"]:
                    raise Exception(f"Could not find device id {device_name} in device group.")
            tutils.exec_test(f"Verifying device id {device_name}", operation)
            
        ###
        # Check the application subscription in the received message device communication container
        # Name of subscription: <device-group-name>-<application-name>-<device-name>,
        if not self.verify_application_cfgs:
            return
        
        for device_cfg in self.device_cfgs:
            device_name = device_cfg.get("name")
            
            for application_cfg in self.verify_application_cfgs:
                application_name = application_cfg.get("name")
                
                n = f"device-communication/{device_name}/received-msg/{device_group_name}-{application_name}-{device_name}"
                def operation():
                    onem2m_dict = dmo.get_resources(api_client=self.api, resourceType="subscription", resourceName=n)
                    if not onem2m_dict:
                        raise Exception(f"Couldn't get subscription {n}.")
                    else:
                        return onem2m_dict
                onem2m_dict:dict = tutils.exec_test(f"Getting application subscription {n}", operation)   

class TestCase_RemoveDevicesFromDeviceGroup(TestCase):
    def __init__(self, api: ApiClient, device_group_cfg:dict, 
                 device_cfgs:List[dict], verify_application_cfgs:List[dict]=None):
        super().__init__(api=api, cfg=device_group_cfg)
        self.device_cfgs = device_cfgs
        self.verify_application_cfgs = verify_application_cfgs
        self.device_names:List[str] = []
        
    def get_name(self):
        return "Remove Devices from DeviceGroup"

    def run(self):
        device_group_name = self.cfg.get("name")

        for device_cfg in self.device_cfgs:
            self.device_names.append(device_cfg.get("name"))
 
        def operation():
            response = DeviceGroup.update_devices(self.api, 
                                                  name=device_group_name,
                                                  remove_names=self.device_names
                                                 )
            if log_level <= tutils.INFO:
                GetResponse(response=response).print()                 
                
        tutils.exec_test(f"Removing device names {self.device_names} from device group {device_group_name}", operation)   

    def verify(self):
        '''
        {
            "cnd": "com.telekom.iot.orchestrator.deviceGroup",
            "rn": "devicegroup02-919",
            "lbl": [
                "deviceType:SDI People Counter"
            ],
            "nds": [],
            "aes": [
                "6802bf3474f6cb71f6fe8f1f"
            ],
            "ty": 28,
            "cr": "Cd2ccli",
            "tsn": "dtiot:devGr",
            "st": 1,
            "ri": "6802bf3074f6cb71f6fe8f1d",
            "pi": "680128d474f6cb71f6fe8e86",
            "ct": "20250418T210800,306000",
            "lt": "20250418T210811,046000",
            "m2m:sub": [
                {
                    "rn": "groupflexcontainer-update-subscription",
                    "nct": 1,
                    "enc": {
                        "net": [
                            1,
                            2,
                            3,
                            4
                        ]
                    },
                    "nu": [
                        "http://d2c-device-provisioning.d2c.svc.cluster.local/provisioning/device-group"
                    ],
                    "su": "http://d2c-device-provisioning.d2c.svc.cluster.local:80/provisioning/device-group",
                    "ty": 23,
                    "ri": "6802bf300aa198ff890ab5d4",
                    "pi": "6802bf3074f6cb71f6fe8f1d",
                    "ct": "20250418T210800,402000",
                    "lt": "20250418T210800,402000"
                }
            ]
        }
        '''
        name = self.cfg.get("name")
        
        def operation():
            onem2m_dict = dmo.get_resources(api_client=self.api, resourceName=f"device-group/{name}")
            if not onem2m_dict:
                raise Exception(f"Could not load device group resource {name}.")
            else:
                return onem2m_dict
        onem2m_dict:dict = tutils.exec_test(f"Getting device group {name}", operation)
        
        for device_name in self.device_names:      
            def operation():
                if device_name in onem2m_dict["nds"]:
                    raise Exception(f"Device id {device_name} has NOT been removed from device group.")
            tutils.exec_test(f"Verifying device id {device_name}", operation)
            
        ###
        # Check the application subscription in the received message device communication container
        # Name of subscription: <device-group-name>-<application-name>-<device-name>,
        if not self.verify_application_cfgs:
            return
        
        for device_cfg in self.device_cfgs:
            device_name = device_cfg.get("name")
            
            for application_cfg in self.verify_application_cfgs:
                application_name = application_cfg.get("name")
                
                n = f"device-communication/{device_name}/received-msg/{name}-{application_name}-{device_name}"
                def operation():
                    onem2m_dict = dmo.get_resources(api_client=self.api, resourceType="subscription", resourceName=n)
                    if onem2m_dict:
                        raise Exception(f"Application subscription {n} still exists.")
                tutils.exec_test(f"Verifying if application subscription {n} has been deleted", operation)   
class TestCase_DeleteDeviceGroup(TestCase):
    def get_name(self):
        return "Delete DeviceGroup"
    
    def run(self):
        delete_device_group(self.api, self.cfg.get("name"))

    def verify(self):
        name = self.cfg.get("name")

        def operation():
            if dmo.get_resources(api_client=self.api, resourceName=f"device-group/{name}"):
                raise Exception(f"Delete request didn't delete device group {name}.")
        tutils.exec_test(f"Checking if device group {name} has been deleted", operation)
#MARK: Tests01
###########################################################################            
# Performs the following test cases:
# - create device group
# - modify device group
# - delete device group
###########################################################################    
class Tests01(TestSet):
    def __init__(self, api: ApiClient):
        super().__init__(api, "TestGroup Tests 01")
    
    def get_sample_configuration_varname(self)->str:
        return "DeviceGroup01Cfg"

    def get_test_cases(self, cfg:dict)->List[TestCase]:
        return [
            TestCase_CreateDeviceGroup(api=self.api, cfg=cfg),
            TestCase_ModifyDeviceGroup(api=self.api, cfg=cfg),
            TestCase_DeleteDeviceGroup(api=self.api, cfg=cfg),
        ]
        
    def test_pre_cleanup(self, cfg:dict)->str:
        delete_device_group(self.api, cfg.get("name"))

    def test_post_cleanup(self, cfg:dict)->str:
        delete_device_group(self.api, cfg.get("name"))

class Tests01_CLI(TestCLI_Base):
    def get1LineHelp(self):
        return "Runs device group test case: create, modify and delete device group."
    def get_test_set(self, api: ApiClient):
        return Tests01(api)
#MARK: Tests02
###########################################################################            
# Performs the following test cases:
# - create device group
# - create application
# - create application
# - remove application
# - add 2 applications 
# - remove application
# - remove application
###########################################################################    
class Tests02(TestSet):
    def __init__(self, api: ApiClient):
        super().__init__(api, "TestGroup Tests 02")
    
    def get_sample_configuration_varname(self)->str:
        return "DeviceGroup02Cfg"

    def get_test_cases(self, cfg:dict)->List[TestCase]:
        return [
            TestCase_CreateDeviceGroup(api=self.api, cfg=cfg),
            TestCase_CreateApplication(api=self.api, cfg=cfg.get("application_1")),
            TestCase_CreateApplication(api=self.api, cfg=cfg.get("application_2")),
            TestCase_AddApplicationsToDeviceGroup(api=self.api, 
                                                  device_group_cfg=cfg, 
                                                  application_cfgs=[cfg.get("application_1")]),
            TestCase_RemoveApplicationsFromDeviceGroup(api=self.api, 
                                                      device_group_cfg=cfg, 
                                                      application_cfgs=[cfg.get("application_1")]),
            TestCase_AddApplicationsToDeviceGroup(api=self.api, 
                                                  device_group_cfg=cfg, 
                                                  application_cfgs=[cfg.get("application_1"), 
                                                                    cfg.get("application_2")]),
            TestCase_RemoveApplicationsFromDeviceGroup(api=self.api, 
                                                      device_group_cfg=cfg, 
                                                      application_cfgs=[cfg.get("application_1")]),
            TestCase_RemoveApplicationsFromDeviceGroup(api=self.api, 
                                                      device_group_cfg=cfg, 
                                                      application_cfgs=[cfg.get("application_2")]),
        ]
        
    def test_pre_cleanup(self, cfg:dict)->str:
        delete_device_group(self.api, cfg.get("name"))
        delete_application(self.api, cfg.get("application_1").get("name"))
        delete_application(self.api, cfg.get("application_2").get("name"))

    def test_post_cleanup(self, cfg:dict)->str:
        delete_device_group(self.api, cfg.get("name"))
        delete_application(self.api, cfg.get("application_1").get("name"))
        delete_application(self.api, cfg.get("application_2").get("name"))

class Tests02_CLI(TestCLI_Base):
    def get1LineHelp(self):
        return "Runs device group test case: add applications, remove applications without devices."

    def get_test_set(self, api: ApiClient):
        return Tests02(api)
#MARK: Tests03
###########################################################################            
# Performs the following test cases:
# - create device group
# - create device
# - create device
# - add device to device group
# - remove device group
# - add 2 devices to device group
# - remove device group
# - remove device group
###########################################################################    
class Tests03(TestSet):
    def __init__(self, api: ApiClient):
        super().__init__(api, "TestGroup Tests 03")
    
    def get_sample_configuration_varname(self)->str:
        return "DeviceGroup02Cfg"

    def get_test_cases(self, cfg:dict)->List[TestCase]:
        return [
            TestCase_CreateDeviceGroup(api=self.api, cfg=cfg),
            
            TestCase_CreateDevice(api=self.api, cfg=cfg.get("device_1")),
            TestCase_CreateDevice(api=self.api, cfg=cfg.get("device_2")),
            TestCase_AddDevicesToDeviceGroup(api=self.api, 
                                            device_group_cfg=cfg, 
                                            device_cfgs=[cfg.get("device_1")],
                                            verify_application_cfgs=None),
            TestCase_RemoveDevicesFromDeviceGroup(api=self.api, 
                                                  device_group_cfg=cfg, 
                                                  device_cfgs=[cfg.get("device_1")]),
            TestCase_AddDevicesToDeviceGroup(api=self.api, 
                                            device_group_cfg=cfg, 
                                            device_cfgs=[cfg.get("device_1"), cfg.get("device_2")],
                                            verify_application_cfgs=None),
            TestCase_RemoveDevicesFromDeviceGroup(api=self.api, 
                                                  device_group_cfg=cfg, 
                                                  device_cfgs=[cfg.get("device_1"), cfg.get("device_2")])
        ]
        
    def test_pre_cleanup(self, cfg:dict)->str:
        delete_device_group(self.api, cfg.get("name"))
        delete_device(self.api, cfg.get("device_1").get("name"))
        delete_device(self.api, cfg.get("device_2").get("name"))

    def test_post_cleanup(self, cfg:dict)->str:
        delete_device_group(self.api, cfg.get("name"))
        delete_device(self.api, cfg.get("device_1").get("name"))
        delete_device(self.api, cfg.get("device_2").get("name"))
class Tests03_CLI(TestCLI_Base):
    def get1LineHelp(self):
        return "Runs device group test case: add devices, remove devices without applications."

    def get_test_set(self, api: ApiClient):
        return Tests03(api)
#MARK: Tests04
###########################################################################            
# Performs the following test cases:
# - create device group
# - create application 
# - create device
# - add applications to device group
# - add device to device group
# - remove device from device group
# - add device to device group
# - remove application from device group 
###########################################################################    
class Tests04(TestSet):
    def __init__(self, api: ApiClient):
        super().__init__(api, "TestGroup Tests 04")
    
    def get_sample_configuration_varname(self)->str:
        return "DeviceGroup02Cfg"

    def get_test_cases(self, cfg:dict)->List[TestCase]:
        return [
            TestCase_CreateDeviceGroup(api=self.api, cfg=cfg),
            TestCase_CreateApplication(api=self.api, cfg=cfg.get("application_1")),
            TestCase_CreateApplication(api=self.api, cfg=cfg.get("application_2")),
            TestCase_CreateDevice(api=self.api, cfg=cfg.get("device_1")),
            TestCase_CreateDevice(api=self.api, cfg=cfg.get("device_2")),
            TestCase_AddApplicationsToDeviceGroup(api=self.api, 
                                                  device_group_cfg=cfg, 
                                                  application_cfgs=[cfg.get("application_1"), cfg.get("application_2")],
                                                  verify_device_cfgs=None),
            TestCase_AddDevicesToDeviceGroup(api=self.api, 
                                            device_group_cfg=cfg, 
                                            device_cfgs=[cfg.get("device_1"), cfg.get("device_2")],
                                            verify_application_cfgs=[cfg.get("application_1"), cfg.get("application_2")]),
            TestCase_RemoveDevicesFromDeviceGroup(api=self.api, 
                                                  device_group_cfg=cfg, 
                                                  device_cfgs=[cfg.get("device_1")],
                                                  verify_application_cfgs=[cfg.get("application_1")]),
            TestCase_RemoveApplicationsFromDeviceGroup(api=self.api, 
                                                      device_group_cfg=cfg, 
                                                      application_cfgs=[cfg.get("application_1")],
                                                      verify_device_cfgs=[cfg.get("device_1")]),
        ]
        
    def test_pre_cleanup(self, cfg:dict)->str:
        delete_device_group(self.api, cfg.get("name"))
        delete_application(self.api, cfg.get("application_1").get("name"))
        delete_device(self.api, cfg.get("device_1").get("name"))

    def test_post_cleanup(self, cfg:dict)->str:
        delete_device_group(self.api, cfg.get("name"))
        delete_application(self.api, cfg.get("application_1").get("name"))
        delete_device(self.api, cfg.get("device_1").get("name"))

class Tests04_CLI(TestCLI_Base):
    def get1LineHelp(self):
        return "Runs device group test case: add and remove application and device."

    def get_test_set(self, api: ApiClient):
        return Tests04(api)    
