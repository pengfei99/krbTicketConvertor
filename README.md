# krbTicketConvertor

The objective of this project is 
1. to get a kerberos ticket(delegable TGT) with tool such as [rubeus](https://github.com/ghostpack/rubeus) or homemade.
2. to convert a kerberos ticket from format `.kirbi` to MIT Kerberos cache file. 

## Get a delegated TGT

The first step is to get a TGT. We use a tool called `rubeus`, https://github.com/ghostpack/rubeus

The main code of how rubeus get the TGT is in class [LSA.cs](https://github.com/GhostPack/Rubeus/blob/master/Rubeus/lib/LSA.cs)

The function is called `RequestFakeDelegTicket`


## tgtdeleg of LSA

The `tgtdeleg` using @gentilkiwi's Kekeo trick (tgt::deleg) that abuses the `Kerberos GSS-API` to retrieve a 
usable TGT for the current user without needing elevation on the host. `AcquireCredentialsHandle()` is used to get 
a handle to the current user's Kerberos security credentials, and `InitializeSecurityContext()` with the `ISC_REQ_DELEGATE` 
flag and a target `SPN of HOST/DC.domain.com` to prepare a fake delegate context to send to the DC. 
This results in an AP-REQ in the GSS-API output that contains a KRB_CRED in the authenticator checksum. 

The service ticket session key is extracted from the local Kerberos cache and is used to decrypt the `KRB_CRED` in the 
authenticator, resulting in a usable TGT `.kirbi`.

If automatic `target/domain` extraction is failing, a known SPN of a service configured with unconstrained delegation can be specified with /target:SPN.


## .kirbi vs CCACHE

As you can notice, the output of the `Kerberos ticket` is in format `.kirbi` which is not the standard MIT cache format.
And many tools only support MIT cache format.

| Feature	   | KIRBI (Windows/Internal)           | 	CCACHE (MIT/Linux)          |
|------------|------------------------------------|------------------------------|
| Encoding   | 	ASN.1 DER (usually)	              | Specialized Binary Format    |
| Origin     | 	Microsoft KRB-CRED                | 	MIT Kerberos V5             |
| Usage      | 	Pass-the-Ticket (Rubeus/Mimikatz) | 	Standard Linux Auth (kinit) |
| Structure	 | Nested ASN.1 Sequences	            | Header + Credential List     |


## The TGT deleg of ssh

Here is the step-by-step breakdown of how that `TGT` travels from your `Windows machine` to the Linux server.

### The TGT Generation (On your Windows Machine)

When you log in to your Windows server, a TGT is generated and stored in your local cache (i.e. LSASS).
When you run `ssh -k user@srv1.example.com`: 
1. `Requesting a Service Ticket`: Your SSH client asks your local Kerberos implementation for a Service Ticket for the remote server (host/srv1.example.com).
2. The "Forwardable" Flag: Because you specified delegation, your client asks the Key Distribution Center (KDC) for 
       a `new, forwardable TGT`.
3. The Package: The KDC sends back a TGT encrypted in a way that only you can open. Your `Windows machine` then wraps 
           this TGT inside the `GSSAPI authentication layer of the SSH protocol.2`. 

### The TGT Forwarding

The TGT is sent over the encrypted SSH tunnel. It is never sent in the clear.It is bundled inside the SSH 
"User Authentication" packet. It travels from your `Windows machine` to the `sshd daemon on the Linux server`.

### The CCache file creation

(On the Linux Server)Once the Linux server receives your delegated credentials, the `SSH Daemon (sshd)` manage the rest.
1. The sshd process receives the GSSAPI data containing the TGT
2. The sshd (which usually runs as root initially) creates a new, temporary file. By default, this is usually located in /tmp/krb5cc_UID_XXXXXX
3. The sshd changes the ownership of this file to your user account and sets permissions so only you can read it (600).
4. The sshd sets the `KRB5CCNAME environment variable` in your shell session. This tells other tools (e.g. klist, nfs, or ldapsearch) 
      exactly where to find that ticket.
