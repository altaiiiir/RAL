import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15

// Cleaned + consistently styled + proper layout
ApplicationWindow {
    id: window
    visible: true
    width: 650
    height: 800
    minimumWidth: 480
    minimumHeight: 640
    color: "#00000000" // transparent for glassy effect (requires compositor)
    flags: Qt.FramelessWindowHint | Qt.Window
    title: "Riot Auto Login"

    // ===== Theme =====
    property string primary:  "#0A1428"
    property string secondary:"#091428"
    property string accent:   "#C89B3C"
    property string textColor:"#F0E6D2"
    property string danger:   "#C34632"
    property string success:  "#1E8B55"
    property string cardBg:   "#1a1a2e"

    // ===== Data =====
    property var accounts: []
    property var regions: []

    // ===== Selection and form state =====
    property string selectAccountText: "Select an account"
    property string selectedAccountDisplay: selectAccountText

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
        Rectangle { anchors.fill: parent; color: "#80000000" }
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
            cursorShape: Qt.SizeAllCursor
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

        // Minimize
        Rectangle {
            width: 24; height: 24; radius: 6
            color: "#404040"
            border.color: "#606060"
            border.width: 1
            MouseArea { 
                anchors.fill: parent; 
                onClicked: window.showMinimized()
                hoverEnabled: true
                onEntered: parent.color = "#505050"
                onExited: parent.color = "#404040"
            }
            Text { anchors.centerIn: parent; text: "—"; color: "white"; font.pixelSize: 12 }
        }
        // Close
        Rectangle {
            width: 24; height: 24; radius: 6
            color: "#404040"
            border.color: "#606060"
            border.width: 1
            MouseArea { 
                anchors.fill: parent; 
                onClicked: Qt.quit()
                hoverEnabled: true
                onEntered: parent.color = "#c34632"
                onExited: parent.color = "#404040"
            }
            Text { anchors.centerIn: parent; text: "×"; color: "white"; font.pixelSize: 14 }
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
                anchors.bottomMargin: 16
                spacing: 16



            // --- Title ---
            Text {
                Layout.fillWidth: true
                horizontalAlignment: Text.AlignHCenter
                color: accent
                text: "Riot Auto Login"
                font.pixelSize: 40
                font.bold: true
            }

            // --- Centered Account Selector ---
            Rectangle {
                id: selectorCard
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 24
                Layout.preferredWidth: Math.min(500, rootColumn.width - 32)
                Layout.preferredHeight: selectorColumn.implicitHeight + 48
                radius: 12
                color: cardBg
                border.color: "#3C3C41"
                border.width: 1

                ColumnLayout {
                    id: selectorColumn
                    anchors.fill: parent
                    anchors.margins: 24
                    spacing: 20

                    ComboBox {
                        id: accountCombo
                        Layout.fillWidth: true
                        Layout.preferredHeight: 55
                        model: [selectAccountText].concat(accounts.map(function(a) { return a.username + " (" + a.region + ")"; }))
                        onActivated: function(index) {
                            if (index === 0) {
                                selectedAccountDisplay = selectAccountText;
                                usernameField.text = "";
                                passwordField.text = "";
                                regionCombo.currentIndex = -1;
                                return;
                            }
                            selectedAccountDisplay = accountCombo.currentText;
                            var u = selectedAccountDisplay.split(" (")[0];
                            var acc = accounts.find(function(a) { return a.username === u; });
                            if (acc) {
                                usernameField.text = acc.username;
                                passwordField.text = acc.password;
                                var ri = regions.indexOf(acc.region);
                                regionCombo.currentIndex = ri;
                            }
                        }
                    }

                    Button {
                        Layout.fillWidth: true
                        text: "LOGIN"
                        implicitHeight: 55
                        background: Rectangle { color: accent; radius: 8 }
                        contentItem: Text {
                            text: parent.text; color: primary; font.pixelSize: 20; font.bold: true
                            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                        }
                        onClicked: {
                            if (selectedAccountDisplay === selectAccountText) {
                                notificationBanner.showMessage("Please select an account to login", "error");
                                return;
                            }
                            backend.loginToClient(selectedUsername());
                        }
                    }
                }
            }

            // --- Account Creation Form ---
            Rectangle {
                id: formCard
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 16
                Layout.preferredWidth: Math.min(500, rootColumn.width - 32)
                Layout.preferredHeight: formColumn.implicitHeight + 48
                radius: 12
                color: cardBg
                border.color: "#3C3C41"
                border.width: 1

                ColumnLayout {
                    id: formColumn
                    anchors.fill: parent
                    anchors.margins: 24
                    spacing: 16

                    Text { text: "Account Details"; color: accent; font.pixelSize: 20; font.bold: true; Layout.alignment: Qt.AlignHCenter }

                    // Username
                    ColumnLayout { Layout.fillWidth: true; spacing: 6
                        Text { text: "Username"; color: textColor; font.pixelSize: 14; font.bold: true }
                        TextField {
                            id: usernameField
                            Layout.fillWidth: true
                            Layout.preferredHeight: 55
                            placeholderText: "Enter username"
                            color: textColor
                            background: Rectangle { color: primary; radius: 8; border.color: "#3C3C41"; border.width: 1 }
                            onTextEdited: if (selectedAccountDisplay !== selectAccountText) selectedAccountDisplay = selectAccountText
                        }
                    }

                    // Password
                    ColumnLayout { Layout.fillWidth: true; spacing: 6
                        Text { text: "Password"; color: textColor; font.pixelSize: 14; font.bold: true }
                        TextField {
                            id: passwordField
                            Layout.fillWidth: true
                            Layout.preferredHeight: 55
                            echoMode: TextInput.Password
                            placeholderText: "Enter password"
                            color: textColor
                            background: Rectangle { color: primary; radius: 8; border.color: "#3C3C41"; border.width: 1 }
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
                            onActivated: function(index) { /* keep selection */ }
                        }
                    }

                    RowLayout { Layout.fillWidth: true; spacing: 8
                        Button {
                            Layout.fillWidth: true
                            text: "SAVE"
                            implicitHeight: 36
                            background: Rectangle { color: accent; radius: 8 }
                            contentItem: Text {
                                text: parent.text; color: primary; font.pixelSize: 14; font.bold: true
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
                            implicitHeight: 36
                            background: Rectangle { color: danger; radius: 8 }
                            contentItem: Text {
                                text: parent.text; color: "white"; font.pixelSize: 14; font.bold: true
                                horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                            }
                            onClicked: confirmOverlay.visible = true
                        }
                    }
                }
            }

            // --- Notification area ---
            Rectangle {
                id: notificationBanner
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 8
                width: Math.min(420, rootColumn.width)
                height: 40
                radius: 6
                color: success
                visible: false

                property var hideTimer: null

                function showMessage(message, type) {
                    textLabel.text = message;
                    color = (type === "error") ? danger : ((type === "success") ? success : "#2196F3");
                    visible = true;
                    if (hideTimer) hideTimer.stop();
                    if (type === "success" || type === "info") {
                        hideTimer = Qt.createQmlObject('import QtQuick 2.15; Timer { interval: 5000; repeat: false }', notificationBanner);
                        hideTimer.triggered.connect(function() { notificationBanner.visible = false; });
                        hideTimer.start();
                    }
                }

                Text { id: textLabel; anchors.centerIn: parent; color: "white"; font.pixelSize: 14 }
            }
        }
        }
    }

    // Match initial top-most behavior for ~2 seconds
    Component.onCompleted: Qt.callLater(function() { window.flags = Qt.FramelessWindowHint | Qt.Window })

    // ===== Backend signal wiring =====
    Connections {
        target: backend
        function onNotification(message, type) { notificationBanner.showMessage(message, type); }
        function onAccountsChanged(items) { window.accounts = items; }
        function onRegionsChanged(items) { window.regions = items; }
        function onSavedAccount(u, r) {
            selectedAccountDisplay = u + " (" + r + ")";
            // update combobox selection to match
            var idx = 0;
            for (var i = 0; i < window.accounts.length; i++) {
                if (window.accounts[i].username === u && window.accounts[i].region === r) {
                    idx = i + 1; // +1 for placeholder option
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
        color: "#80000000"
        visible: false
        z: 1000

        Rectangle {
            id: confirmCard
            width: Math.min(420, window.width - 40)
            height: 180
            radius: 10
            color: cardBg
            border.color: "#3C3C41"
            border.width: 1
            anchors.centerIn: parent

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12

                Text {
                    text: "Are you sure you want to delete the selected account?"
                    color: textColor
                    wrapMode: Text.WordWrap
                }

                RowLayout {
                    spacing: 8
                    Layout.fillWidth: true

                    Button {
                        Layout.fillWidth: true
                        text: "Cancel"
                        onClicked: confirmOverlay.visible = false
                    }
                    Button {
                        Layout.fillWidth: true
                        text: "OK"
                        background: Rectangle { color: danger; radius: 8 }
                        contentItem: Text {
                            text: parent.text; color: "white"; font.pixelSize: 14; font.bold: true
                            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                        }
                        onClicked: {
                            if (selectedAccountDisplay === selectAccountText) {
                                notificationBanner.showMessage("Please select an account to delete", "error");
                                confirmOverlay.visible = false;
                                return;
                            }
                            var uname = selectedAccountDisplay.split(" (")[0];
                            backend.deleteAccount(uname);
                            usernameField.text = "";
                            passwordField.text = "";
                            regionCombo.currentIndex = -1;
                            selectedAccountDisplay = selectAccountText;
                            confirmOverlay.visible = false;
                        }
                    }
                }
            }
        }
    }
}
