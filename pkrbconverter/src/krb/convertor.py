import base64

from asn1crypto import core
from minikerberos.common.ccache import CCACHE, Credential, CCACHEPrincipal, Times, Keyblock, CCACHEOctetString
from minikerberos.common.kirbi import Kirbi
from minikerberos.protocol.asn1_structs import EncKrbCredPart, TicketFlags, Ticket


def from_kirbi(kirbi: Kirbi):
    krbcred = kirbi.kirbiobj.native
    c = Credential()
    enc_credinfo = EncKrbCredPart.load(krbcred['enc-part']['cipher']).native
    ticket_info = enc_credinfo['ticket-info'][0]

    c.client = CCACHEPrincipal.from_asn1(ticket_info['pname'], ticket_info['prealm'])
    # yaaaaay 4 additional weirdness!!!!
    # if sname name-string contains a realm as well htne impacket will crash miserably :(
    if len(ticket_info['sname']['name-string']) > 2 and ticket_info['sname']['name-string'][-1].upper() == ticket_info[
        'srealm'].upper():
        print('SNAME contains the realm as well, trimming it')
        t = ticket_info['sname']
        t['name-string'] = t['name-string'][:-1]
        c.server = CCACHEPrincipal.from_asn1(t, ticket_info['srealm'])
    else:
        c.server = CCACHEPrincipal.from_asn1(ticket_info['sname'], ticket_info['srealm'])

    c.time = Times.from_asn1(ticket_info)
    c.key = Keyblock.from_asn1(ticket_info['key'])
    c.is_skey = 0  # not sure!

    c.tktflags = TicketFlags(ticket_info['flags']).cast(core.IntegerBitString).native
    c.num_address = 0
    c.num_authdata = 0
    c.ticket = CCACHEOctetString.from_asn1(
        Ticket(krbcred['tickets'][0]).dump())  # kirbi only stores one ticket per file
    c.second_ticket = CCACHEOctetString.empty()

    return c

def convert_kirbi(src:str, dest:str)->None:
    """

    :param src: The path of source .kirbi file which contains the tgt binary in base64 format
    :param dest: The path of converted MIT ccache file
    :return:
    """
    kirbi_b64 = open(src, "rb").read()
    kirbi_byte = base64.b64decode(kirbi_b64)

    cc = CCACHE.from_bytes(kirbi_byte)

    cc.to_file(dest)

    print("done")