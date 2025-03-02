*** Settings ***
Resource    common.resource

*** Variables ***
&{Deviceinfo}    Hostname=${Hostname}    IPAddress=${IPAddress}    Username=${Username}    Password=${Password}    EnablePass=${EnablePass}    DeviceType=${DeviceType}

*** Tasks ***
Parse
    [Documentation]  パース実行    
    ${ConnResult}=    Connect Device Nolog    ${Deviceinfo}
    Run Keyword And Continue On Failure    Should Be True    ${ConnResult}

    IF    ${ConnResult} == ${True}
        ${result}=    Send Commands From CSV    ${CommandFile}
        Generate Html Dict Structure    ${result}    ${Timestamp}
        disconnect
    END