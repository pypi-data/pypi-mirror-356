#!/usr/bin/python3

import pyvisa, logging, sys, asyncio, time, sys

from os import environ

import caproto

from caproto.server import PVGroup, pvproperty
from caproto.asyncio.server import Context as ServerContext

PfeifferResponses = {
    'ETX': b'\x03',
    'CR':  b'\r',
    'LF':  b'\n',
    'ENQ': b'\x05',
    'ACK': b'\x06',
    'NAK': b'\x15'
}

PfeifferGaugeStatus = {
    0: "ok",
    1: "underrange",
    2: "overrange",
    3: "sensor-error",
    4: "sensor-off",
    5: "no-gauge",
    6: "id-error"
}


class PfeifferDevice:
    ''' Encapsulates access to a Pfeiffer/Balzer pump controller.

    Does async communication only.
    '''

    def __init__(self, dev=None, rman=None):
        if dev is None:
            dev = environ.get('PFEIFFER_VISA_DEVICE', None)

        if rman is None:
            rman = environ.get('PFEIFFER_VISA_RMAN', '@py')

        if dev is None:
            raise RuntimeError(f'No device specified')

        logging.info(f'Opening: {dev} via {rman}')

        self.dev = dev
        self.rman = pyvisa.ResourceManager(rman)
        self.instr = self.rman.open_resource(self.dev,
                                             read_termination = '\r\n',
                                             write_termination = None,
                                             timeout = 0)


    async def tx(self, data, end=None, validate=None, timeout=1.0):
        '''
        Executes one send-receive cycle with the Pfeiffer.
        '''

        if isinstance(data, str):
            data = data.encode('utf-8')

        l = self.instr.write_raw(data)
        if l != len(data):
            raise RuntimeError(f'Error writing request: {l} '
                               f'bytes written, should have been {len(data)+1}')
        return await self.read(end, timeout, validate)


    async def request(self, r, timeout=1.0):
        def _is_ack(data):
            return data == PfeifferResponses['ACK']

        return await self.tx(r+'\r', end=self.instr.read_termination.encode('utf-8'),
                             timeout=timeout, validate=_is_ack)


    async def enquire(self, timeout=1.0):
        def _is_non_zero(data):
            return len(data) > 0

        return await self.tx(PfeifferResponses['ENQ'], timeout=timeout,
                             end=self.instr.read_termination.encode('utf-8'),
                             validate=_is_non_zero)


    async def read(self, end=None, timeout=1.0, validate=None):
        '''
        Asynchronously performs one read operation.

        Note that this relies on TCP/IP read timeout being 0,
        and repeatedly pollig the device until a full message
        is constructured (with short async sleeps in between).
        This has been known to fail in the past, depending on
        the specific pyVISA device (seems to work with TCP/IP
        most of the time).

        If you encounter problems, this needs to be rewritten.
        '''
        t0 = time.time()
        result = bytes()
        while True:
            try:
                result += self.instr.read_raw()
                if (end is not None):
                    if (result[-len(end):] == end):
                        result = result[:-len(end)]
                        break
                else:
                    break

            except pyvisa.VisaIOError as e:
                tnow = time.time()
                if (tnow-t0) >= timeout:
                    logging.info(f'Real timeout: {str(e)}')
                    raise e
                else:
                    await asyncio.sleep(0.00001)
                    continue

        if validate is None:
            return result.decode('utf-8')
        elif validate(result):
            return result.decode('utf-8')

        raise RuntimeError(f'Bad query: "{data}", response: "{result}"')


    async def PRX(self):
        await self.request('PRX')
        res = await self.enquire()
        str_data = res.split(',')
        data = []
        for s in str_data:
            try:
                data.append(int(s))
            except ValueError:
                try:
                    data.append(float(s))
                except ValueError:
                    data.append(s)
        return data


async def loop(pv_dict):

    ctx = ServerContext(pv_dict)
    asyncio.create_task(ctx.run())

    while True:
        await asyncio.sleep(1.0)


class PfeifferGaugeIOC(PVGroup):
    ''' Encapsulates PV definitions for one single gauge.

    Needs PfeifferIOC to function (is actually used within that).
    '''

    VALUE = pvproperty(value=0.0, doc="Gauge value")
    STATUS = pvproperty(value="n/a",
                        doc="Gauge status",
                        dtype=caproto.ChannelType.STRING,
                        string_encoding='latin-1')

    def __init__(self, prefix):
        super().__init__(prefix=prefix)

    async def set_values(self, status, measure):

        if self.STATUS.value != status:
            await self.STATUS.write(value=status)

        if self.VALUE.value != measure:
            await self.VALUE.write(value=measure)


class PfeifferIOC(PVGroup):
    ''' Top-level IOC control for a Pfeiffer device.

    This implements the master polling loop (see .POLL.startup()).
    It is important that instrument access only happens in one
    spot (i.e. here) to keep the dialogue consistent.

    Publication of values for indivitual gauges is delegated
    to several PfeifferGaugeIOC instance (see self.gauges).
    '''

    POLL = pvproperty(value="hello")

    def __init__(self, prefix, device, nr_gauges=6, poll_wait=0.5):
        '''
        Args:
            nr_gauges: how many gauges are attached to the controller
            poll_wait: how much to pause between instrument status polls
        '''
        self.instr = device
        self.poll_wait = poll_wait
        super().__init__(prefix)

        self.gauges = [
            PfeifferGaugeIOC(prefix=f"{prefix}G{i+1}:")
            for i in range(nr_gauges)
        ]


    def get_pv_dict(self):
        pv_dict = {}
        pv_dict.update(self.pvdb)
        for g in self.gauges:
            pv_dict.update(g.pvdb)
        return pv_dict


    @POLL.startup
    async def POLL(self, instance, value):
        while True:
            try:
                data = await self.instr.PRX()

                #logging.info(f'Pfeiffer data: {data}')

                for g,s,m in zip(self.gauges, data[0::2], data[1::2]):
                    await g.set_values(PfeifferGaugeStatus[s], m)

                await asyncio.sleep(self.poll_wait)

            except:
                await asyncio.sleep(3.0)
                raise


def main(prefix=None, args=None):

    logging.basicConfig(level=logging.INFO)

    if prefix is None:
        prefix = environ.get('PFEIFFER_EPICS_PREFIX', 'DOODLE:')

    if args is None:
        args = sys.argv

    instrument = environ.get('PFEIFFER_VISA_DEVICE',
                             "TCPIP::192.168.169.190::8000::SOCKET")

    nr_gauges = int(environ.get('PFEIFFER_NR_GAUGES', '6'))

    device = PfeifferDevice(dev=insrument)

    ioc = PfeifferIOC(prefix=prefix,
                      device=device,
                      nr_gauges=nr_gauges)

    pvs = ioc.get_pv_dict()

    logging.info("Have PVs:")
    for k in pvs:
        logging.info(f'  {k}')

    asyncio.run(loop(pvs))


if __name__ == "__main__":
    main()
