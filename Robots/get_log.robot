*** Settings ***
Resource    common.resource

*** Variables ***
${LogFolder}    Text_Based_Log

*** Tasks ***
Get-Log
    [Documentation]  ログ取得実行
    ${DeviceinfoList}=    Load Device Info From CSV    ${DeviceFile}    ${LogFolder}    ${Timestamp}

    FOR    ${Deviceinfo}    IN    @{DeviceinfoList}
        ${ConnResult}=    Connect Device    ${Deviceinfo}
        Run Keyword And Continue On Failure    Should Be True    ${ConnResult}        
        
        IF    ${ConnResult} == ${True}
            Send Commands From CSV    ${CommandFile}
            disconnect
        END
    END
