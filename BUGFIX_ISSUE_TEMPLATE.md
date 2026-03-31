# Bug: Incorrect Scale Factor for Temperature Sensors t_acs_raw and t_ambiente_raw

## Description
The temperature sensors `t_acs_raw` and `t_ambiente_raw` have incorrect scale factors in the Modbus register configuration. Currently set to `scale: 1`, but should be `scale: 0.1` to properly divide the raw values by 10.

## Affected Registers
- **t_acs_raw** (register 8988): ACS temperature sensor
- **t_ambiente_raw** (register 8992): Internal ambient temperature sensor

## Current Configuration (Incorrect)
```python
{
    "key": "t_acs_raw",
    "name": "Temperatura ACS",
    "register": 8988,
    "scale": 1,  # ❌ Should be 0.1
    ...
},
{
    "key": "t_ambiente_raw", 
    "name": "Temperatura ambiente interno",
    "register": 8992,
    "scale": 1,  # ❌ Should be 0.1
    ...
}
```

## Expected Configuration (Fixed)
```python
{
    "key": "t_acs_raw",
    "name": "Temperatura ACS", 
    "register": 8988,
    "scale": 0.1,  # ✅ Correct scale factor
    ...
},
{
    "key": "t_ambiente_raw",
    "name": "Temperatura ambiente interno",
    "register": 8992, 
    "scale": 0.1,  # ✅ Correct scale factor
    ...
}
```

## Impact
- Temperature readings are displayed 10x higher than actual values
- Incorrect temperature monitoring for ACS and ambient sensors
- Potential issues with automation and climate control

## Resolution
✅ **FIXED**: Updated scale factor from `1` to `0.1` for both sensors in `const.py`

## Files Changed
- `const.py`: Corrected scale factors for t_acs_raw and t_ambiente_raw

## Testing
- Verify temperature readings are now accurate (divided by 10)
- Check that values make sense for typical indoor/outdoor temperatures
- Ensure no regression in other temperature sensors

## Labels
- bug
- temperature
- modbus
- sensors