import multicoin
from .. import utils
from ..script import serialization as script_ser


def make_sh_address(script_string, witness=False):
    addr_bytes = bytearray()
    script_bytes = script_ser.serialize_from_string(script_string)
    if witness:
        script_hash = utils.sha256(script_bytes)
        addr_bytes.extend(multicoin.network.P2WSH_PREFIX)
        addr_bytes.extend(script_hash)
        return multicoin.network.SEGWIT_ENCODER.encode(addr_bytes)
    else:
        script_hash = utils.hash160(script_bytes)
        addr_bytes.extend(multicoin.network.P2SH_PREFIX)
        addr_bytes.extend(script_hash)
        return multicoin.network.LEGACY_ENCODER.encode(addr_bytes)


def make_p2wsh_address(script_string):
    return make_sh_address(script_string, witness=True)


def make_p2sh_address(script_string):
    return make_sh_address(script_string, witness=False)


def make_pkh_address(pubkey, witness=False):
    addr_bytes = bytearray()
    pubkey_hash = utils.hash160(pubkey)
    if witness:
        addr_bytes.extend(multicoin.network.P2WPKH_PREFIX)
        addr_bytes.extend(pubkey_hash)
        return multicoin.network.SEGWIT_ENCODER.encode(addr_bytes)
    else:
        addr_bytes.extend(multicoin.network.P2PKH_PREFIX)
        addr_bytes.extend(pubkey_hash)
        return multicoin.network.LEGACY_ENCODER.encode(addr_bytes)


def make_p2wpkh_address(pubkey):
    return make_pkh_address(pubkey, witness=True)


def make_p2pkh_address(pubkey):
    return make_pkh_address(pubkey, witness=False)


def parse(address):
    try:
        return bytearray(multicoin.network.LEGACY_ENCODER.decode(address))
    except:
        try:
            return bytearray(multicoin.network.SEGWIT_ENCODER.decode(address))
        except:
            raise ValueError(
                'Unsupported address format: {}'.format(address))


def parse_pkh_address(address):
    return parse(address)


def parse_p2wpkh_address(address):
    return parse_pkh_address(address)


def parse_p2pkh_address(address):
    return parse_pkh_address(address)


def parse_sh_address(address):
    return parse(address)


def parse_p2sh_address(address):
    return parse_sh_address(address)


def parse_p2wsh_address(address):
    return parse_sh_address(address)


def parse_hash(address):
    '''
    There's probably a better way to do this.
    '''

    raw = parse_sh_address(address)

    try:
        address.find(multicoin.network.BECH32_HRP)  # errors on NoneType
        if raw.find(multicoin.network.P2WPKH_PREFIX) != -1:
            return raw[len(multicoin.network.P2WPKH_PREFIX):]
        if raw.find(multicoin.network.P2WPKH_PREFIX) != -1:
            return raw[len(multicoin.network.P2WPKH_PREFIX):]
    except:
        pass

    if raw.find(multicoin.network.P2SH_PREFIX) != -1:
        return raw[len(multicoin.network.P2SH_PREFIX):]
    if raw.find(multicoin.network.P2PKH_PREFIX) != -1:
        return raw[len(multicoin.network.P2PKH_PREFIX)]

    raise ValueError(
        'Network {} does not support address format: {} '
        .format(multicoin.get_current_network(), address))