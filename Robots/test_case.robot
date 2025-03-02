*** Settings ***
Library    String
Resource    common.resource

*** Variables ***
${LogFolder}    TestResult

*** Test Cases ***
Test-Case
    [Documentation]  テスト実行
    ${ResultSummary}=    Create List
    ${DeviceinfoList}=    Load Device Info From CSV    ${DeviceFile}    ${LogFolder}    ${Timestamp}

    FOR    ${Deviceinfo}    IN    @{DeviceinfoList}
        ${ConnResult}=    Connect Device    ${Deviceinfo}
        Run Keyword And Continue On Failure    Should Be True    ${ConnResult}        
        
        IF    ${ConnResult} == ${True}
            ${TestCaseInfoList}=    Load TestCase From CSV    ${TestCaseFile}    ${Deviceinfo}[Hostname]
            FOR    ${TestCaseInfo}    IN    @{TestCaseInfoList}
                ${Boolean}    ${Output} =    Param Check    ${TestCaseInfo}
                
                ${Result}=    Run Keyword And Continue On Failure    Should Be True    ${Boolean}   
                ${Result}=    Evaluate    'OK' if ${Boolean} else 'NG'
                ${List}=    Create List    ${Deviceinfo}[Hostname]    ${TestCaseInfo}[ExpectedValue]    ${TestCaseInfo}[Operator]    ${Output}    ${Result}
                Append To List    ${ResultSummary}    ${List}
            END
            disconnect
        ELSE
            ${List}=    Create List    ${Deviceinfo}[Hostname]    -    -    -    Connection NG
            Append To List    ${ResultSummary}    ${List} 
        END
    END

    Generate Html Result Summary    ${ResultSummary}    ${Timestamp}
