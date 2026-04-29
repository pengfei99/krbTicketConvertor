# krbTicketConvertor

The objective of this project is 
1. to get a kerberos ticket with tool such as [rubeus](https://github.com/ghostpack/rubeus).
2. to convert a kerberos ticket from format `.kirbi` to MIT Kerberos ccache file. 

## Get a delegated TGT

The first step is to get a TGT. We use a tool called `rubeus`, https://github.com/ghostpack/rubeus


### tgtdeleg

The tgtdeleg using @gentilkiwi's Kekeo trick (tgt::deleg) that abuses the Kerberos GSS-API to retrieve a usable TGT for the current user without needing elevation on the host. AcquireCredentialsHandle() is used to get a handle to the current user's Kerberos security credentials, and InitializeSecurityContext() with the `ISC_REQ_DELEGATE` flag and a target `SPN of HOST/DC.domain.com` to prepare a fake delegate context to send to the DC. This results in an AP-REQ in the GSS-API output that contains a KRB_CRED in the authenticator checksum. The service ticket session key is extracted from the local Kerberos cache and is used to decrypt the KRB_CRED in the authenticator, resulting in a usable TGT `.kirbi`.

If automatic target/domain extraction is failing, a known SPN of a service configured with unconstrained delegation can be specified with /target:SPN.


## Dev env

This project use `.NET Framework 4.8 Developer Pack`. Because for the windows server 2019, `4.8.1` is not supported.

To build the dev env, I use `.Net 8.0 SDK`. Because, it’s the most stable "long-term" version that includes the CLI.

> You can get the `.NET Framework 4.8 Developer Pack` via https://dotnet.microsoft.com/en-us/download/dotnet-framework/thank-you/net48-developer-pack-offline-installer.
> You need admin right to install it, and you need to restart after installation.
> after your installation, you should find the `MSBuild.exe` under `C:\Windows\Microsoft.NET\Framework64\v4.0.30319\`

> You can use the vscode extension `.net install tool`(this extention will be install automatically after your install C# Dev Kit) to install the `.Net 8.0 SDK`. 
> after your installation, you should find the folder under `C:\Program Files\dotnet\`.


### SDK vs Developer Pack

The SDK and developer Pack are two different things:

- The `Developer Pack`: installs the compilers (like csc.exe) and libraries, but it does not include the dotnet CLI tool. That tool only comes with .NET Core, .NET 5, 6, 7, 8, or 10.

- The `.NET SDK`: all you to use the dotnet command in PowerShell (e.g. dotnet --version). A modern version(e.g. 8.0) allow you to build with older version developer pack(e.g. 4.8) 


### Check your env

```powershell
# check your sdk version.
dotnet --version
8.0.101
```

### Create your C# project

```powershell
# this command will generate a project skeleton with .net 8.0
dotnet new console -n KrbConverter

cd KrbConverter
```

You will find two files:
- KrbConverter.csproj
- Program.cs


You need to replace the generated `KrbConverter.csproj` with the below content

```.csproj
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net48</TargetFramework>
    <RootNamespace>KrbConverter</RootNamespace>
    <Platforms>AnyCPU;x64</Platforms>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Kerberos.NET" />
  </ItemGroup>

</Project>
```

Install the required package

```powershell
dotnet add package Kerberos.NET
```

> The latest version is `4.6.146`

This file defines how dotnet build the .exe

```powershell
# build a .exe
dotnet restore
dotnet build -c Release
```

You will find a .exe in your `bin/Release/net48` 


If you have error during your build, you need to clean the project before you rebuild the 

```powershell
dotnet clean
```
