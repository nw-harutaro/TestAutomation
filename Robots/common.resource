*** Settings ***
Library    ExcelLibrary
Library    DateTime
Library    OperatingSystem
Library    Collections
Library    ../Libraries/NetworkDeviceHandler.py
Library    ../Libraries/ExcelKeywords.py
Library    ../Libraries/GenerateHTML.py

*** Variables ***
${DeviceFile}    ${CURDIR}/../Data/device.csv
${CommandFile}    ${CURDIR}/../Data/command.csv
${TestCaseFile}    ${CURDIR}/../Data/test-case.csv
${Timestamp}    ${None}
${Hostname}    ${None}
${IPAddress}    ${None}
${Username}    ${None}
${Password}    ${None}
${EnablePass}    ${None}
${DeviceType}    ${None}

