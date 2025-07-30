# Python library for instrumenting FleaScope

With this library, you can control and read your [FleaScope(s)](https://rtestardi.github.io/usbte/flea-scope.pdf).

# Usage

Connect to your FleaScope

```python
from pyfleascope.flea_scope import FleaScope

scope = FleaScope.connect() # for default hostname FleaScope
# scope = FleaScope.connect('scope1')
# scope = FleaScope.connect(port='/dev/ttyACM0')
```
Connecting by name will also take care of resetting the device if necessary.

Get your first reading from the BNC connector
```python
df = scope.x1.read(timedelta(milliseconds=20))['bnc']
```

## Calibration

Calibration values are by default read from flash upon connection.
If necessary, recalibration can be performed via

```python
# BNC probe in x1 mode
# Connect probe to GND
scope.x1.calibrate_0()
# Connect probe to 3.3V
scope.x1.calibrate_3v3()
scope.x1.write_calibration_to_flash()

# BNC probe in x10 mode
# Connect probe to GND
scope.x10.calibrate_0()
# Connect probe to 3.3V
scope.x10.calibrate_3v3()
scope.x10.write_calibration_to_flash()
```

## Triggers
Trigger reading on analog edges
```python
from pyfleascope.trigger_config import AnalogTrigger

df = scope.x1.read(
            timedelta(milliseconds=20),
            trigger=AnalogTrigger.start_capturing_when().rising_edge(volts=2),
)
```

or on digital signals
```python
from pyfleascope.trigger_config import DigitalTrigger, BitState

df = scope.x1.read(
            timedelta(milliseconds=20),
            trigger=DigitalTrigger.start_capturing_when()
              .bit1(BitState.HIGH)
              .bit7(BitState.LOW)
              .starts_matching(),
)
```

## Delay
Start capturing with a delay.
```python
df = scope.x1.read(
            timedelta(milliseconds=20),
            trigger=AnalogTrigger.start_capturing_when().rising_edge(volts=2),
            delay=timedelta(milliseconds=0.2),
)
```

## Waveform
Configure the built-in waveform generator.

```python
from pyfleascope.flea_scope import Waveform

scope.set_waveform(Waveform.EKG, hz=1000)
```

## Digital inputs
The digital input is captured in the column `bitmask`.
The function `extract_bits` extracts boolean columns `bit_$i` for each bit.

```python
df = scope.x1.read(
            timedelta(milliseconds=20),
            trigger=DigitalTrigger.start_capturing_when()
              .bit0(BitState.HIGH)
              .bit1(BitState.HIGH)
              .starts_matching(),
)
df = FleaScope.extract_bits(df)
df['bit_0'] = df['bit_0'].apply(int)
```

## Using multiple FleaScopes

Multiple FleaScopes can be used at the same time.
For exact timing alignment, the trigger signal can be forwarded.

```python
scope1 = FleaScope.connect('scope1')
scope2 = FleaScope.connect('scope2')


capture_time = timedelta(microseconds=120)

# Capture data from two FleaScopes at the same time by forwarding the trigger
# TRIGGER_OUT on scope1 is connected to Bit 0 on scope2 via cable

def read_scope1():
    time.sleep(1) # give scope1 time to prepare
    return scope1.x1.read(
        capture_time,
        AnalogTrigger.start_capturing_when().auto(2),
    )

def read_scope2():
    return scope2.x1.read(
            capture_time,
            DigitalTrigger.start_capturing_when().bit0(BitState.HIGH).starts_matching(),
    )

with ThreadPoolExecutor(max_workers=8) as executor:
    f1 = executor.submit(read_scope1)
    f2 = executor.submit(read_scope2)
    df1 = f1.result()
    df2 = f2.result()
```

## Cancel ongoing read

While waiting for the trigger or capturing values, the FleaScope is unresponsive.
The ongoing read operation can be canceled via the `unblock` method.

```python
scope.unblock()
```
