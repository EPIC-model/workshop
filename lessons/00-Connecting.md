# Connecting using SSH

The Cirrus login address is

```bash
login.cirrus.ac.uk
```

Access to Cirrus is via SSH using **both** a time-based code (TOTP) and a passphrase-protected SSH key pair.

# TOTP

A time based one time password (TOTP) is a credential that changes value over time (on Cirrus, the code changes every 30 seconds).
Users link a TOTP app on their mobile device or laptop to their Cirrus account using an initial *seed*
(usually provided by a QR code that you scan but can also be a string of characters)
and this then allows the app to produce codes that match the ones known by Cirrus.

When you create an account on Cirrus, you will need to register TOTP access in a suitable app.
Instructions for doing this [are available in the SAFE documentation](https://epcced.github.io/safe-docs/safe-for-users/#how-to-turn-on-mfa-on-your-machine-account).

You only need to enter the TOTP once every 10 hours for each account and local host that you connect to Cirrus from.

# SSH keys

As well as TOTP, users are required to add the public part of an SSH key pair to access Cirrus.
The public part of the key pair is associated with your account using the SAFE web interface.
See the Cirrus User and Best Practice Guide for information on how to create SSH key pairs and associate them with your account:

* [Connecting to Cirrus](https://docs.cirrus.ac.uk/user-guide/connecting/)

# Log in to Cirrus

Once you have managed to setup your TOTP and SSH key pair try to log into Cirrus for the first time using the command:

```bash
ssh -i /path/to/sshkey username@login.cirrus.ac.uk
```

# Data transfer services: scp, rsync

Cirrus supports a number of different data transfer mechanisms.
The one you choose depends on the amount and structure of the data you want to transfer and where you want to transfer the data to.
The three main options are:

* `scp`: The standard way to transfer small to medium amounts of data off Cirrus to any other location
* `rsync`: Used if you need to keep small to medium datasets synchronised between two different locations

More information on data transfer mechanisms can be found in the Cirrus User and Best Practice Guide:

* [Data management and transfer](https://docs.cirrus.ac.uk/user-guide/data/)

## Data transfer best practice

There is a lot of information available in the Cirrus documentation
on how to transfer data using the methods above and how to make it efficient in the documentation linked above.

Here are the main points you should consider:

* **Not all data are created equal, understand your data.**
  Know what data you have.
  What is your critical data that needs to be copied to a secure location?
  Which data do you need in a different location to analyse?
  Which data would it be easier to regenerate rather than transfer?
  You should create a brief data management plan laying this out as this will allow you to understand which tools to use and when.

* **Minimise the data you are transferring.**
  Transferring large amounts of data is costly in both researcher time and actual time.
  Make sure you are only transferring the data you need to transfer.

* **Minimise the number of files you are transferring.**
  Each individual file has a static overhead in data transfers so it is efficient to bundle multiple files together into a single large archive file for transfer.

* **Does compression help or hinder?**
  Many tools have the option to use compression (e.g. `rsync`, `tar`, `zip`) and generally encourage you to use them to reduce data volumes.
  However, in some cases, the time spent compressing the data can take longer than actually transferring the uncompressed data;
  particularly when transferring data between two locations that both have large data transfer bandwidth available.

* **Be aware of encryption overheads.**
  When transferring data using `scp` (and `rsync` over `scp`) your data will be encrypted introducing a static overhead per file.
  This issue can be minimised by reducing the number files to be transferred by creating archives.
  You can also change the encryption algorithm to one that involves minimal encryption.
  The fastest performing cipher that is commonly available in SSH at the moment
  is generally `aes128-ctr` as most common processors provide a hardware implementation.
