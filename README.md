# krbTicketConvertor

The objective of this project is 
1. to get a kerberos ticket with tool such as [rubeus](https://github.com/ghostpack/rubeus).
2. to convert a kerberos ticket from format `.kirbi` to MIT Kerberos ccache file. 

## Get a delegated TGT

The first step is to get a TGT. We use a tool called `rubeus`, https://github.com/ghostpack/rubeus


### tgtdeleg

The tgtdeleg using @gentilkiwi's Kekeo trick (tgt::deleg) that abuses the Kerberos GSS-API to retrieve a usable TGT for the current user without needing elevation on the host. AcquireCredentialsHandle() is used to get a handle to the current user's Kerberos security credentials, and InitializeSecurityContext() with the `ISC_REQ_DELEGATE` flag and a target `SPN of HOST/DC.domain.com` to prepare a fake delegate context to send to the DC. This results in an AP-REQ in the GSS-API output that contains a KRB_CRED in the authenticator checksum. The service ticket session key is extracted from the local Kerberos cache and is used to decrypt the KRB_CRED in the authenticator, resulting in a usable TGT `.kirbi`.

If automatic target/domain extraction is failing, a known SPN of a service configured with unconstrained delegation can be specified with /target:SPN.

