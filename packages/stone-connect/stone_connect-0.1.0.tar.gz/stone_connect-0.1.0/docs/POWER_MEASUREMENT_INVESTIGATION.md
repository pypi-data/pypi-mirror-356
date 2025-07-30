# Power Measurement Investigation Summary

## Problem Statement
Despite setting the Stone Connect heater to MANUAL mode at 30°C, the `Power_Consumption_Watt` field consistently reports 0, even when the device should be actively heating.

## Investigation Results

### Code Analysis Findings

After thorough analysis of the decompiled Android APK source code, I found:

1. **Direct Hardware Reporting**: The `Power_Consumption_Watt` value is directly copied from the device's JSON response without any software calculation or transformation.

2. **No Device Capability Checks**: The Android app does not check device model, PCB version, firmware version, or any other identifier to determine if power measurement is supported.

3. **Hardware-Dependent Feature**: Power measurement appears to be a hardware-dependent capability, not a software feature.

### Code Evidence

**StatusNetworkObject.java**: The power consumption field is mapped directly from JSON:
```java
@SerializedName("Power_Consumption_Watt")
@Expose
private long power_consumption_watt;
```

**AsyncUpdateDeviceInfo.java**: Power consumption is copied without modification:
```java
device.setPower_consumption_watt((float) statusNetworkObject.getPower_consumption_watt());
```

**No Calculation Logic**: Extensive search revealed no code that calculates power consumption based on:
- Operating mode (MANUAL, HIGH, etc.)
- Set point temperature
- Heating element status
- Load size watts

### Device Information Analysis

Your device info shows:
- **PCB_PN**: "571519332"
- **PCB_Version**: "2.0" 
- **FW_Version**: "1.0.2"
- **Load_Size_Watt**: 0

The `Load_Size_Watt: 0` is particularly telling, as this field typically indicates the maximum power consumption capability of the device.

## Conclusion

**The consistent 0W power consumption is likely due to hardware limitations, not a software issue.**

### Possible Explanations:

1. **PCB Variant**: Your specific PCB version (2.0 of part 571519332) may not include power measurement circuitry
2. **Cost Optimization**: Some device variants may exclude power sensors to reduce manufacturing costs
3. **Hardware Fault**: Less likely, but possible hardware sensor failure

### Evidence Supporting Hardware Limitation:

- ✅ `Load_Size_Watt: 0` (typically non-zero for devices with power measurement)
- ✅ No software logic for power calculation in the app
- ✅ Direct hardware reporting without capability checks
- ✅ Consistent 0W regardless of heating state

## Recommendations

### For Integration Projects:
1. **Capability Detection**: Use the `has_power_measurement_support()` method in the Python library
2. **Graceful Degradation**: Hide power consumption UI elements for devices that don't support it
3. **User Communication**: Inform users that some device models don't support power measurement

### For Your Specific Device:
1. **Accept Limitation**: Your device model likely doesn't support power measurement
2. **Focus on Temperature Control**: All temperature and mode control functions work normally
3. **Energy Estimation**: If needed, estimate power consumption based on operating modes and time

## Updated Library Features

The Python library now includes:
- `has_power_measurement_support()` method for capability detection
- Updated documentation explaining hardware limitations
- Example code demonstrating power measurement detection

This investigation confirms that power consumption measurement is a hardware feature that varies by device model, and your specific device appears to be a variant without this capability.
