import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15
import QtQuick.LocalStorage 2.15

// Cleaned + consistently styled + proper layout
ApplicationWindow {
    id: window
    visible: true
    width: 650
    height: 850
    minimumWidth: 480
    minimumHeight: 700
    color: bgTransparent // transparent for glassy effect (requires compositor)
    flags: Qt.FramelessWindowHint | Qt.Window
    title: "Riot Auto Login"

    // ===== Theme =====
    property string primary:   "#0A1428"
    property string secondary: "#091428"
    property string accent:    "#C89B3C"
    property string textColor: "#F0E6D2"
    property string danger:    "#C34632"
    property string success:   "#1E8B55"
    property string cardBg:    "#1a1a2e"

    // ===== Palette (centralized) =====
    property string bgTransparent: "#00000000"
    property string overlayScrimBG:  "#40000000"
    property string overlayScrim:  "#80000000"
    property string shadowColor:   "#40000000"
    property string borderColor:   "#3C3C41"
    property string neutral400:    "#404040"
    property string neutral500:    "#606060"
    property string mutedText:     "#666666"
    property string disabledBg:    "#2a2a2a"
    property string hintText:      "#888888"
    property string info:          "#2196F3"
    property string warn:          "#e6a500"
    property string white:         "#FFFFFF"
    property string offWhite:      "#E0E0E0"

    // ===== Data =====
    property var accounts: []
    property var regions: []

    // ===== Selection and form state =====
    property string selectAccountText: "Select an account"
    property string selectedAccountDisplay: selectAccountText
    property int selectedAccountIndex: -1  // For account management list
    property bool isEditingAccount: false  // Track if we're editing vs creating new
    property bool passwordVisible: false  // Track password visibility
    
    // ===== Page state =====
    property bool isSettingsPage: false
    property int currentTab: 0  // 0 = Login, 1 = Account Management
    
    // ===== Settings =====
    property int currentSpeed: 1
    property bool isLoadingSettings: true
    
    // Auto-save speed setting when it changes
    onCurrentSpeedChanged: {
        if (!isLoadingSettings) {
            backend.setSpeedSetting(currentSpeed)
        }
    }
    
    // Initialize and load settings
    Component.onCompleted: {
        // Load saved speed setting from backend
        currentSpeed = backend.getSpeedSetting()
        isLoadingSettings = false  // Enable auto-save after initial load
        
        // Match initial top-most behavior for ~2 seconds
        Qt.callLater(function() { window.flags = Qt.FramelessWindowHint | Qt.Window })
    }

    // convenience getters
    function selectedUsername() {
        if (selectedAccountDisplay === selectAccountText) return "";
        return selectedAccountDisplay.split(" (")[0];
    }

    signal requestMinimize()
    signal requestClose()

    // ===== Background =====
    Item {
        anchors.fill: parent
        Image {
            anchors.fill: parent
            source: bgImageUrl
            fillMode: Image.PreserveAspectCrop
            asynchronous: true
            cache: false
            visible: bgImageUrl && bgImageUrl.toString() !== ""
        }
        // overlay for readability
        Rectangle { anchors.fill: parent; color: overlayScrimBG }
    }

    // ===== Top Drag Area =====
    Rectangle {
        id: topDragArea
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: 60
        color: "transparent"
        z: 999

        MouseArea {
            anchors.fill: parent
            onPressed: window.startSystemMove()
        }
    }

    // ===== Back Button (Left Side) =====
    Rectangle {
        id: backButton
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.topMargin: 16
        anchors.leftMargin: 16
        width: 28; height: 28; radius: 6
        color: neutral400
        border.color: neutral500
        border.width: 1
        visible: isSettingsPage
        z: 1000
        
        MouseArea { 
            anchors.fill: parent; 
            onClicked: isSettingsPage = false
            hoverEnabled: true
            onEntered: parent.color = neutral500
            onExited: parent.color = neutral400
        }
        Text { 
            anchors.centerIn: parent; 
            text: "<"; 
            color: white; 
            font.pixelSize: 14; 
            font.bold: true 
        }
    }

    // ===== Window Control Buttons =====
    Row {
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.topMargin: 16
        anchors.rightMargin: 16
        spacing: 8
        z: 1000

        // Settings
        Rectangle {
            width: 28; height: 28; radius: 6
            color: neutral400
            border.color: neutral500
            border.width: 1
            visible: !isSettingsPage
            MouseArea { 
                anchors.fill: parent; 
                onClicked: isSettingsPage = true
                hoverEnabled: true
                onEntered: parent.color = neutral500
                onExited: parent.color = neutral400
            }
            Text { 
                anchors.centerIn: parent; 
                text: "⚙"; 
                color: white; 
                font.pixelSize: 14 
            }
        }
        // Minimize
        Rectangle {
            width: 28; height: 28; radius: 6
            color: neutral400
            border.color: neutral500
            border.width: 1
            MouseArea { 
                anchors.fill: parent; 
                onClicked: window.showMinimized()
                hoverEnabled: true
                onEntered: parent.color = warn
                onExited: parent.color = neutral400
            }
            Text { anchors.centerIn: parent; text: "—"; color: white; font.pixelSize: 12 }
        }
        // Close
        Rectangle {
            width: 28; height: 28; radius: 6
            color: neutral400
            border.color: neutral500
            border.width: 1
            MouseArea { 
                anchors.fill: parent; 
                onClicked: Qt.quit()
                hoverEnabled: true
                onEntered: parent.color = danger
                onExited: parent.color = neutral400
            }
            Text { anchors.centerIn: parent; text: "×"; color: white; font.pixelSize: 14 }
        }
    }

    // ===== Main content =====
    // Use a centered column with a max width for nice layout on large windows
    ScrollView {
        id: scroller
        anchors.fill: parent
        clip: true
        leftPadding: 0
        rightPadding: 0
        topPadding: 0
        bottomPadding: 0
        
        ScrollBar.vertical.policy: ScrollBar.AsNeeded
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

        Item {
            width: scroller.width
            height: Math.max(scroller.height, rootColumn.implicitHeight + 32)
            
            ColumnLayout {
                id: rootColumn
                width: Math.min(720, parent.width)
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 16
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 32
                spacing: 16



            // --- Title ---
            Text {
                Layout.fillWidth: true
                horizontalAlignment: Text.AlignHCenter
                color: accent
                text: isSettingsPage ? "Settings" : "Riot Auto Login"
                font.pixelSize: 40
                font.bold: true
            }

            // --- Tab Bar (only on main page) ---
            TabBar {
                id: tabBar
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 16
                visible: !isSettingsPage
                spacing: 80
                
                background: Rectangle {
                    color: "transparent"
                }

                
                TabButton {
                    text: "Login"
                    checked: currentTab === 0
                    onClicked: currentTab = 0
                    implicitWidth: 120
                    implicitHeight: 40
                    
                    background: Rectangle {
                        color: "transparent"
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: parent.checked ? accent : textColor
                        font.pixelSize: 16
                        font.bold: parent.checked
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    indicator: Rectangle {
                        width: parent.width - 16
                        height: 3
                        color: accent
                        radius: 1.5
                        anchors.bottom: parent.bottom
                        anchors.horizontalCenter: parent.horizontalCenter
                        visible: parent.checked
                    }
                }
                
                TabButton {
                    text: "Manage"
                    checked: currentTab === 1
                    onClicked: currentTab = 1
                    implicitWidth: 120
                    implicitHeight: 40
                    
                    background: Rectangle {
                        color: "transparent"
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: parent.checked ? accent : textColor
                        font.pixelSize: 16
                        font.bold: parent.checked
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    indicator: Rectangle {
                        width: parent.width - 16
                        height: 3
                        color: accent
                        radius: 1.5
                        anchors.bottom: parent.bottom
                        anchors.horizontalCenter: parent.horizontalCenter
                        visible: parent.checked
                    }
                }
            }

            // --- Content Stack ---
            StackLayout {
                id: contentStack
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 20
                Layout.preferredWidth: Math.min(500, rootColumn.width - 32)
                Layout.minimumHeight: 450
                Layout.maximumHeight: 580
                currentIndex: isSettingsPage ? 2 : currentTab
                
                // --- Login Tab Content ---
                Item {
                    Rectangle {
                        id: loginCard
                        width: Math.min(500, contentStack.width - 32)
                        height: loginColumn.implicitHeight + 48
                        anchors.centerIn: parent
                        radius: 12
                        color: cardBg
                        border.color: borderColor
                        border.width: 1

                        ColumnLayout {
                            id: loginColumn
                            anchors.fill: parent
                            anchors.margins: 20
                            spacing: 14

                            Text { text: "Login"; color: accent; font.pixelSize: 20; font.bold: true; Layout.alignment: Qt.AlignHCenter }

                            // Account Selection for Login
                            ColumnLayout { Layout.fillWidth: true; spacing: 6
                                Text { text: "Select Account:"; color: textColor; font.pixelSize: 14; font.bold: true }
                                
                                Rectangle {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 120
                                    color: primary
                                    radius: 8
                                    border.color: borderColor
                                    border.width: 1
                                    
                                    ListView {
                                        id: loginAccountListView
                                        anchors.fill: parent
                                        anchors.margins: 4
                                        model: accounts
                                        clip: true
                                        
                                        property int selectedLoginIndex: -1
                                        
                                        delegate: Rectangle {
                                            width: loginAccountListView.width
                                            height: 36
                                            color: index === loginAccountListView.selectedLoginIndex ? accent : "transparent"
                                            radius: 6
                                            border.color: index === loginAccountListView.selectedLoginIndex ? accent : borderColor
                                            border.width: 1
                                            
                                            Text {
                                                anchors.left: parent.left
                                                anchors.leftMargin: 12
                                                anchors.verticalCenter: parent.verticalCenter
                                                text: modelData.username + " (" + modelData.region + ")"
                                                color: index === loginAccountListView.selectedLoginIndex ? primary : textColor
                                                font.pixelSize: 14
                                                font.bold: index === loginAccountListView.selectedLoginIndex
                                            }
                                            
                                            MouseArea {
                                                anchors.fill: parent
                                                onClicked: {
                                                    loginAccountListView.selectedLoginIndex = index
                                                    selectedAccountDisplay = modelData.username + " (" + modelData.region + ")"
                                                    // Update the combobox for compatibility
                                                    accountCombo.currentIndex = index + 1
                                                }
                                            }
                                        }
                                    }
                                    
                                    Text {
                                        anchors.centerIn: parent
                                        text: "No accounts saved\nGo to 'Manage' tab to add accounts"
                                        color: mutedText
                                        font.pixelSize: 13
                                        horizontalAlignment: Text.AlignHCenter
                                        visible: accounts.length === 0
                                    }
                                }
                            }

                            // Hidden combobox for compatibility (keep existing backend connections working)
                            ComboBox {
                                id: accountCombo
                                visible: false
                                model: [selectAccountText].concat(accounts.map(function(a) { return a.username + " (" + a.region + ")"; }))
                            }

                            Button {
                                Layout.fillWidth: true
                                text: "LOGIN"
                                implicitHeight: 45
                                enabled: loginAccountListView.selectedLoginIndex >= 0
                                background: Rectangle { 
                                    color: loginAccountListView.selectedLoginIndex >= 0 ? accent : disabledBg
                                    radius: 8 
                                }
                                contentItem: Text {
                                    text: parent.text
                                    color: loginAccountListView.selectedLoginIndex >= 0 ? primary : mutedText
                                    font.pixelSize: 16
                                    font.bold: true
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                }
                                onClicked: {
                                    if (loginAccountListView.selectedLoginIndex < 0) {
                                        notificationBanner.showMessage("Please select an account to login", "error");
                                        return;
                                    }
                                    var selectedAccount = accounts[loginAccountListView.selectedLoginIndex];
                                    backend.loginToClient(selectedAccount.username, ["Slow", "Default", "Fast"][window.currentSpeed]);
                                }
                            }
                        }
                    }
                }

                // --- Account Tab Content ---
                Item {
                    Rectangle {
                        id: accountCard
                        width: Math.min(500, contentStack.width - 32)
                        height: accountColumn.implicitHeight + 48
                        anchors.centerIn: parent
                        radius: 12
                        color: cardBg
                        border.color: borderColor
                        border.width: 1

                        ColumnLayout {
                            id: accountColumn
                            anchors.fill: parent
                            anchors.margins: 20
                            spacing: 12

                            Text { text: "Account Management"; color: accent; font.pixelSize: 20; font.bold: true; Layout.alignment: Qt.AlignHCenter }

                            // Account List
                            ColumnLayout { Layout.fillWidth: true; spacing: 6
                                Text { text: "Select Account:"; color: textColor; font.pixelSize: 14; font.bold: true }
                                
                                Rectangle {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 120
                                    color: primary
                                    radius: 8
                                    border.color: borderColor
                                    border.width: 1
                                    
                                    ListView {
                                        id: accountListView
                                        anchors.fill: parent
                                        anchors.margins: 4
                                        model: accounts
                                        clip: true
                                        
                                        delegate: Rectangle {
                                            width: accountListView.width
                                            height: 32
                                            color: index === selectedAccountIndex ? accent : "transparent"
                                            radius: 6
                                            border.color: index === selectedAccountIndex ? accent : borderColor
                                            border.width: 1
                                            
                                            Text {
                                                anchors.left: parent.left
                                                anchors.leftMargin: 12
                                                anchors.verticalCenter: parent.verticalCenter
                                                text: modelData.username + " (" + modelData.region + ")"
                                                color: index === selectedAccountIndex ? primary : textColor
                                                font.pixelSize: 13
                                                font.bold: index === selectedAccountIndex
                                            }
                                            
                                            MouseArea {
                                                anchors.fill: parent
                                                onClicked: {
                                                    selectedAccountIndex = index
                                                    isEditingAccount = true
                                                    usernameField.text = modelData.username
                                                    passwordField.text = modelData.password
                                                    var regionIdx = regions.indexOf(modelData.region)
                                                    regionCombo.currentIndex = regionIdx
                                                    selectedAccountDisplay = modelData.username + " (" + modelData.region + ")"
                                                }
                                            }
                                        }
                                    }
                                    
                                    Text {
                                        anchors.centerIn: parent
                                        text: "No accounts saved"
                                        color: mutedText
                                        font.pixelSize: 13
                                        visible: accounts.length === 0
                                    }
                                }
                                
                                // Add New Account Button
                                Button {
                                    Layout.fillWidth: true
                                    implicitHeight: 40
                                    background: Rectangle { 
                                        color: "transparent"
                                        radius: 8
                                        border.color: accent
                                        border.width: 2
                                    }
                                    contentItem: Text {
                                        text: "+ Add New Account"
                                        color: accent
                                        font.pixelSize: 14
                                        font.bold: true
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                    onClicked: {
                                        selectedAccountIndex = -1
                                        loginAccountListView.selectedLoginIndex = -1
                                        isEditingAccount = false
                                        usernameField.text = ""
                                        passwordField.text = ""
                                        regionCombo.currentIndex = -1
                                        selectedAccountDisplay = selectAccountText
                                    }
                                }
                            }

                            // Username - Modern Floating Label Field
                            Item {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 70
                                
                                Rectangle {
                                    id: usernameContainer
                                    anchors.fill: parent
                                    anchors.topMargin: 15
                                    color: primary
                                    radius: 12
                                    border.color: usernameField.activeFocus ? accent : (usernameMouseArea.containsMouse ? neutral400 : borderColor)
                                    border.width: usernameField.activeFocus ? 2 : 1
                                    
                                    Behavior on border.color { ColorAnimation { duration: 200; easing.type: Easing.OutQuad } }
                                    Behavior on border.width { NumberAnimation { duration: 200; easing.type: Easing.OutQuad } }
                                    
                                    // Glow effect when focused
                                    Rectangle {
                                        anchors.fill: parent
                                        anchors.margins: -3
                                        radius: parent.radius + 3
                                        color: "transparent"
                                        border.color: accent
                                        border.width: usernameField.activeFocus ? 1 : 0
                                        opacity: usernameField.activeFocus ? 0.3 : 0
                                        
                                        Behavior on opacity { NumberAnimation { duration: 200; easing.type: Easing.OutQuad } }
                                        Behavior on border.width { NumberAnimation { duration: 200; easing.type: Easing.OutQuad } }
                                    }
                                    
                                    TextField {
                                        id: usernameField
                                        anchors.fill: parent
                                        anchors.topMargin: 8
                                        color: textColor
                                        leftPadding: 16
                                        rightPadding: 16
                                        topPadding: 8
                                        bottomPadding: 8
                                        background: Rectangle { color: "transparent" }
                                        selectByMouse: true
                                        
                                        // Custom cursor
                                        cursorDelegate: Rectangle {
                                            color: accent
                                            width: 2
                                            radius: 1
                                            opacity: usernameField.activeFocus ? 1 : 0
                                            
                                            SequentialAnimation on opacity {
                                                id: usernameCursorAnimation
                                                loops: Animation.Infinite
                                                running: usernameField.activeFocus
                                                NumberAnimation { from: 1; to: 0; duration: 500; easing.type: Easing.InOutQuad }
                                                NumberAnimation { from: 0; to: 1; duration: 500; easing.type: Easing.InOutQuad }
                                            }
                                        }
                                        
                                        onTextEdited: if (selectedAccountDisplay !== selectAccountText) selectedAccountDisplay = selectAccountText
                                    }
                                    
                                    MouseArea {
                                        id: usernameMouseArea
                                        anchors.fill: parent
                                        hoverEnabled: true
                                        acceptedButtons: Qt.NoButton
                                        z: -1
                                    }
                                }
                                
                                // Floating Label
                                Text {
                                    id: usernameLabel
                                    text: "Username"
                                    color: usernameField.activeFocus ? accent : (usernameField.text.length > 0 ? textColor : hintText)
                                    font.pixelSize: usernameField.activeFocus || usernameField.text.length > 0 ? 12 : 16
                                    font.bold: usernameField.activeFocus
                                    
                                    anchors.left: parent.left
                                    anchors.leftMargin: 16
                                    
                                    y: usernameField.activeFocus || usernameField.text.length > 0 ? 18 : 30
                                    
                                    Behavior on y { NumberAnimation { duration: 200; easing.type: Easing.OutQuad } }
                                    Behavior on font.pixelSize { NumberAnimation { duration: 200; easing.type: Easing.OutQuad } }
                                    Behavior on color { ColorAnimation { duration: 200; easing.type: Easing.OutQuad } }
                                    
                                    MouseArea {
                                        anchors.fill: parent
                                        onClicked: usernameField.forceActiveFocus()
                                    }
                                }
                            }

                            // Password - Modern Floating Label Field with Enhanced Eye Toggle
                            Item {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 70
                                
                                Rectangle {
                                    id: passwordContainer
                                    anchors.fill: parent
                                    anchors.topMargin: 15
                                    color: primary
                                    radius: 12
                                    border.color: passwordField.activeFocus ? accent : (passwordMouseArea.containsMouse ? neutral400 : borderColor)
                                    border.width: passwordField.activeFocus ? 2 : 1
                                    
                                    Behavior on border.color { ColorAnimation { duration: 200; easing.type: Easing.OutQuad } }
                                    Behavior on border.width { NumberAnimation { duration: 200; easing.type: Easing.OutQuad } }
                                    
                                    // Glow effect when focused
                                    Rectangle {
                                        anchors.fill: parent
                                        anchors.margins: -3
                                        radius: parent.radius + 3
                                        color: "transparent"
                                        border.color: accent
                                        border.width: passwordField.activeFocus ? 1 : 0
                                        opacity: passwordField.activeFocus ? 0.3 : 0
                                        
                                        Behavior on opacity { NumberAnimation { duration: 200; easing.type: Easing.OutQuad } }
                                        Behavior on border.width { NumberAnimation { duration: 200; easing.type: Easing.OutQuad } }
                                    }
                                    
                                    TextField {
                                        id: passwordField
                                        anchors.fill: parent
                                        anchors.topMargin: 8
                                        anchors.rightMargin: 50  // Space for eye button
                                        echoMode: passwordVisible ? TextInput.Normal : TextInput.Password
                                        color: textColor
                                        leftPadding: 16
                                        rightPadding: 16
                                        topPadding: 8
                                        bottomPadding: 8
                                        background: Rectangle { color: "transparent" }
                                        selectByMouse: true
                                        
                                        // Custom cursor
                                        cursorDelegate: Rectangle {
                                            color: accent
                                            width: 2
                                            radius: 1
                                            opacity: passwordField.activeFocus ? 1 : 0
                                            
                                            SequentialAnimation on opacity {
                                                id: passwordCursorAnimation
                                                loops: Animation.Infinite
                                                running: passwordField.activeFocus
                                                NumberAnimation { from: 1; to: 0; duration: 800; easing.type: Easing.InOutQuad }
                                                NumberAnimation { from: 0; to: 1; duration: 800; easing.type: Easing.InOutQuad }
                                            }
                                        }
                                    }
                                    
                                    // Enhanced Eye toggle button with ripple effect
                                    Rectangle {
                                        id: eyeButton
                                        anchors.right: parent.right
                                        anchors.rightMargin: 8
                                        anchors.verticalCenter: parent.verticalCenter
                                        width: 36
                                        height: 36
                                        radius: 18
                                        color: eyeMouseArea.containsMouse ? neutral400 : "transparent"
                                        
                                        Behavior on color { ColorAnimation { duration: 150; easing.type: Easing.OutQuad } }
                                        
                                        // Ripple effect
                                        Rectangle {
                                            id: ripple
                                            anchors.centerIn: parent
                                            width: 0
                                            height: 0
                                            radius: width / 2
                                            color: accent
                                            opacity: 0
                                            
                                            SequentialAnimation {
                                                id: rippleAnimation
                                                ParallelAnimation {
                                                    NumberAnimation { target: ripple; property: "width"; from: 0; to: 48; duration: 300; easing.type: Easing.OutQuad }
                                                    NumberAnimation { target: ripple; property: "height"; from: 0; to: 48; duration: 300; easing.type: Easing.OutQuad }
                                                    NumberAnimation { target: ripple; property: "opacity"; from: 0.4; to: 0; duration: 300; easing.type: Easing.OutQuad }
                                                }
                                                ScriptAction { script: { ripple.width = 0; ripple.height = 0; ripple.opacity = 0; } }
                                            }
                                        }
                                        
                                        Text {
                                            anchors.centerIn: parent
                                            text: passwordVisible ? "🔓" : "🔒"
                                            font.pixelSize: 18
                                            color: eyeMouseArea.containsMouse ? accent : textColor
                                            
                                            Behavior on color { ColorAnimation { duration: 150; easing.type: Easing.OutQuad } }
                                            
                                            // Subtle bounce animation when toggled
                                            SequentialAnimation on scale {
                                                id: bounceAnimation
                                                running: false
                                                NumberAnimation { from: 1; to: 1.3; duration: 100; easing.type: Easing.OutQuad }
                                                NumberAnimation { from: 1.3; to: 1; duration: 150; easing.type: Easing.OutBounce }
                                            }
                                        }
                                        
                                        MouseArea {
                                            id: eyeMouseArea
                                            anchors.fill: parent
                                            hoverEnabled: true
                                            onClicked: {
                                                passwordVisible = !passwordVisible
                                                rippleAnimation.start()
                                                bounceAnimation.start()
                                            }
                                        }
                                    }
                                    
                                    MouseArea {
                                        id: passwordMouseArea
                                        anchors.fill: parent
                                        anchors.rightMargin: 50
                                        hoverEnabled: true
                                        acceptedButtons: Qt.NoButton
                                        z: -1
                                    }
                                }
                                
                                // Floating Label
                                Text {
                                    id: passwordLabel
                                    text: "Password"
                                    color: passwordField.activeFocus ? accent : (passwordField.text.length > 0 ? textColor : hintText)
                                    font.pixelSize: passwordField.activeFocus || passwordField.text.length > 0 ? 12 : 16
                                    font.bold: passwordField.activeFocus
                                    
                                    anchors.left: parent.left
                                    anchors.leftMargin: 16
                                    
                                    y: passwordField.activeFocus || passwordField.text.length > 0 ? 18 : 30
                                    
                                    Behavior on y { NumberAnimation { duration: 200; easing.type: Easing.OutQuad } }
                                    Behavior on font.pixelSize { NumberAnimation { duration: 200; easing.type: Easing.OutQuad } }
                                    Behavior on color { ColorAnimation { duration: 200; easing.type: Easing.OutQuad } }
                                    
                                    MouseArea {
                                        anchors.fill: parent
                                        onClicked: passwordField.forceActiveFocus()
                                    }
                                }
                            }

                            // Region
                            ColumnLayout { Layout.fillWidth: true; spacing: 6
                                Text { text: "Region"; color: textColor; font.pixelSize: 14; font.bold: true }
                                ComboBox {
                                    id: regionCombo
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 55
                                    model: regions
                                    currentIndex: -1
                                    displayText: currentIndex >= 0 ? currentText : "Select a region"
                                    font.pixelSize: 14
                                    
                                    background: Rectangle {
                                        color: primary
                                        radius: 8
                                        border.color: borderColor
                                        border.width: 1
                                    }
                                    
                                    contentItem: Text {
                                        text: regionCombo.displayText
                                        color: regionCombo.currentIndex >= 0 ? textColor : hintText
                                        font.pixelSize: 14
                                        verticalAlignment: Text.AlignVCenter
                                        leftPadding: 12
                                    }
                                    
                                    indicator: Text {
                                        anchors.right: parent.right
                                        anchors.rightMargin: 12
                                        anchors.verticalCenter: parent.verticalCenter
                                        text: "▼"
                                        color: hintText
                                        font.pixelSize: 12
                                    }
                                    
                                     popup: Popup {
                                         y: regionCombo.height
                                         width: regionCombo.width
                                         implicitHeight: Math.min(contentItem.implicitHeight, 200) // Max height of 200px
                                         padding: 2
                                        
                                        background: Rectangle {
                                            color: cardBg
                                            radius: 8
                                            border.color: borderColor
                                            border.width: 1
                                            
                                            // Add subtle shadow
                                            Rectangle {
                                                anchors.fill: parent
                                                anchors.margins: -3
                                                radius: parent.radius + 3
                                                color: shadowColor
                                                z: -1
                                            }
                                        }
                                        
                                        contentItem: ListView {
                                            clip: true
                                            implicitHeight: contentHeight
                                            model: regionCombo.popup.visible ? regionCombo.delegateModel : null
                                            currentIndex: regionCombo.highlightedIndex
                                        }
                                    }
                                    
                                    // Custom delegate styling
                                    delegate: ItemDelegate {
                                        width: regionCombo.width - 4
                                        implicitHeight: 32
                                        
                                        background: Rectangle {
                                            color: parent.hovered ? accent : "transparent"
                                            radius: 4
                                            anchors.margins: 1
                                        }
                                        
                                        contentItem: Text {
                                            text: modelData
                                            color: parent.hovered ? primary : textColor
                                            font.pixelSize: 12
                                            verticalAlignment: Text.AlignVCenter
                                            leftPadding: 8
                                        }
                                    }
                                    
                                    onActivated: function(index) { /* keep selection */ }
                                }
                            }

                            RowLayout { Layout.fillWidth: true; spacing: 8
                                Button {
                                    Layout.fillWidth: true
                                    text: isEditingAccount ? "UPDATE" : "SAVE"
                                    implicitHeight: 45
                                    background: Rectangle { color: accent; radius: 8 }
                                    contentItem: Text {
                                        text: parent.text; color: primary; font.pixelSize: 16; font.bold: true
                                        horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                                    }
                                    onClicked: {
                                        if (!usernameField.text.trim()) {
                                            notificationBanner.showMessage("Username is required", "error");
                                            return;
                                        }
                                        if (!passwordField.text) {
                                            notificationBanner.showMessage("Password is required", "error");
                                            return;
                                        }
                                        if (regionCombo.currentIndex < 0 || !regionCombo.currentText) {
                                            notificationBanner.showMessage("Please select a region", "error");
                                            return;
                                        }
                                        backend.saveAccount(usernameField.text, passwordField.text, regionCombo.currentText);
                                    }
                                }
                                Button {
                                    Layout.fillWidth: true
                                    text: "DELETE"
                                    implicitHeight: 45
                                    enabled: isEditingAccount
                                    background: Rectangle { 
                                        color: isEditingAccount ? danger : disabledBg
                                        radius: 8 
                                    }
                                    contentItem: Text {
                                        text: parent.text
                                        color: isEditingAccount ? white : mutedText
                                        font.pixelSize: 16
                                        font.bold: true
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                    onClicked: {
                                        if (isEditingAccount) {
                                            confirmOverlay.visible = true
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                // --- Settings Page Content ---
                Item {
                    Rectangle {
                        id: settingsCard
                        width: Math.min(500, contentStack.width - 32)
                        height: settingsColumn.implicitHeight + 48
                        anchors.centerIn: parent
                        radius: 12
                        color: cardBg
                        border.color: borderColor
                        border.width: 1

                        ColumnLayout {
                            id: settingsColumn
                            anchors.fill: parent
                            anchors.margins: 20
                            spacing: 16

                            // Speed Selector
                            ColumnLayout { Layout.fillWidth: true; spacing: 8
                                Text { text: "Speed:"; color: textColor; font.pixelSize: 14; font.bold: true }
                                RowLayout { Layout.fillWidth: true; spacing: 12
                                    Slider {
                                        id: settingsSpeedSlider
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: 35
                                        from: 0
                                        to: 2
                                        stepSize: 1
                                        value: window.currentSpeed
                                        onValueChanged: window.currentSpeed = settingsSpeedSlider.value
                                        snapMode: Slider.SnapAlways
                                        
                                        background: Rectangle {
                                            x: settingsSpeedSlider.leftPadding
                                            y: settingsSpeedSlider.topPadding + settingsSpeedSlider.availableHeight / 2 - height / 2
                                            width: settingsSpeedSlider.availableWidth
                                            height: 4
                                            radius: 2
                                            color: borderColor
                                            
                                            Rectangle {
                                                width: settingsSpeedSlider.visualPosition * parent.width
                                                height: parent.height
                                                color: accent
                                                radius: 2
                                            }
                                        }
                                        
                                        handle: Rectangle {
                                            x: settingsSpeedSlider.leftPadding + settingsSpeedSlider.visualPosition * (settingsSpeedSlider.availableWidth - width)
                                            y: settingsSpeedSlider.topPadding + settingsSpeedSlider.availableHeight / 2 - height / 2
                                            width: 20
                                            height: 20
                                            radius: 10
                                            color: settingsSpeedSlider.pressed ? offWhite : white
                                            border.color: accent
                                            border.width: 2
                                        }
                                    }
                                    Text {
                                        id: settingsSpeedLabel
                                        text: ["Slow", "Default", "Fast"][settingsSpeedSlider.value]
                                        color: textColor
                                        font.pixelSize: 14
                                        font.bold: true
                                        Layout.preferredWidth: 60
                                        horizontalAlignment: Text.AlignHCenter
                                    }
                                }
                            }
                        }
                    }
                }
            }


        }
        }
    }

    // ===== Notification Banner (Overlay) =====
    Rectangle {
        id: notificationBanner
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 80
        width: Math.min(420, window.width - 40)
        height: 45
        radius: 8
        color: success
        visible: false
        z: 2000

        property var hideTimer: null

        function showMessage(message, type) {
            textLabel.text = message;
            color = (type === "error") ? danger : ((type === "success") ? success : info);
            visible = true;
            if (hideTimer) hideTimer.stop();
            // Auto-hide all message types after 3 seconds
            hideTimer = Qt.createQmlObject('import QtQuick 2.15; Timer { interval: 3000; repeat: false }', notificationBanner);
            hideTimer.triggered.connect(function() { notificationBanner.visible = false; });
            hideTimer.start();
        }

        Text { 
            id: textLabel
            anchors.centerIn: parent
            color: white
            font.pixelSize: 14
            font.bold: true
        }
        
        // Add a subtle shadow effect
        Rectangle {
            anchors.fill: parent
            anchors.margins: -2
            radius: parent.radius + 2
            color: shadowColor
            z: -1
        }
    }

    // ===== Backend signal wiring =====
    Connections {
        target: backend
        function onNotification(message, type) { notificationBanner.showMessage(message, type); }
        function onAccountsChanged(items) { window.accounts = items; }
        function onRegionsChanged(items) { window.regions = items; }
        function onSavedAccount(u, r) {
            selectedAccountDisplay = u + " (" + r + ")";
            // update both list selections to match
            var idx = 0;
            for (var i = 0; i < window.accounts.length; i++) {
                if (window.accounts[i].username === u && window.accounts[i].region === r) {
                    idx = i + 1; // +1 for placeholder option
                    selectedAccountIndex = i; // Update account management list selection
                    loginAccountListView.selectedLoginIndex = i; // Update login list selection
                    isEditingAccount = true;
                    break;
                }
            }
            accountCombo.currentIndex = idx;
        }
    }

    // ===== Confirm delete overlay =====
    Rectangle {
        id: confirmOverlay
        anchors.fill: parent
        color: overlayScrim
        visible: false
        z: 1000

        Rectangle {
            id: confirmCard
            width: Math.min(420, window.width - 40)
            height: 180
            radius: 10
            color: cardBg
            border.color: borderColor
            border.width: 1
            anchors.centerIn: parent

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12

                Text {
                    text: isEditingAccount && selectedAccountIndex >= 0 ? 
                          "Are you sure you want to delete '" + window.accounts[selectedAccountIndex].username + " (" + window.accounts[selectedAccountIndex].region + ")'?" :
                          "Are you sure you want to delete the selected account?"
                    color: textColor
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }

                RowLayout {
                    spacing: 8
                    Layout.fillWidth: true

                    Button {
                        Layout.fillWidth: true
                        text: "Cancel"
                        implicitHeight: 40
                        background: Rectangle { color: neutral400; radius: 8; border.color: neutral500; border.width: 1 }
                        contentItem: Text {
                            text: parent.text; color: white; font.pixelSize: 14; font.bold: true
                            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                        }
                        onClicked: confirmOverlay.visible = false
                    }
                    Button {
                        Layout.fillWidth: true
                        text: "OK"
                        implicitHeight: 40
                        background: Rectangle { color: danger; radius: 8 }
                        contentItem: Text {
                            text: parent.text; color: white; font.pixelSize: 14; font.bold: true
                            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                        }
                        onClicked: {
                            if (!isEditingAccount || selectedAccountIndex < 0) {
                                notificationBanner.showMessage("Please select an account to delete", "error");
                                confirmOverlay.visible = false;
                                return;
                            }
                            var account = window.accounts[selectedAccountIndex];
                            backend.deleteAccount(account.username);
                            usernameField.text = "";
                            passwordField.text = "";
                            regionCombo.currentIndex = -1;
                            selectedAccountDisplay = selectAccountText;
                            selectedAccountIndex = -1;
                            loginAccountListView.selectedLoginIndex = -1;
                            isEditingAccount = false;
                            confirmOverlay.visible = false;
                        }
                    }
                }
            }
        }
    }
}
