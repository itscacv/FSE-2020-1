#Carvente Velasco Carlos Alberto
#Hernandez Romero Pompeyo
#practica 6
#set del reloj en tiempo real modulo DS1307

from datetime import datetime

import smbus

def _int_to_bcd(n):
    """Encode a one or two digits number to the BCD.
    """
    bcd = 0
    for i in (n // 10, n % 10):
        for p in (8, 4, 2, 1):
            if i >= p:
                bcd += 1
                i -= p
            bcd <<= 1
    return bcd >> 1

class DS1307():
    _REG_SECONDS = 0x00
    _REG_MINUTES = 0x01
    _REG_HOURS = 0x02
    _REG_DAY = 0x03
    _REG_DATE = 0x04
    _REG_MONTH = 0x05
    _REG_YEAR = 0x06
    _REG_CONTROL = 0x07

    def __init__(self, twi=1, addr=0x68):
        self._bus = smbus.SMBus(twi)
        self._addr = addr


    def _write(self, register, data):
        self._bus.write_byte_data(self._addr, register, data)

    def write_all(self, seconds=None, minutes=None, hours=None, day=None,
            date=None, month=None, year=None, save_as_24h=True):
        """Direct write un-none value.
        Range: seconds [0,59], minutes [0,59], hours [0,23],
               day [0,7], date [1-31], month [1-12], year [0-99].
        """
        if seconds is not None:
            if seconds < 0 or seconds > 59:
                raise ValueError('Seconds is out of range [0,59].')
            self._write(self._REG_SECONDS, _int_to_bcd(seconds))

        if minutes is not None:
            if minutes < 0 or minutes > 59:
                raise ValueError('Minutes is out of range [0,59].')
            self._write(self._REG_MINUTES, _int_to_bcd(minutes))

        if hours is not None:
            if hours < 0 or hours > 23:
                raise ValueError('Hours is out of range [0,23].')
            if save_as_24h:
                self._write(self._REG_HOURS, _int_to_bcd(hours) | 0x40)
            else:
                if hours == 0:
                    h = _int_to_bcd(12) | 0x32
                elif hours <= 12:
                    h = _int_to_bcd(hours)
                else:
                    h = _int_to_bcd(hours - 12) | 0x32
                self._write(self._REG_HOURS, h)

        if year is not None:
            if year < 0 or year > 99:
                raise ValueError('Years is out of range [0,99].')
            self._write(self._REG_YEAR, _int_to_bcd(year))

        if month is not None:
            if month < 1 or month > 12:
                raise ValueError('Month is out of range [1,12].')
            self._write(self._REG_MONTH, _int_to_bcd(month))

        if date is not None:
            if date < 1 or date > 31:
                raise ValueError('Date is out of range [1,31].')
            self._write(self._REG_DATE, _int_to_bcd(date))

        if day is not None:
            if day < 1 or day > 7:
                raise ValueError('Day is out of range [1,7].')
            self._write(self._REG_DAY, _int_to_bcd(day))


def main():
    ds = DS1307(1, 0x68)
    ds.write_all(seconds=0, minutes=16, hours=1, day=3, date=8, month=10, year=19)

main()