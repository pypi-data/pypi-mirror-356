Device01Cfg = {
    "name":"device01-%RUNID%",
    "create_props" : {
        "manufacturer":"PSsystec",
        "model":"Smartbox Mini",
        "sub_model":"NB-IoT",
        "iccid": "89374121317959919924",
        "hardware_version":"2024.1 PC r1",
        "country":"DE",
        "description":"Das ist eine Beschreibung.",
        "label":"this is a label" ,
        "device_type":"Pretty Device" ,
        "device_name":"This is the name of the device",
        "firmware_version":"fw 1.0.1",
        "software_version":"sw 2.0.1",
        "os_version":"os 3.0.1",
        "location":"geo:25.245470,51.454009" ,
        "protocols":["LWM2M"] ,
        "uplink_properties": {"address":"Kuckhoffstr 114A, 13156 Berlin"},
        "device_properties": {"lastMaintenance":"25.3.2025 1300", "prop2":"value2"},
        "credentials_id": "device01-%RUNID%",
        "credentials_secret": "Q3hhc21FTUw3NFNiUlIzUw=="
    },
    "modify_props" : {
        "manufacturer":"x PSsystec",
        "model":"x Smartbox Mini",
        "sub_model":"x NB-IoT",
        "iccid": "99999999317959919924",
        "hardware_version":"x 2024.1 PC r1",
        "country":"XX",
        "description":"x Das ist eine Beschreibung.",
        "label":"x this is a label" ,
        "device_type":"x Pretty Device" ,
        "device_name":"Hallo die Waldfee device_name",
        "firmware_version":"x fw 1.0.1",
        "software_version":"x sw 2.0.1",
        "os_version":"x os 3.0.1",
        "location":"geo:88.999999,88.999999" ,
        "protocols":["LWM2M"] ,
        "uplink_properties": {"address":"xx Kuckhoffstr 114A, 13156 Berlin", "location":"Berlin"},
        "device_properties": {"lastMaintenance":"25.3.2025 1300","Status": "Out of order"},

        #Update lwm2m cridentials is not supported yet via d2ccli
        #"credentials_id": "x device01-%RUNID%",
        #"credentials_secret": "x Q3hhc21FTUw3NFNiUlIzUw=="
    }    
} 
Device02Cfg = {
    "name":"device02-%RUNID%",
    "create_props" : {
        "manufacturer":"PSsystec",
        "model":"Smartbox Mini",
        "sub_model":"NB-IoT",
        "iccid": "89374121317959919924",
        "hardware_version":"2024.1 PC r1",
        "country":"DE",
        "description":"Das ist eine Beschreibung.",
        "label":"this is a label" ,
        "device_type":"Pretty Device" ,
        "firmware_version":"fw 1.0.1",
        "software_version":"sw 2.0.1",
        "os_version":"os 3.0.1",
        "location":"geo:25.245470,51.454009" ,
        "protocols":["LWM2M"] ,
        "uplink_properties": {"address":"Kuckhoffstr 114A, 13156 Berlin"},
        "device_properties": {"lastMaintenance":"25.3.2025 1300"},
        "credentials_id": "device01-%RUNID%",
        "credentials_secret": "Q3hhc21FTUw3NFNiUlIzUw=="
    }
} 

Application01Cfg = {
    "name":"application01-%RUNID%",
    "create_props" : {
        "application_type":"webHook",
        "urls": ["https://api.scs.iot.telekom.com/message-monitor"],
        "connection_properties": {"Auth":"dfadfdsafasdf", "another-token":"88888888"}
    }, 
    "modify_props" : {    
        "urls": ["https://dev.scs.iot.telekom.com/scs-callback-dummy"],
        "connection_properties": {"Auth":"88888888", "another-token":"dfadfdsafasdf"}
    }
}

DeviceGroup01Cfg = {
    "name":"devicegroup01-%RUNID%", 
    "create_props" : {
        "labels":{"deviceType":"SDI People Counter"},
        "device_ids": [],
        "application_ids": []
    },
    "modify_props":{
        "labels":{"deviceType":"SDI People Counter, ELSYS", "street":"Kuckhoffstr."},
        "device_ids": [],
        "application_ids": []
    }
}

DeviceGroup02Cfg = {
    "name":"devicegroup02-%RUNID%", 
    "create_props" : {
        "labels":{"deviceType":"SDI People Counter"},
        "device_ids": [],
        "application_ids": []
    },
    "application_1": {
        "name":"devicegroup02-app1-%RUNID%",
        "create_props":{
            "urls": ["https://api.scs.iot.telekom.com/message-monitor"],
            "labels": {"customerKey":"CUST-001"},        
        }
    },
    "application_2":{
        "name":"devicegroup02-app2-%RUNID%",
        "create_props":{
            "urls": ["https://dev.scs.iot.telekom.com/scs-callback-dummy"],
            "labels": {"customerKey":"CUST-099", "costCenter":"999888"},        
        }
    },
    "device_1": Device01Cfg,
    "device_2": Device02Cfg
}