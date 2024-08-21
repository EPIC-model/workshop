# Accessing the Cirrus cluster

Detailed information about the Cirrus cluster can be found in the [Cirrus website](https://www.cirrus.ac.uk/about/hardware.html) and in [this repo](lessons/01-Cirrus.md).

#### Summary:
  * Create SSH key-pair
  * Create SAFE account
  * Accept invite to `d185`, you will need to add the public part of an SSH key-pair to the `d185` machine account in SAFE when accepting the invite
  * Create an MFA token for the `d185` machine account on SAFE
  * Login to cirrus using an ssh client with: `ssh -i /path/to/your-ssh-private-key your_username@login.cirrus.ac.uk`
  * Type your TOTP/MFA code, which only be asked once a day (unless your IP changes, then you'll be asked for another TOTP)

#### Detailed Instructions:

The steps below will also be sent to your email, with the invite to join the `d185` project.

To get an account on Cirrus, a Tier 2 national HPC service from the EPSRC in the UK,
first you'll need an account on SAFE, the Service Administration service ran by EPCC.

You can register for a SAFE account following the steps detailed in the
[SAFE documentation](https://epcced.github.io/safe-docs/safe-for-users/#registering-logging-in-passwords),
please register using the same email address that the invite was sent to.

You will need to accept the invite to join `d185`, create an SSH key-pair --
[more instructions here](https://docs.cirrus.ac.uk/user-guide/connecting/#ssh-key-pairs) --
and add it to the `d185` machine account.
You can either upload the public key file, or paste the text the file contains, i.e., copy the output of:

```bash
cat /path/to/your/key
```

You will then need to setup an MFA (multi-factor authentication) method for time based one
time passwords (TOTP) and link it to your machine account,
[see instructions here](https://docs.cirrus.ac.uk/user-guide/connecting/#time-based-one-time-passcode-totp-code).

To login, use:

```bash
ssh -i /path/to/your/ssh/key user@login.cirrus.ac.uk

# for example, for the user "d185-rfga" using a linux system:
ssh -i ~/.ssh/id_rsa_cirrus d185-rfga@login.cirrus.ac.uk
```
> [!NOTE]
> More details on how to login can be found [in the Cirrus documentation](https://docs.cirrus.ac.uk/user-guide/connecting/#ssh-clients)
> and in [this repo](lessons/00-Connecting.md).
