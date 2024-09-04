Next: [Setting up the environment](02-setup_environment.md), Previous: [Installing X-Windows](00-xwindow.md), Up: [Main page](../README.md)

# Accessing the Cirrus cluster

Detailed information about the Cirrus cluster can be found in the [Cirrus website](https://www.cirrus.ac.uk/about/hardware.html) and in [this repo](../lessons/01-Cirrus.md).

#### Summary:
  * Create SSH key-pair
  * Create SAFE account
  * Accept invite to `tc066`, you will need to add the public part of an SSH key-pair to the `tc066` machine account in SAFE when accepting the invite
  * Create an MFA token for the `tc066` machine account on SAFE
  * Login to cirrus using an ssh client with: `ssh -i /path/to/your-ssh-private-key your_username@login.cirrus.ac.uk`
  * Type your TOTP/MFA code, which only be asked once a day (unless your IP changes, then you'll be asked for another TOTP)

#### Detailed Instructions:

The steps below will also be sent to your email, with the invite to join the `tc066` project.

To get an account on Cirrus, a Tier 2 national HPC service from the EPSRC in the UK,
first you'll need an account on SAFE, the Service Administration service ran by EPCC.

You can register for a SAFE account following the steps detailed in the
[SAFE documentation](https://epcced.github.io/safe-docs/safe-for-users/#registering-logging-in-passwords),
please register using the same email address that the invite was sent to.

You will need to accept the invite to join `tc066`, create an SSH key-pair --
[more instructions here](https://docs.cirrus.ac.uk/user-guide/connecting/#ssh-key-pairs) --
and add it to the `tc066` machine account.
The public key will be a file ending in `.pub`, while the private key will have no extension.
You can either upload the public key file, or paste the text the file contains, i.e., copy the output of:

```bash
cat /path/to/your/key.pub
```

You will then need to setup an MFA (multi-factor authentication) method for time based one time passwords (TOTP) and link it to your machine account,
[see detailed instructions here](https://docs.cirrus.ac.uk/user-guide/connecting/#time-based-one-time-passcode-totp-code).

To login, use:

```bash
ssh -X -i /path/to/your/ssh/privatekey user@login.cirrus.ac.uk

# for example, for the user "tc066-rfga" using a linux system:
ssh -X -i ~/.ssh/id_rsa_cirrus tc066-rfga@login.cirrus.ac.uk
```
> [!NOTE]
> More details on how to login can be found [in the Cirrus documentation](https://docs.cirrus.ac.uk/user-guide/connecting/#ssh-clients)
> and in [this repo](../lessons/00-Connecting.md).

Next: [Setting up the environment](02-setup_environment.md), Previous: [Installing X-Windows](00-xwindow.md), Up: [Main page](../README.md)

