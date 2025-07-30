*** Settings ***
Library    SeleniumLibrary

*** Keywords ***
Open QAppuccino Login Page
    [Arguments]    ${url}    ${browser}
    Open Browser    ${url}    ${browser}
    Maximize Browser Window

Input QAppuccino Username
    [Arguments]    ${username_locator}    ${username}
    Input Text    ${username_locator}    ${username}

Input QAppuccino Password
    [Arguments]    ${password_locator}    ${password}
    Input Text    ${password_locator}    ${password}

Click QAppuccino Login
    [Arguments]    ${login_button_locator}
    Click Button    ${login_button_locator}

Verify QAppuccino Login Success
    [Arguments]    ${dashboard_locator}
    Page Should Contain Element    ${dashboard_locator}

QAppuccino Login Flow
    [Arguments]
    ...    ${url}
    ...    ${browser}
    ...    ${username_locator}
    ...    ${password_locator}
    ...    ${login_button_locator}
    ...    ${dashboard_locator}
    ...    ${username}
    ...    ${password}
    Open QAppuccino Login Page    ${url}    ${browser}
    Input QAppuccino Username     ${username_locator}    ${username}
    Input QAppuccino Password     ${password_locator}    ${password}
    Click QAppuccino Login        ${login_button_locator}
    Verify QAppuccino Login Success    ${dashboard_locator}

Close QAppuccino Browser
    Close Browser
