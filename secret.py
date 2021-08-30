# using an existing secret
# requires a secret, secret keytab, in kubectl and reana access
# Couler:

import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter
from couler.core.templates.volume import VolumeMount, Volume
from couler.core.templates.volume_claim import VolumeClaimTemplate
from couler.core.syntax.volume import create_workflow_volume


def opendata():
    '''accesses an existing secret and uses it to acces reana'''

    access_key = ["keytab"]
    secret = couler.obtain_secret(
        secret_keys=access_key, namespace="argo", name="jetencoded", dry_run=False,
    )

    couler.run_container(
        image="nooraangelva/reana-auth-krb5",
        secret=secret,
        command=["bash", "-c", 'echo "Encoded keytab: $keytab"',
                 'echo "Decoded keytab: $(echo $keytab | base64 -d)"',
                 'echo $keytab | base64 -d > /mnt/vol/.keytab',
                 'kinit -k -t /mnt/vol/.keytab nangelva@CERN.CH',
                 'id',
                 'klist',
                 'ls -l /tmp/krb5cc_1000',
                 'cp /tmp/krb5cc_1000 /mnt/vol']
    )


opendata()
# couler.config_workflow(name="pytest")
submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
