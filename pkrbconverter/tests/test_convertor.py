from krb.convertor import convert_kirbi


def test_convertor():
    kirbi = "C:/Users/pliu/Documents/git/krbTicketConvertor/pkrbconverter/tests/tmp/tgt.kirbi"
    ccache = "C:/Users/pliu/Documents/git/krbTicketConvertor/pkrbconverter/tests/tmp/tgt.ccache"

    convert_kirbi(kirbi, ccache)
