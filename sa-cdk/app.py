#!/usr/bin/env python3

from aws_cdk import core

from sa_cdk.sa_cdk_stack import SaCdkStack


app = core.App()
sa_stack = SaCdkStack(app, "sa-cms")
core.Tag.add(sa_stack, 'Name','sa-cms')

app.synth()
