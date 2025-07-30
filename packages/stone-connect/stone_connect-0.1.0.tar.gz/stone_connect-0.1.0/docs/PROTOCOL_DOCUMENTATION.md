# Stone Connect WiFi Electric Heater - Communication Protocol Documentation

## Overview

This document provides a comprehensive analysis of the communication protocol used by the Stone Connect WiFi electric heater application. The system uses multiple communication methods:

1. **WiFi Provisioning** (ESP32-based using Protocol Buffers)
2. **HTTP REST API** (Local and Cloud communication)
3. **MQTT** (Eurotech cloud-based messaging)

## 1. WiFi Provisioning Protocol

### 1.1 ESP32 Provisioning System

The heater uses ESP32-based WiFi provisioning with Protocol Buffers for configuration.

#### Key Protocol Buffer Definitions:

**WiFi Configuration (`wifi_config.proto`)**:
```protobuf
message CmdSetConfig {
    bytes ssid = 1;
    bytes passphrase = 2;
    bytes bssid = 3;
    int32 channel = 4;
}

message RespGetStatus {
    Status status = 1;
    WifiStationState sta_state = 2;
    oneof state {
        WifiConnectFailedReason fail_reason = 10;
        WifiConnectedState connected = 11;
    }
}
```

**WiFi States (`wifi_constants.proto`)**:
```protobuf
enum WifiStationState {
    Connected = 0;
    Connecting = 1;
    Disconnected = 2;
    ConnectionFailed = 3;
}

enum WifiAuthMode {
    Open = 0;
    WEP = 1;
    WPA_PSK = 2;
    WPA2_PSK = 3;
    WPA_WPA2_PSK = 4;
    WPA2_ENTERPRISE = 5;
}
```

#### Provisioning Flow:

1. **Device Discovery**: Scan for WiFi networks with device prefix
2. **Connect to Device AP**: Connect to heater's access point
3. **Send WiFi Credentials**: Use `CmdSetConfig` to configure WiFi
4. **Apply Configuration**: Send `CmdApplyConfig` command
5. **Monitor Status**: Poll with `CmdGetStatus` until connected

#### Message Types:
- `TypeCmdGetStatus = 0` - Get current WiFi status
- `TypeCmdSetConfig = 2` - Set WiFi credentials
- `TypeCmdApplyConfig = 4` - Apply WiFi configuration

## 2. Local HTTPS API

### 2.1 Base Configuration

**Local API Configuration**:
- Protocol: HTTPS (TLS/SSL enabled)
- Port: 443 (standard HTTPS port)
- Base URL: `https://{device_ip}/Domestic_Heating/Radiators/v1/`
- Timeout: 30 seconds for connect/read/write operations
- Certificate: Self-signed (requires SSL verification bypass)

### 2.2 Authentication

**Local Authentication** (Required for all endpoints):
```
Authorization: Basic QXBwX1JhZFdpRmlfdmBgZWVqZnM0dzhlN3E1d2RhNHM1ZDFhczI=
```

**Decoded Credentials**:
- Username: `App_RadWiFi_v1`
- Password: `e1qf45s4w8e7q5wda4s5d1as2`

### 2.3 API Endpoints

All endpoints use the base URL: `https://{device_ip}/Domestic_Heating/Radiators/v1/`

#### Device Information
```http
GET /info
Response: Device information including model, version, capabilities
```

#### Device Status
```http
GET /Status
Response: Current temperature, setpoint, operation mode, heating status
```

#### Weekly Schedule
```http
GET /Schedule
Response: Weekly heating schedule with time points and temperatures
```

#### Temperature and Mode Control (Combined)
```http
PUT /setpoint
Body: {
  "Client_ID": "571519332SN20244900365",
  "Set_Point": 21.5,
  "Operative_Mode": "SET"
}
Response: Updated status confirmation
```

#### Device Control
```http
PUT /blink
Body: {} (triggers LED blink for device identification)

PUT /factoryReset
Body: {} (resets device to factory defaults)

PUT /putApplianceName
Body: {"name": "Living Room Heater"}
```

**Required Headers for all requests**:
```
Authorization: Basic QXBwX1JhZFdpRmlfdmBgZWVqZnM0dzhlN3E1d2RhNHM1ZDFhczI=
Content-Type: application/json
```

**Note**: Temperature and operation mode are set together via the `/setpoint` endpoint, not separately.
  - Authorization: Basic {auth}
  - Home_ID: {home_id}
  - Home_Token: {home_token}
```

### 2.4 URL Patterns

**Local URLs**:
```
http://{device_ip}/Domestic_Heating/Radiators/v1/{endpoint}
```

**Cloud URLs** (Base varies by environment):
```
https://api.cloud.com/v1/{endpoint}
```

### 2.5 Data Models

#### StatusNetworkObject
```json
{
  "Client_ID": "string",
  "Set_Point": 20.5,
  "Operative_Mode": "MANUAL|AUTO|ECO|COMFORT|ANTIFREEZE|BOOST",
  "Daily_Energy": 0,
  "Power_Consumption_Watt": 1200,
  "Error_Code": 0,
  "Error_Message": "string",
  "Last_Update": 1640995200000,
  "Broker_Enabled": true
}
```

#### Device Information
```json
{
  "Client_ID": "string",
  "Zone_Name": "Living Room",
  "Zone_ID": "zone_001",
  "MAC_Address": "AA:BB:CC:DD:EE:FF",
  "IP_Address": "192.168.1.100",
  "FW_Version": "1.2.3",
  "PCB_Version": "2.1",
  "Temperature_Unit": "CELSIUS|FAHRENHEIT",
  "High_Power": 1500,
  "Medium_Power": 1000,
  "Low_Power": 500,
  "Is_Installed": true
}
```

## 3. MQTT Protocol

### 3.1 Broker Configuration

**Primary Configuration** (`eurotech_config.json`):
```json
{
  "port": 1883,
  "sslEnabled": false,
  "willEnabled": false,
  "accountName": "Zoppas-Test",
  "username": "device_client_android",
  "password": "V9DefLgNHf!5Yss",
  "clientId": "my-Device-client",
  "url": "mqtt://broker-sandbox.everyware-cloud.com",
  "modelId": "stone"
}
```

**Environment-Specific Brokers**:
- **Sandbox**: `mqtt://broker-sandbox.everyware-cloud.com:1883`
- **Stage**: `mqtt://broker-stage.everyware-cloud.com:1883`  
- **Production**: `mqtt://broker.everyware-cloud.com:1883`

### 3.2 Topic Structure

**Data Topics**:
```
{account_name}/{client_id}/data
Zoppas-Test/my-Device-client/data
```

**Control Topics**:
```
$EDC/{account_name}/{client_id}/#
$EDC/{account_name}/$ALL/#
```

**Birth Certificate**:
```
$EDC/{account_name}/{client_id}/MQTT/BIRTH
```

**Last Will Testament**:
```
$EDC/{account_name}/{client_id}/MQTT/LWT
```

**Disconnect Certificate**:
```
$EDC/{account_name}/{client_id}/MQTT/DC
```

### 3.3 Message Format

**Statistics Message Example**:
```json
{
  "d": {
    "device": "smartphone",
    "statistics": {
      "day": [
        {
          "p": [
            "0:2:289:0",  // hour:mode:power:minute
            "0:1:189:1",
            "0:3:358:2"
          ],
          "d": 1438778407806  // timestamp
        }
      ]
    }
  }
}
```

**Device Status Payload**:
```json
{
  "timestamp": 1640995200000,
  "client_id": "device_001",
  "temperature": 21.5,
  "setpoint": 20.0,
  "mode": "AUTO",
  "power": 1200,
  "energy": 2.5
}
```

### 3.4 QoS Levels

- **Birth/Death Messages**: QoS 1 (at least once)
- **Data Messages**: QoS 0 (fire and forget)
- **Control Messages**: QoS 0 (fire and forget)

## 4. Device Status Protocol

### 4.1 BLE Configuration Values

**Temperature Encoding**:
- Celsius: Direct temperature value
- Fahrenheit: Converted value
- Special values: Antifreeze (-50), Standby (-51)

**Operating Modes**:
```java
enum ModoOperativo {
    MANUAL,
    AUTO, 
    ECO,
    COMFORT,
    ANTIFREEZE,
    BOOST,
    STANDBY
}
```

**Error Codes**:
```java
enum Allarme {
    NO_ALARM,
    TEMPERATURE_SENSOR_ERROR,
    OVERHEATING,
    COMMUNICATION_ERROR
}
```

### 4.2 Status Byte Array Format

Device status is encoded as a byte array (13 bytes):
```
[0] Current Temperature
[1-2] CIP (Current in Progress) - Big Endian
[3] Operating Mode
[4] Eco Temperature
[5] Comfort Temperature  
[6] Antifreeze Temperature
[7] Boost Value
[8] Warning/Alarm Code
[9] Mode Settings (Celsius/Fahrenheit)
[10] Holiday Active (0/1)
[11] Boost Remaining Time
[12] Lock Active (0/1)
```

## 4. Device Hardware Limitations

### 4.1 Power Measurement Capability

Based on analysis of the decompiled Android app, power consumption measurement appears to be hardware-dependent:

- **Power_Consumption_Watt**: This field is directly reported by the device hardware and stored/relayed without modification by the firmware
- **Hardware Dependency**: Some device models/PCB versions may not include power measurement sensors
- **Zero Values**: Devices without power measurement capability will consistently report `Power_Consumption_Watt: 0`
- **No Software Detection**: The app does not check device model, PCB version, or firmware version to determine power measurement support

### 4.2 Identifying Power Measurement Support

**Indicators of Power Measurement Support**:
- `Load_Size_Watt` > 0 in device info (theoretical maximum power)
- Non-zero `Power_Consumption_Watt` values when heater is actively heating
- Device model and PCB version may indicate capability (check documentation)

**Expected Behavior**:
- Devices WITH power sensors: Report actual consumption when heating (e.g., 800-2000W depending on mode)
- Devices WITHOUT power sensors: Always report 0W regardless of operational state

**Recommendation for Integration**:
- Test initial device response to determine if power measurement is supported
- If `Power_Consumption_Watt` remains 0 during active heating, assume no power measurement capability
- Hide or disable power-related UI elements for devices that don't support measurement
````markdown
# Stone Connect WiFi Electric Heater - Communication Protocol Documentation

## Overview

This document provides a comprehensive analysis of the communication protocol used by the Stone Connect WiFi electric heater application. The system uses multiple communication methods:

1. **WiFi Provisioning** (ESP32-based using Protocol Buffers)
2. **HTTP REST API** (Local and Cloud communication)
3. **MQTT** (Eurotech cloud-based messaging)

## 1. WiFi Provisioning Protocol

### 1.1 ESP32 Provisioning System

The heater uses ESP32-based WiFi provisioning with Protocol Buffers for configuration.

#### Key Protocol Buffer Definitions:

**WiFi Configuration (`wifi_config.proto`)**:
```protobuf
message CmdSetConfig {
    bytes ssid = 1;
    bytes passphrase = 2;
    bytes bssid = 3;
    int32 channel = 4;
}

message RespGetStatus {
    Status status = 1;
    WifiStationState sta_state = 2;
    oneof state {
        WifiConnectFailedReason fail_reason = 10;
        WifiConnectedState connected = 11;
    }
}
```

**WiFi States (`wifi_constants.proto`)**:
```protobuf
enum WifiStationState {
    Connected = 0;
    Connecting = 1;
    Disconnected = 2;
    ConnectionFailed = 3;
}

enum WifiAuthMode {
    Open = 0;
    WEP = 1;
    WPA_PSK = 2;
    WPA2_PSK = 3;
    WPA_WPA2_PSK = 4;
    WPA2_ENTERPRISE = 5;
}
```

#### Provisioning Flow:

1. **Device Discovery**: Scan for WiFi networks with device prefix
2. **Connect to Device AP**: Connect to heater's access point
3. **Send WiFi Credentials**: Use `CmdSetConfig` to configure WiFi
4. **Apply Configuration**: Send `CmdApplyConfig` command
5. **Monitor Status**: Poll with `CmdGetStatus` until connected

#### Message Types:
- `TypeCmdGetStatus = 0` - Get current WiFi status
- `TypeCmdSetConfig = 2` - Set WiFi credentials
- `TypeCmdApplyConfig = 4` - Apply WiFi configuration

## 2. Local HTTPS API

### 2.1 Base Configuration

**Local API Configuration**:
- Protocol: HTTPS (TLS/SSL enabled)
- Port: 443 (standard HTTPS port)
- Base URL: `https://{device_ip}/Domestic_Heating/Radiators/v1/`
- Timeout: 30 seconds for connect/read/write operations
- Certificate: Self-signed (requires SSL verification bypass)

### 2.2 Authentication

**Local Authentication** (Required for all endpoints):
```
Authorization: Basic QXBwX1JhZFdpRmlfdmBgZWVqZnM0dzhlN3E1d2RhNHM1ZDFhczI=
```

**Decoded Credentials**:
- Username: `App_RadWiFi_v1`
- Password: `e1qf45s4w8e7q5wda4s5d1as2`

### 2.3 API Endpoints

All endpoints use the base URL: `https://{device_ip}/Domestic_Heating/Radiators/v1/`

#### Device Information
```http
GET /info
Response: Device information including model, version, capabilities
```

#### Device Status
```http
GET /Status
Response: Current temperature, setpoint, operation mode, heating status
```

#### Weekly Schedule
```http
GET /Schedule
Response: Weekly heating schedule with time points and temperatures
```

#### Temperature and Mode Control (Combined)
```http
PUT /setpoint
Body: {
  "Client_ID": "571519332SN20244900365",
  "Set_Point": 21.5,
  "Operative_Mode": "SET"
}
Response: Updated status confirmation
```

#### Device Control
```http
PUT /blink
Body: {} (triggers LED blink for device identification)

PUT /factoryReset
Body: {} (resets device to factory defaults)

PUT /putApplianceName
Body: {"name": "Living Room Heater"}
```

**Required Headers for all requests**:
```
Authorization: Basic QXBwX1JhZFdpRmlfdmBgZWVqZnM0dzhlN3E1d2RhNHM1ZDFhczI=
Content-Type: application/json
```

**Note**: Temperature and operation mode are set together via the `/setpoint` endpoint, not separately.
  - Authorization: Basic {auth}
  - Home_ID: {home_id}
  - Home_Token: {home_token}
```

### 2.4 URL Patterns

**Local URLs**:
```
http://{device_ip}/Domestic_Heating/Radiators/v1/{endpoint}
```

**Cloud URLs** (Base varies by environment):
```
https://api.cloud.com/v1/{endpoint}
```

### 2.5 Data Models

#### StatusNetworkObject
```json
{
  "Client_ID": "string",
  "Set_Point": 20.5,
  "Operative_Mode": "MANUAL|AUTO|ECO|COMFORT|ANTIFREEZE|BOOST",
  "Daily_Energy": 0,
  "Power_Consumption_Watt": 1200,
  "Error_Code": 0,
  "Error_Message": "string",
  "Last_Update": 1640995200000,
  "Broker_Enabled": true
}
```

#### Device Information
```json
{
  "Client_ID": "string",
  "Zone_Name": "Living Room",
  "Zone_ID": "zone_001",
  "MAC_Address": "AA:BB:CC:DD:EE:FF",
  "IP_Address": "192.168.1.100",
  "FW_Version": "1.2.3",
  "PCB_Version": "2.1",
  "Temperature_Unit": "CELSIUS|FAHRENHEIT",
  "High_Power": 1500,
  "Medium_Power": 1000,
  "Low_Power": 500,
  "Is_Installed": true
}
```

## 3. MQTT Protocol

### 3.1 Broker Configuration

**Primary Configuration** (`eurotech_config.json`):
```json
{
  "port": 1883,
  "sslEnabled": false,
  "willEnabled": false,
  "accountName": "Zoppas-Test",
  "username": "device_client_android",
  "password": "V9DefLgNHf!5Yss",
  "clientId": "my-Device-client",
  "url": "mqtt://broker-sandbox.everyware-cloud.com",
  "modelId": "stone"
}
```

**Environment-Specific Brokers**:
- **Sandbox**: `mqtt://broker-sandbox.everyware-cloud.com:1883`
- **Stage**: `mqtt://broker-stage.everyware-cloud.com:1883`  
- **Production**: `mqtt://broker.everyware-cloud.com:1883`

### 3.2 Topic Structure

**Data Topics**:
```
{account_name}/{client_id}/data
Zoppas-Test/my-Device-client/data
```

**Control Topics**:
```
$EDC/{account_name}/{client_id}/#
$EDC/{account_name}/$ALL/#
```

**Birth Certificate**:
```
$EDC/{account_name}/{client_id}/MQTT/BIRTH
```

**Last Will Testament**:
```
$EDC/{account_name}/{client_id}/MQTT/LWT
```

**Disconnect Certificate**:
```
$EDC/{account_name}/{client_id}/MQTT/DC
```

### 3.3 Message Format

**Statistics Message Example**:
```json
{
  "d": {
    "device": "smartphone",
    "statistics": {
      "day": [
        {
          "p": [
            "0:2:289:0",  // hour:mode:power:minute
            "0:1:189:1",
            "0:3:358:2"
          ],
          "d": 1438778407806  // timestamp
        }
      ]
    }
  }
}
```

**Device Status Payload**:
```json
{
  "timestamp": 1640995200000,
  "client_id": "device_001",
  "temperature": 21.5,
  "setpoint": 20.0,
  "mode": "AUTO",
  "power": 1200,
  "energy": 2.5
}
```

### 3.4 QoS Levels

- **Birth/Death Messages**: QoS 1 (at least once)
- **Data Messages**: QoS 0 (fire and forget)
- **Control Messages**: QoS 0 (fire and forget)

## 4. Device Status Protocol

### 4.1 BLE Configuration Values

**Temperature Encoding**:
- Celsius: Direct temperature value
- Fahrenheit: Converted value
- Special values: Antifreeze (-50), Standby (-51)

**Operating Modes**:
```java
enum ModoOperativo {
    MANUAL,
    AUTO, 
    ECO,
    COMFORT,
    ANTIFREEZE,
    BOOST,
    STANDBY
}
```

**Error Codes**:
```java
enum Allarme {
    NO_ALARM,
    TEMPERATURE_SENSOR_ERROR,
    OVERHEATING,
    COMMUNICATION_ERROR
}
```

### 4.2 Status Byte Array Format

Device status is encoded as a byte array (13 bytes):
```
[0] Current Temperature
[1-2] CIP (Current in Progress) - Big Endian
[3] Operating Mode
[4] Eco Temperature
[5] Comfort Temperature  
[6] Antifreeze Temperature
[7] Boost Value
[8] Warning/Alarm Code
[9] Mode Settings (Celsius/Fahrenheit)
[10] Holiday Active (0/1)
[11] Boost Remaining Time
[12] Lock Active (0/1)
```

## 4. Device Hardware Limitations

### 4.1 Power Measurement Capability

Based on analysis of the decompiled Android app, power consumption measurement appears to be hardware-dependent:

- **Power_Consumption_Watt**: This field is directly reported by the device hardware and stored/relayed without modification by the firmware
- **Hardware Dependency**: Some device models/PCB versions may not include power measurement sensors
- **Zero Values**: Devices without power measurement capability will consistently report `Power_Consumption_Watt: 0`
- **No Software Detection**: The app does not check device model, PCB version, or firmware version to determine power measurement support

### 4.2 Identifying Power Measurement Support

**Indicators of Power Measurement Support**:
- `Load_Size_Watt` > 0 in device info (theoretical maximum power)
- Non-zero `Power_Consumption_Watt` values when heater is actively heating
- Device model and PCB version may indicate capability (check documentation)

**Expected Behavior**:
- Devices WITH power sensors: Report actual consumption when heating (e.g., 800-2000W depending on mode)
- Devices WITHOUT power sensors: Always report 0W regardless of operational state

**Recommendation for Integration**:
- Test initial device response to determine if power measurement is supported
- If `Power_Consumption_Watt` remains 0 during active heating, assume no power measurement capability
- Hide or disable power-related UI elements for devices that don't support measurement
